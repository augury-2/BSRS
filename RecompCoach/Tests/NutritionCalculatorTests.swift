import XCTest
@testable import RecompCoach

final class NutritionCalculatorTests: XCTestCase {

    func testTotalsSumEntries() {
        let a = NutritionEntry(meal: .lunch, foodID: nil, foodName: "A", quantityGrams: 100,
                               nutrients: Nutrients([.calories: 200, .protein: 20]))
        let b = NutritionEntry(meal: .lunch, foodID: nil, foodName: "B", quantityGrams: 100,
                               nutrients: Nutrients([.calories: 150, .protein: 10, .fiber: 5]))
        let total = NutritionCalculator.totals([a, b])
        XCTAssertEqual(total.calories, 350)
        XCTAssertEqual(total.protein, 30)
        XCTAssertEqual(total.fiber, 5)
    }

    func testScaling() {
        let per100 = Nutrients([.calories: 380, .protein: 80])
        let scaled = per100.scaled(by: 30.0 / 100.0)
        XCTAssertEqual(scaled.calories, 114, accuracy: 0.01)
        XCTAssertEqual(scaled.protein, 24, accuracy: 0.01)
    }

    func testEnergyFromSteps() {
        XCTAssertEqual(NutritionCalculator.energyFromSteps(10000, weightKg: 80), 400, accuracy: 0.1)
    }

    func testWorkoutEnergyMET() {
        // MET 5, 60 min, 80 kg → 5*3.5*80/200*60 = 420
        XCTAssertEqual(NutritionCalculator.workoutEnergy(met: 5, minutes: 60, weightKg: 80), 420, accuracy: 0.5)
    }

    func testPercentRDA() {
        let targets = NutritionTargets(calories: 2000, protein: 150, carbs: 200, fat: 60,
                                       fiber: 30, steps: 10000, micros: [.iron: 10, .calcium: 1000])
        let consumed = Nutrients([.iron: 5, .calcium: 1000])
        let pct = NutritionCalculator.percentRDA(consumed, targets: targets)
        XCTAssertEqual(pct[.iron] ?? 0, 50, accuracy: 0.1)
        XCTAssertEqual(pct[.calcium] ?? 0, 100, accuracy: 0.1)
    }
}
