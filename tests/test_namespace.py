"""Test namespace package structure and extensibility."""

import owi.metadatabase
from owi.metadatabase._version import __version__
from owi.metadatabase.geometry import OWT, GeometryAPI, OWTs
from owi.metadatabase.locations import LocationsAPI


def test_namespace_package_no_file():
    """
    Verify owi is a proper PEP 420 namespace package.

    Namespace packages may have __file__ in Python 3.11+ but should
    not have __path__ as a list (it's a _NamespacePath instead).

    Examples
    --------
    >>> import owi
    >>> # Namespace packages have special __path__
    >>> str(type(owi.__path__))
    "<class '_frozen_importlib_external._NamespacePath'>"
    """
    import owi

    # Check that __path__ is a namespace path, not a regular list
    assert hasattr(owi, "__path__"), "owi should have __path__"
    assert "_NamespacePath" in str(type(owi.__path__)), (
        f"owi.__path__ should be _NamespacePath, got {type(owi.__path__)}"
    )


def test_version_accessible():
    """
    Test that version is accessible from package root.

    Examples
    --------
    >>> from owi.metadatabase._version import __version__
    >>> __version__
    '0.1.0'
    """
    assert __version__ == "0.1.0"


def test_geometry_module_importable():
    """
    Test that geometry module and its classes are importable.

    Examples
    --------
    >>> from owi.metadatabase.geometry import GeometryAPI
    >>> from owi.metadatabase.geometry import OWT, OWTs
    >>> GeometryAPI.__name__
    'GeometryAPI'
    """
    assert GeometryAPI is not None
    assert OWT is not None
    assert OWTs is not None


def test_locations_module_importable():
    """
    Test that locations module is importable.

    Examples
    --------
    >>> from owi.metadatabase.locations import LocationsAPI
    >>> LocationsAPI.__name__
    'LocationsAPI'
    """
    assert LocationsAPI is not None


def test_utils_internal_module():
    """
    Test that internal _utils module is accessible.

    Examples
    --------
    >>> from owi.metadatabase._utils import deepcompare
    >>> from owi.metadatabase._utils import APIConnectionError
    >>> APIConnectionError.__name__
    'APIConnectionError'
    """
    from owi.metadatabase._utils import (
        APIConnectionError,
        DataProcessingError,
        InvalidParameterError,
        deepcompare,
    )

    assert APIConnectionError is not None
    assert DataProcessingError is not None
    assert InvalidParameterError is not None
    assert deepcompare is not None


def test_extensibility_structure():
    """
    Test that package structure supports future extensions.

    This validates that the namespace package can be extended
    with additional modules like owi-metadatabase-fatigue or
    owi-metadatabase-soil.
    """
    import sys

    # Check that owi is in sys.modules and is a namespace
    assert "owi" in sys.modules
    assert "owi.metadatabase" in sys.modules

    # Verify the namespace package has a namespace path
    assert hasattr(owi.metadatabase, "__path__")


if __name__ == "__main__":
    """Run tests with doctest."""
    import doctest

    doctest.testmod(verbose=True)
