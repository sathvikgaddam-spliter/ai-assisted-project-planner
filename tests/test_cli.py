import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main as cli
from models import Phase, ProjectPlan, Task


def test_cli_saves_prompt_pack_zip(monkeypatch, capsys):
    plan = ProjectPlan(
        project_name="CLI Plan",
        description="Build a CLI test project.",
        domain="software",
        project_type="software application",
        complexity="medium",
        status="plan_generated",
        summary="A CLI test plan.",
    )

    monkeypatch.setattr("builtins.input", lambda _: "Build a CLI test project.")
    monkeypatch.setattr(cli, "analyze_project", lambda _: {"domain": "software"})
    monkeypatch.setattr(cli, "generate_project_plan", lambda _: plan)
    monkeypatch.setattr(cli, "save_json_output", lambda _: Path("outputs/cli-plan.plan.json"))
    monkeypatch.setattr(cli, "save_markdown_output", lambda _: Path("outputs/cli-plan.plan.md"))
    monkeypatch.setattr(cli, "save_prompt_pack_zip", lambda _: "outputs/cli-plan.prompt_pack.zip")
    monkeypatch.setattr(cli, "save_build_pack_zip", lambda analysis, plan: "outputs/cli-plan.coding-agent-job.zip")

    result = cli.main()
    output = capsys.readouterr().out

    assert result == 0
    assert "JSON output: outputs\\cli-plan.plan.json" in output or "JSON output: outputs/cli-plan.plan.json" in output
    assert "Markdown output: outputs\\cli-plan.plan.md" in output or "Markdown output: outputs/cli-plan.plan.md" in output
    assert "Prompt Pack ZIP saved to: outputs/cli-plan.prompt_pack.zip" in output
    assert "Coding Agent ZIP saved to: outputs/cli-plan.coding-agent-job.zip" in output


def test_cli_shows_draft_banner_for_incomplete_draft_plan(monkeypatch, capsys):
    plan = ProjectPlan(
        project_name="Draft CLI Plan",
        description="Build a racing game.",
        domain="software",
        project_type="game application",
        complexity="medium",
        status="clarification_required",
        summary="Draft incomplete plan.",
        phases=[
            Phase(
                id="P1",
                name="Discovery",
                objective="Clarify gameplay requirements.",
                estimated_duration="1 week",
                tasks=[
                    Task(
                        id="T1",
                        title="Define gameplay",
                        description="Clarify core gameplay loop.",
                        owner_role="Product Lead",
                        estimated_effort="1 day",
                    )
                ],
            )
        ],
        assumptions=["Target users were not specified and should be confirmed."],
        warnings=["This is a draft execution plan generated from incomplete requirements."],
        clarification_questions=["Who are the target players?"],
    )

    monkeypatch.setattr("builtins.input", lambda _: "Build a racing game")
    monkeypatch.setattr(cli, "analyze_project", lambda _: {"domain": "software"})
    monkeypatch.setattr(cli, "generate_project_plan", lambda _: plan)
    monkeypatch.setattr(cli, "save_json_output", lambda _: Path("outputs/draft-cli-plan.plan.json"))
    monkeypatch.setattr(cli, "save_markdown_output", lambda _: Path("outputs/draft-cli-plan.plan.md"))
    monkeypatch.setattr(cli, "save_prompt_pack_zip", lambda _: "outputs/draft-cli-plan.prompt_pack.zip")
    monkeypatch.setattr(cli, "save_build_pack_zip", lambda analysis, plan: "outputs/draft-cli-plan.coding-agent-job.zip")

    result = cli.main()
    output = capsys.readouterr().out

    assert result == 0
    assert "[DRAFT PLAN - REQUIREMENTS INCOMPLETE]" in output
    assert "Clarification is required before implementation." in output
