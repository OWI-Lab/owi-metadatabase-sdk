"""Test basic package imports."""

from owi.metadatabase import __version__
from owi.metadatabase.geometry import OWT, GeometryAPI, OWTs
from owi.metadatabase.locations import LocationsAPI


def test_version():
    """Test that version is accessible."""
    assert __version__ == "0.11.0"


def test_geometry_imports():
    """Test that geometry module imports work."""
    assert GeometryAPI is not None
    assert OWT is not None
    assert OWTs is not None


def test_locations_imports():
    """Test that locations module imports work."""
    assert LocationsAPI is not None
