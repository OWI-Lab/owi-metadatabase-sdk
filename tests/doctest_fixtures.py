"""
Fixtures and utilities for doctests.

This module provides sample data and helper functions to support doctests
across the owi.metadatabase package. These fixtures allow examples in docstrings
to be executable without requiring actual API access.

Examples
--------
In module docstrings, you can use these fixtures by importing them in the
doctest setup (via conftest.py):

    >>> sample_geometry = get_sample_geometry_data()
    >>> len(sample_geometry)
    3
"""

from typing import Any, Optional


def get_sample_geometry_data() -> list[dict[str, Any]]:
    """
    Get sample geometry data for doctest examples.

    Returns
    -------
    list[dict[str, Any]]
        List of sample geometry records with typical structure.

    Examples
    --------
    >>> data = get_sample_geometry_data()
    >>> data[0]["turbine"]
    'T01'
    >>> data[0]["subassembly_type"]
    'TW'
    """
    return [
        {
            "id": 1,
            "project": "SampleProject",
            "turbine": "T01",
            "subassembly_type": "TW",
            "z_position": 15000,
        },
        {
            "id": 2,
            "project": "SampleProject",
            "turbine": "T01",
            "subassembly_type": "TP",
            "z_position": -5000,
        },
        {
            "id": 3,
            "project": "SampleProject",
            "turbine": "T01",
            "subassembly_type": "MP",
            "z_position": -50000,
        },
    ]


def get_sample_location_data() -> list[dict[str, Any]]:
    """
    Get sample location data for doctest examples.

    Returns
    -------
    list[dict[str, Any]]
        List of sample location records with typical structure.

    Examples
    --------
    >>> data = get_sample_location_data()
    >>> data[0]["turbine_name"]
    'T01'
    >>> data[0]["latitude"]
    51.5
    """
    return [
        {
            "id": 1,
            "project": "SampleProject",
            "turbine_name": "T01",
            "latitude": 51.5,
            "longitude": 2.8,
            "water_depth": 25.0,
        },
        {
            "id": 2,
            "project": "SampleProject",
            "turbine_name": "T02",
            "latitude": 51.52,
            "longitude": 2.85,
            "water_depth": 26.5,
        },
    ]


def get_sample_building_block() -> dict[str, Any]:
    """
    Get a sample building block for geometry examples.

    Returns
    -------
    dict[str, Any]
        Sample building block with typical structure.

    Examples
    --------
    >>> bb = get_sample_building_block()
    >>> bb["name"]
    'BB_Tower_01'
    >>> bb["shape"]
    'Cylinder'
    """
    return {
        "id": 1,
        "name": "BB_Tower_01",
        "shape": "Cylinder",
        "diameter_top": 3.5,
        "diameter_bottom": 6.0,
        "thickness_top": 0.025,
        "thickness_bottom": 0.040,
        "height": 90.0,
        "material": "S355",
    }


def get_sample_subassembly() -> dict[str, Any]:
    """
    Get a sample subassembly for geometry examples.

    Returns
    -------
    dict[str, Any]
        Sample subassembly with typical structure.

    Examples
    --------
    >>> sa = get_sample_subassembly()
    >>> sa["type"]
    'Tower'
    >>> len(sa["building_blocks"])
    2
    """
    return {
        "id": 1,
        "type": "Tower",
        "name": "SA_Tower_01",
        "z_bottom": 15.0,
        "z_top": 105.0,
        "building_blocks": [
            {
                "id": 1,
                "name": "BB_Tower_01",
                "z_start": 15.0,
                "z_end": 60.0,
            },
            {
                "id": 2,
                "name": "BB_Tower_02",
                "z_start": 60.0,
                "z_end": 105.0,
            },
        ],
    }


def get_sample_material() -> dict[str, Any]:
    """
    Get a sample material definition.

    Returns
    -------
    dict[str, Any]
        Sample material with typical properties.

    Examples
    --------
    >>> mat = get_sample_material()
    >>> mat["name"]
    'S355'
    >>> mat["yield_strength"]
    355.0
    """
    return {
        "id": 1,
        "name": "S355",
        "yield_strength": 355.0,
        "young_modulus": 210000.0,
        "density": 7850.0,
        "poisson_ratio": 0.3,
    }


def get_sample_api_response() -> dict[str, Any]:
    """
    Get a sample API response structure.

    Returns
    -------
    dict[str, Any]
        Sample API response with count and results.

    Examples
    --------
    >>> resp = get_sample_api_response()
    >>> resp["count"]
    3
    >>> len(resp["results"])
    3
    """
    return {
        "count": 3,
        "next": None,
        "previous": None,
        "results": get_sample_geometry_data(),
    }


class MockAPIResponse:
    """
    Mock API response for doctest examples.

    This class simulates a requests.Response object with controlled data,
    allowing doctests to demonstrate API interaction without network calls.

    Parameters
    ----------
    status_code : int
        HTTP status code, default is 200.
    json_data : dict[str, Any] or None
        Data to return from .json() method.

    Examples
    --------
    >>> resp = MockAPIResponse(200, {"count": 1, "results": []})
    >>> resp.status_code
    200
    >>> resp.json()["count"]
    1
    """

    def __init__(
        self,
        status_code: int = 200,
        json_data: Optional[dict[str, Any]] = None,
    ) -> None:
        """Initialize mock API response."""
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self) -> dict[str, Any]:
        """Return JSON data."""
        return self._json_data

    def raise_for_status(self) -> None:
        """Simulate raise_for_status for non-200 codes."""
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


# Common sample data for different modules
SAMPLE_TURBINES = ["T01", "T02", "T03"]
SAMPLE_PROJECT = "SampleProject"
SAMPLE_COORDINATES = [(51.5, 2.8), (51.52, 2.85), (51.54, 2.9)]
SAMPLE_WATER_DEPTHS = [25.0, 26.5, 27.0]
