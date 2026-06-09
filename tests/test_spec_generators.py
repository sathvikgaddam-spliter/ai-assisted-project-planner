import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from planner import generate_project_plan
from project_analyzer import analyze_project
from spec_generators import REQUIRED_BUILD_PACK_FILES, generate_build_pack


def test_generate_build_pack_returns_all_required_files():
    analysis = analyze_project("Build a SaaS expense tracker")
    plan = generate_project_plan("Build a SaaS expense tracker", use_ai=False)

    build_pack = generate_build_pack(analysis, plan)

    assert set(build_pack.keys()) == set(REQUIRED_BUILD_PACK_FILES)


def test_generated_build_pack_files_are_non_empty_markdown():
    analysis = analyze_project("Build a SaaS expense tracker")
    build_pack = generate_build_pack(analysis)

    for filename, content in build_pack.items():
        assert filename.endswith(".md")
        assert content.strip()
        assert content.startswith("#")


def test_saas_expense_tracker_specs_include_inferred_content():
    analysis = analyze_project("Build a SaaS expense tracker")
    build_pack = generate_build_pack(analysis)

    assert "SaaS application" in build_pack["project_brief.md"]
    assert "workspace users" in build_pack["project_brief.md"]
    assert "Workspace" in build_pack["database_schema.md"]
    assert "auth APIs" in build_pack["api_spec.md"]
    assert "dashboard shell" in build_pack["frontend_spec.md"]


def test_marketplace_specs_include_marketplace_entities_and_workflows():
    analysis = analyze_project("Build a marketplace for used textbooks")
    build_pack = generate_build_pack(analysis)

    assert "marketplace" in build_pack["project_brief.md"]
    assert "buyers" in build_pack["requirements.md"]
    assert "sellers" in build_pack["requirements.md"]
    assert "Listing" in build_pack["database_schema.md"]
    assert "Transaction" in build_pack["database_schema.md"]
    assert "listing APIs" in build_pack["architecture.md"]


def test_ai_study_planner_specs_include_ai_and_planner_features():
    analysis = analyze_project("Build an AI study planner")
    build_pack = generate_build_pack(analysis)

    assert "AI application" in build_pack["project_brief.md"]
    assert "model integration" in build_pack["requirements.md"]
    assert "Prompt" in build_pack["database_schema.md"]
    assert "AI orchestration API" in build_pack["api_spec.md"]
    assert "reminders" in build_pack["mvp_scope.md"]
    assert "calendar or timeline views" in build_pack["frontend_spec.md"]


def test_coding_agent_prompt_contains_agent_instructions():
    analysis = analyze_project("Build a marketplace for used textbooks")
    build_pack = generate_build_pack(analysis)
    prompt = build_pack["coding_agent_prompt.md"]

    assert "Codex/Claude/Cursor-style coding agent" in prompt
    assert "Generate a runnable application source tree" in prompt
    assert "Create actual source code" in prompt
    assert "Create build and runtime configuration" in prompt
    assert "Add a README with exact install, run, test, and build commands." in prompt
    assert "architecture.md" in prompt
    assert "database_schema.md" in prompt
    assert "api_spec.md" in prompt
    assert "Build the complete MVP, not only a minimal prototype." in prompt
    assert "Write unit, integration, API, frontend, and end-to-end tests." in prompt
    assert "Use assumptions.md when details are incomplete" in prompt


def test_start_here_contains_clear_application_build_instructions():
    analysis = analyze_project("Build a SaaS expense tracker")
    build_pack = generate_build_pack(analysis)
    start_here = build_pack["START_HERE.md"]

    assert "Create a complete runnable MVP application" in start_here
    assert "generate actual source code" in start_here
    assert "Do not only summarize" in start_here
    assert "package.json" in start_here
    assert "exact install, run, test, and build commands" in start_here


def test_copy_this_prompt_tells_coding_agent_to_build_requested_app():
    analysis = analyze_project("Build a marketplace for used textbooks")
    build_pack = generate_build_pack(analysis)
    prompt = build_pack["COPY_THIS_PROMPT.md"]

    assert "Paste this prompt into Codex" in prompt
    assert "Your task is to build the application the user requested." in prompt
    assert "Generate actual source code" in prompt
    assert "Do not only summarize the documents." in prompt
    assert "Create or modify files until the project is runnable locally." in prompt


def test_implementation_steps_include_build_order_and_milestones():
    analysis = analyze_project("Build a SaaS expense tracker")
    plan = generate_project_plan("Build a SaaS expense tracker", use_ai=False)
    build_pack = generate_build_pack(analysis, plan)
    implementation_steps = build_pack["implementation_steps.md"]

    assert "## Build Order" in implementation_steps
    assert "## Milestones" in implementation_steps
    assert "Complete" in implementation_steps
    assert "Testing Checkpoints" in implementation_steps
