from planner import generate_project_plan
from utils import save_json_output, save_markdown_output


def main() -> int:
    print("AI-Assisted Project Planner - Phase 1")
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

    if plan.clarification_questions:
        print("")
        print("Clarification questions:")
        for index, question in enumerate(plan.clarification_questions, start=1):
            print(f"{index}. {question}")

    json_path = save_json_output(plan)
    markdown_path = save_markdown_output(plan)

    print("")
    print(f"JSON output: {json_path}")
    print(f"Markdown output: {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
