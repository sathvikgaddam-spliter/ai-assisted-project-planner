import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from project_analyzer import analyze_project, infer_build_pack_understanding


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


def test_specific_short_software_product_is_not_vague():
    analysis = analyze_project("Build a personal expense tracker web app")

    assert analysis["domain"] == "software"
    assert analysis["requires_clarification"] is False


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
    assert analysis["meaningful_project_intent"] is False
    assert "timeline" in analysis["missing_information"]


def test_analyzer_detects_meaningful_short_project_intent():
    analysis = analyze_project("Build a racing game")

    assert analysis["domain"] == "software"
    assert analysis["requires_clarification"] is True
    assert analysis["meaningful_project_intent"] is True


def test_analyzer_flags_unrealistic_scope():
    analysis = analyze_project(
        "Build a full e-commerce marketplace with payments, inventory, seller dashboards, mobile apps, and analytics in one week."
    )

    assert analysis["domain"] == "analytics" or analysis["domain"] == "software"
    assert analysis["complexity"] == "high"
    assert analysis["warnings"]


def test_build_pack_understanding_for_single_line_project():
    analysis = analyze_project("Build a SaaS expense tracker")
    understanding = analysis["build_pack_understanding"]

    assert analysis["detected_project_type"] == "SaaS application"
    assert understanding["detected_project_type"] == "SaaS application"
    assert "workspace users" in understanding["target_users"]
    assert "authentication" in understanding["core_features"]
    assert "Workspace" in understanding["likely_data_entities"]
    assert understanding["frontend_needs"]
    assert understanding["backend_api_needs"]
    assert understanding["infrastructure_testing_assumptions"]


def test_build_pack_marketplace_detection():
    understanding = infer_build_pack_understanding("Build a marketplace for used textbooks", "software")

    assert understanding["detected_project_type"] == "marketplace"
    assert "buyers" in understanding["target_users"]
    assert "sellers" in understanding["target_users"]
    assert "Listing" in understanding["likely_data_entities"]
    assert "transactions" in understanding["core_features"]


def test_build_pack_ai_application_detection():
    understanding = infer_build_pack_understanding("Build an AI study planner", "software")

    assert understanding["detected_project_type"] == "AI application"
    assert "model integration" in understanding["core_features"]
    assert "Prompt" in understanding["likely_data_entities"]
    assert "prompt input" in understanding["frontend_needs"]


def test_build_pack_ecommerce_detection():
    understanding = infer_build_pack_understanding("Create an ecommerce application for handmade products", "software")

    assert understanding["detected_project_type"] == "ecommerce application"
    assert "products" in understanding["core_features"]
    assert "cart" in understanding["core_features"]
    assert "Order" in understanding["likely_data_entities"]


def test_build_pack_dashboard_detection():
    understanding = infer_build_pack_understanding("Build an analytics dashboard for warehouse managers", "analytics")

    assert understanding["detected_project_type"] == "dashboard"
    assert "metrics" in understanding["core_features"]
    assert "filters" in understanding["core_features"]
    assert "chart layout" in understanding["frontend_needs"]


def test_build_pack_generic_fallback():
    understanding = infer_build_pack_understanding("Build a volunteer coordination tool", "software")

    assert understanding["detected_project_type"] == "generic web application"
    assert "end users" in understanding["target_users"]
    assert "CRUD workflows" in understanding["core_features"]
