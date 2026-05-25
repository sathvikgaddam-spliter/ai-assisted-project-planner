from pathlib import Path
from string import Template
from typing import Dict


class PromptManager:
    def __init__(self, prompts_dir: Path | str = "prompts"):
        self.prompts_dir = Path(prompts_dir)

    def load_prompt(self, prompt_name: str) -> str:
        path = self.prompts_dir / prompt_name
        if not path.exists():
            raise FileNotFoundError(f"Prompt template not found: {path}")
        return path.read_text(encoding="utf-8")

    def render_prompt(self, prompt_name: str, variables: Dict[str, object]) -> str:
        template = Template(self.load_prompt(prompt_name))
        safe_variables = {key: str(value) for key, value in variables.items()}
        return template.safe_substitute(safe_variables)
