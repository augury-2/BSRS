import Foundation

/// Thin REST client for the cloud backend (see Backend/API.md). All calls are
/// optional; failures are surfaced to the caller and never block local use.
protocol APIClienting {
    func pushOps(_ ops: [SyncOp]) async throws -> [UUID]          // returns applied op ids
    func pullDeltas(since: Date?) async throws -> PullResponse
    func foodDeltas(since: Date?) async throws -> [FoodDTO]
    func coachChat(messages: [ChatMessage], context: WeeklySnapshot) async throws -> String
}

struct PullResponse: Codable {
    var profile: ProfileDTO?
    var foods: [FoodDTO]
    var entries: [EntryDTO]
    var measurements: [MeasurementDTO]
    var serverTime: Date
}

struct ChatMessage: Codable, Identifiable, Equatable {
    enum Role: String, Codable { case user, assistant, system }
    var id = UUID()
    var role: Role
    var content: String
}

final class APIClient: APIClienting {
    private let baseURL: URL
    private let session: URLSession
    var authToken: String?

    init(baseURL: URL = URL(string: "https://api.recompcoach.app/v1")!,
         session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session
    }

    private func makeRequest(_ path: String, method: String, body: Encodable? = nil) throws -> URLRequest {
        var req = URLRequest(url: baseURL.appending(path: path))
        req.httpMethod = method
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if let token = authToken { req.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization") }
        if let body { req.httpBody = try JSONEncoder.iso.encode(AnyEncodable(body)) }
        return req
    }

    private func send<T: Decodable>(_ req: URLRequest, as: T.Type) async throws -> T {
        let (data, resp) = try await session.data(for: req)
        guard let http = resp as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw APIError.badStatus((resp as? HTTPURLResponse)?.statusCode ?? -1)
        }
        return try JSONDecoder.iso.decode(T.self, from: data)
    }

    func pushOps(_ ops: [SyncOp]) async throws -> [UUID] {
        struct Req: Encodable { let ops: [SyncOp] }
        struct Resp: Decodable { let applied: [UUID] }
        let req = try makeRequest("/sync/push", method: "POST", body: Req(ops: ops))
        return try await send(req, as: Resp.self).applied
    }

    func pullDeltas(since: Date?) async throws -> PullResponse {
        var path = "/sync/pull"
        if let since { path += "?since=\(ISO8601DateFormatter().string(from: since))" }
        return try await send(try makeRequest(path, method: "GET"), as: PullResponse.self)
    }

    func foodDeltas(since: Date?) async throws -> [FoodDTO] {
        struct Resp: Decodable { let foods: [FoodDTO] }
        var path = "/foods"
        if let since { path += "?since=\(ISO8601DateFormatter().string(from: since))" }
        return try await send(try makeRequest(path, method: "GET"), as: Resp.self).foods
    }

    func coachChat(messages: [ChatMessage], context: WeeklySnapshot) async throws -> String {
        struct Req: Encodable { let messages: [ChatMessage]; let context: WeeklySnapshot }
        struct Resp: Decodable { let reply: String }
        let req = try makeRequest("/coach/chat", method: "POST", body: Req(messages: messages, context: context))
        return try await send(req, as: Resp.self).reply
    }

    enum APIError: Error { case badStatus(Int) }
}

// MARK: - JSON helpers

extension JSONEncoder { static let iso: JSONEncoder = { let e = JSONEncoder(); e.dateEncodingStrategy = .iso8601; return e }() }
extension JSONDecoder { static let iso: JSONDecoder = { let d = JSONDecoder(); d.dateDecodingStrategy = .iso8601; return d }() }

struct AnyEncodable: Encodable {
    private let encodeFunc: (Encoder) throws -> Void
    init(_ wrapped: Encodable) { encodeFunc = wrapped.encode }
    func encode(to encoder: Encoder) throws { try encodeFunc(encoder) }
}
