from planner import generate_project_plan
from utils import is_draft_plan, save_json_output, save_markdown_output, save_prompt_pack_zip


def main() -> int:
    print("AI-Assisted Project Planner - Phase 2")
    description = input("Enter project description: ").strip()

    try:
        plan = generate_project_plan(description)
    except ValueError as exc:
        print(f"Validation error: {exc}")
        return 1

    print("")
    print("Plan Summary")
    print(f"Project: {plan.project_name}")
    print(f"Domain: {plan.domain}")
    print(f"Type: {plan.project_type}")
    print(f"Complexity: {plan.complexity}")
    print(f"Status: {plan.status}")

    if is_draft_plan(plan):
        print("")
        print("[DRAFT PLAN - REQUIREMENTS INCOMPLETE]")
        print("Clarification is required before implementation. Assumptions and engineering prompts must be reviewed.")

    if plan.clarification_questions:
        print("")
        print("Clarification questions:")
        for index, question in enumerate(plan.clarification_questions, start=1):
            print(f"{index}. {question}")

    if plan.warnings:
        print("")
        print("Warnings and debug notes:")
        for warning in plan.warnings:
            print(f"- {warning}")

    json_path = save_json_output(plan)
    markdown_path = save_markdown_output(plan)
    prompt_pack_zip_path = save_prompt_pack_zip(plan)

    print("")
    print(f"JSON output: {json_path}")
    print(f"Markdown output: {markdown_path}")
    print(f"Prompt Pack ZIP saved to: {prompt_pack_zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
