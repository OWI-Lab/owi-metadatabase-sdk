"""
OWI Metadatabase SDK - Core package for geometry and location data.

This is a namespace package that provides access to the OWI-Lab
metadatabase for offshore wind installations. The package follows
PEP 420 namespace package conventions to allow for modular extensions.

Modules
-------
geometry : Module for handling geometry data
locations : Module for handling location data

Examples
--------
>>> from owi.metadatabase.geometry.io import GeometryAPI
>>> from owi.metadatabase.locations.io import LocationsAPI
"""

from owi.metadatabase._version import __version__

__all__ = ["__version__"]
