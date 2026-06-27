import XCTest
@testable import RecompCoach

final class CoachingEngineTests: XCTestCase {

    private func base(goal: GoalType = .loseFatMaintainMuscle) -> WeeklySnapshot {
        WeeklySnapshot(goal: goal, bodyWeightKg: 80, weightChangeKgPerWeek: -0.5,
                       waistChangeCmPerWeek: -0.3, avgCalories: 2000, calorieTarget: 2100,
                       avgProtein: 170, proteinTarget: 175, avgFiber: 28, fiberTarget: 30,
                       avgSteps: 9000, stepsTarget: 10000, trainingDaysPerWeek: 5,
                       loggingDays: 6, reportedLowEnergy: false, avgSleepHours: 7.5)
    }

    func testLosingTooFastWarns() {
        var s = base(); s.weightChangeKgPerWeek = -1.5   // ~1.9%/week
        let insights = CoachingEngine.analyze(s)
        XCTAssertTrue(insights.contains { $0.title.contains("too fast") && $0.severity == .warning })
    }

    func testIdealPaceIsPositive() {
        let insights = CoachingEngine.analyze(base())   // 0.5kg/0.625%
        XCTAssertTrue(insights.contains { $0.severity == .positive && $0.title.contains("Ideal") })
    }

    func testRecompClassificationWhenStableWeightWaistDown() {
        let label = CoachingEngine.classifyTrend(weightChangeKgPerWeek: 0.0,
                                                 waistChangeCmPerWeek: -0.4, bodyWeightKg: 80)
        XCTAssertEqual(label, "Losing fat while maintaining muscle")
    }

    func testLowProteinTriggersAction() {
        var s = base(); s.avgProtein = 120; s.proteinTarget = 175
        let insights = CoachingEngine.analyze(s)
        XCTAssertTrue(insights.contains { $0.title.contains("protein") && $0.severity == .action })
    }

    func testInsightsOrderedActionFirst() {
        var s = base(); s.avgProtein = 100; s.weightChangeKgPerWeek = -1.6
        let insights = CoachingEngine.analyze(s)
        // First non-info insight should be an action/warning, not positive.
        XCTAssertNotEqual(insights.first?.severity, .positive)
    }

    func testLowLoggingNudges() {
        var s = base(); s.loggingDays = 2
        let insights = CoachingEngine.analyze(s)
        XCTAssertTrue(insights.contains { $0.title.contains("Log a little more") })
    }
}
