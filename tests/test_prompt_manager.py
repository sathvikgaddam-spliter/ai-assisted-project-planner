import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt_manager import PromptManager


def test_prompt_manager_loads_prompt():
    manager = PromptManager(Path(__file__).resolve().parents[1] / "prompts")

    content = manager.load_prompt("planning_prompt.txt")

    assert "structured project plan" in content


def test_prompt_manager_renders_variables(tmp_path):
    prompt_file = tmp_path / "example.txt"
    prompt_file.write_text("Project: $project_description", encoding="utf-8")
    manager = PromptManager(tmp_path)

    rendered = manager.render_prompt("example.txt", {"project_description": "Build dashboard"})

    assert rendered == "Project: Build dashboard"


def test_prompt_manager_missing_prompt_raises(tmp_path):
    manager = PromptManager(tmp_path)

    with pytest.raises(FileNotFoundError):
        manager.load_prompt("missing.txt")
