from pathlib import Path


def test_optional_dependencies_include_soil():
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject_text = pyproject_path.read_text()

    assert "[project.optional-dependencies]" in pyproject_text
    assert "owi-metadatabase-soil" in pyproject_text


def test_optional_dependencies_include_results():
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject_text = pyproject_path.read_text()

    assert "[project.optional-dependencies]" in pyproject_text
    assert "owi-metadatabase-results" in pyproject_text
