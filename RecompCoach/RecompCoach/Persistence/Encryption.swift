import Foundation
import CryptoKit
import Security

/// Stores a 256-bit symmetric key in the Keychain and provides AES-GCM
/// seal/open for encrypted exports and field-level secrets (e.g. auth tokens).
///
/// The SwiftData store itself is protected at rest by iOS Data Protection
/// (`FileProtectionType.complete`, applied in `AppDatabase`). For full-database
/// encryption beyond Data Protection, swap the store for SQLCipher.
enum AppCrypto {

    private static let service = "app.recompcoach.key"
    private static let account = "primary-symmetric-key"

    static func symmetricKey() throws -> SymmetricKey {
        if let existing = try loadKey() { return existing }
        let key = SymmetricKey(size: .bits256)
        try storeKey(key)
        return key
    }

    static func seal(_ data: Data) throws -> Data {
        let key = try symmetricKey()
        let box = try AES.GCM.seal(data, using: key)
        guard let combined = box.combined else { throw CryptoError.sealFailed }
        return combined
    }

    static func open(_ data: Data) throws -> Data {
        let key = try symmetricKey()
        let box = try AES.GCM.SealedBox(combined: data)
        return try AES.GCM.open(box, using: key)
    }

    // MARK: - Keychain

    private static func storeKey(_ key: SymmetricKey) throws {
        let raw = key.withUnsafeBytes { Data($0) }
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
            kSecValueData as String: raw
        ]
        SecItemDelete(query as CFDictionary)
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else { throw CryptoError.keychain(status) }
    }

    private static func loadKey() throws -> SymmetricKey? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        var item: CFTypeRef?
        let status = SecItemCopyMatching(query as CFDictionary, &item)
        if status == errSecItemNotFound { return nil }
        guard status == errSecSuccess, let data = item as? Data else { throw CryptoError.keychain(status) }
        return SymmetricKey(data: data)
    }

    enum CryptoError: Error { case sealFailed, keychain(OSStatus) }
}
