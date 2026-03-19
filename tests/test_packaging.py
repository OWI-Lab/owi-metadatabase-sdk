from pathlib import Path


def test_optional_dependencies_include_soil():
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    pyproject_text = pyproject_path.read_text()

    assert "[project.optional-dependencies]" in pyproject_text
    assert 'soil = [\n    "owi-metadatabase-soil >=0.1.0",\n]' in pyproject_text
