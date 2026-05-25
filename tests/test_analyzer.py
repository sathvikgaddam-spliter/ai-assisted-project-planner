import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from project_analyzer import analyze_project


def test_analyzer_detects_software_project():
    analysis = analyze_project("Build an expense tracker app for college students.")

    assert analysis["domain"] == "software"
    assert analysis["project_type"] == "software MVP"
    assert analysis["complexity"] == "medium"


def test_software_product_keywords_win_over_report_wording():
    analysis = analyze_project(
        "Build a mobile-friendly expense tracker app for college students to categorize spending, set monthly budgets, and export simple reports by the end of the semester."
    )

    assert analysis["domain"] == "software"
    assert analysis["project_type"] == "software MVP"


def test_analyzer_detects_analytics_project():
    analysis = analyze_project("Build a Power BI dashboard for sales managers.")

    assert analysis["domain"] == "analytics"
    assert analysis["project_type"] == "Power BI dashboard"


def test_analyzer_detects_academic_project():
    analysis = analyze_project("Research AI workflows for an independent study.")

    assert analysis["domain"] == "academic"
    assert analysis["project_type"] == "independent study plan"


def test_analyzer_marks_vague_input_for_clarification():
    analysis = analyze_project("I want to build something for students.")

    assert analysis["requires_clarification"] is True
    assert "timeline" in analysis["missing_information"]


def test_analyzer_flags_unrealistic_scope():
    analysis = analyze_project(
        "Build a full e-commerce marketplace with payments, inventory, seller dashboards, mobile apps, and analytics in one week."
    )

    assert analysis["domain"] == "analytics" or analysis["domain"] == "software"
    assert analysis["complexity"] == "high"
    assert analysis["warnings"]
