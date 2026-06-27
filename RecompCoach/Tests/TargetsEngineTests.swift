import XCTest
@testable import RecompCoach

final class TargetsEngineTests: XCTestCase {

    func testMifflinNoBodyFat() {
        let p = UserProfile(age: 28, sex: .male, heightCm: 174, currentWeightKg: 81,
                            goal: .loseFatMaintainMuscle, activity: .moderate)
        let r = TargetsEngine.compute(for: p)
        // BMR = 10*81 + 6.25*174 - 5*28 + 5 = 1762.5
        XCTAssertEqual(r.bmr, 1763, accuracy: 1)
        // TDEE = 1762.5 * 1.55 ≈ 2732
        XCTAssertEqual(r.tdee, 2732, accuracy: 1)
        // Calories = TDEE * 0.80 ≈ 2186 → rounded to 10
        XCTAssertEqual(r.targets.calories, 2190, accuracy: 10)
        // Protein = 2.2 * 81 ≈ 178 g (no lean mass)
        XCTAssertEqual(r.targets.protein, 178, accuracy: 1)
        // Fat = 0.8 * 81 ≈ 65 g
        XCTAssertEqual(r.targets.fat, 65, accuracy: 1)
        // Fiber = 14 * kcal / 1000
        XCTAssertEqual(r.targets.fiber, 31, accuracy: 1)
    }

    func testKatchWithBodyFatUsesLeanMass() {
        let p = UserProfile(age: 28, sex: .male, heightCm: 174, currentWeightKg: 81,
                            goal: .loseFatGainMuscle, activity: .moderate, bodyFatPercent: 22)
        let r = TargetsEngine.compute(for: p)
        // LBM = 81 * 0.78 = 63.18; Katch BMR = 370 + 21.6*63.18 ≈ 1735
        XCTAssertEqual(r.bmr, 1735, accuracy: 1)
        // Protein = 2.8 * 63.18 ≈ 177 g
        XCTAssertEqual(r.targets.protein, 177, accuracy: 1)
    }

    func testCalorieFloorRespected() {
        let p = UserProfile(age: 70, sex: .female, heightCm: 150, currentWeightKg: 45,
                            goal: .loseFatMaintainMuscle, activity: .sedentary)
        let r = TargetsEngine.compute(for: p)
        XCTAssertGreaterThanOrEqual(r.targets.calories, 1200)
    }

    func testMicroRDADiffersBySex() {
        let male = UserProfile(sex: .male)
        let female = UserProfile(sex: .female)
        XCTAssertEqual(TargetsEngine.microRDAs(for: male)[.iron], 8)
        XCTAssertEqual(TargetsEngine.microRDAs(for: female)[.iron], 18)
    }
}
