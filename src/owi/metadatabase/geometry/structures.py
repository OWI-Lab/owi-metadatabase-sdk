"""Module containing the data classes for the geometry module."""

# mypy: ignore-errors

from typing import Any, TypedDict, Union, cast

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from numpy import pi

from owi.metadatabase._utils.utils import deepcompare

PLOT_SETTINGS_SUBASSEMBLY = {
    "MP": {"color": "brown"},
    "TP": {"color": "goldenrod"},
    "TW": {"color": "grey"},
}

DEFAULT_NP_FLOAT64_VALUE = np.float64(0.0)


class DataMat(TypedDict):
    title: str
    slug: str
    id: np.int64
    description: str
    young_modulus: np.float64
    density: np.float64
    poisson_ratio: np.float64


class DataBB(TypedDict):
    id: np.int64
    description: str
    slug: str
    alpha: np.float64
    beta: np.float64
    gamma: np.float64
    x_position: np.float64
    y_position: np.float64
    z_position: np.float64
    vertical_position_reference_system: str
    title: str
    height: np.float64
    mass_distribution: np.float64
    volume_distribution: np.float64
    area_distribution: np.float64
    c_d: np.float64
    c_m: np.float64
    sub_assembly: np.int64
    projectsite_name: str
    asset_name: str
    subassembly_name: str
    material_name: str
    youngs_modulus: np.float64
    density: np.float64
    poissons_ratio: np.float64
    bottom_outer_diameter: np.float64
    top_outer_diameter: np.float64
    wall_thickness: np.float64
    material: np.float64
    moment_of_inertia_x: np.float64
    moment_of_inertia_y: np.float64
    moment_of_inertia_z: np.float64
    mass: np.float64


class DataSA(TypedDict):
    id: np.int64
    title: str
    description: str
    slug: str
    x_position: np.float64
    y_position: np.float64
    z_position: np.float64
    vertical_position_reference_system: str
    subassembly_type: str
    source: str
    asset: np.int64
    model_definition: np.int64


class BaseStructure:
    """Base class for all structures."""

    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            comp = deepcompare(self, other)
            assert comp[0], comp[1]
        elif isinstance(other, dict):
            comp = deepcompare(self.__dict__, other)
            assert comp[0], comp[1]
        else:
            raise AssertionError("Comparison is not possible due to incompatible types!")
        return comp[0]


class Material(BaseStructure):
    """Material derived from the raw data."""

    def __init__(self, json: DataMat) -> None:
        """
        Create an instance of the Material class with required
        parameters.

        Parameters
        ----------
        json : DataMat
            JSON data containing the material information.

        Examples
        --------
        >>> data = {
        ...     "title": "Steel",
        ...     "slug": "steel",
        ...     "id": np.int64(1),
        ...     "description": "",
        ...     "young_modulus": np.float64(210000.0),
        ...     "density": np.float64(7850.0),
        ...     "poisson_ratio": np.float64(0.3),
        ... }
        >>> material = Material(data)
        >>> material.title
        'Steel'
        """
        self.title = json["title"]
        self.description = json["description"]
        self.density = json["density"]
        self.poisson_ratio = json["poisson_ratio"]
        self.young_modulus = json["young_modulus"]
        self.id = json["id"]

    def as_dict(self) -> dict[str, Union[str, np.float64]]:
        """
        Transform data into dictionary.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "title": Name of the material.
            - "description": Description of the material.
            - "poisson_ratio": Poisson ratio of the material.
            - "young_modulus": Young modulus of the material.

        Examples
        --------
        >>> data = {
        ...     "title": "Steel",
        ...     "slug": "steel",
        ...     "id": np.int64(1),
        ...     "description": "",
        ...     "young_modulus": np.float64(210000.0),
        ...     "density": np.float64(7850.0),
        ...     "poisson_ratio": np.float64(0.3),
        ... }
        >>> Material(data).as_dict()["title"]
        'Steel'
        """
        return {
            "title": self.title,
            "description": self.description,
            "poisson_ratio": self.poisson_ratio,
            "young_modulus": self.young_modulus,
        }


class Position(BaseStructure):
    """Position of the components."""

    def __init__(
        self,
        x: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
        y: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
        z: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
        alpha: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
        beta: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
        gamma: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
        reference_system: str = "LAT",
    ) -> None:
        """
        Create an instance of the Position class with required
        parameters.

        Parameters
        ----------
        x : np.float64, optional
            X coordinate of the component.
        y : np.float64, optional
            Y coordinate of the component.
        z : np.float64, optional
            Z coordinate of the component.
        alpha : np.float64, optional
            Rotation around the x-axis.
        beta : np.float64, optional
            Rotation around the y-axis.
        gamma : np.float64, optional
            Rotation around the z-axis.
        reference_system : str, optional
            Reference system for the vertical position, default is
            "LAT".

        Examples
        --------
        >>> pos = Position(np.float64(1), np.float64(2), np.float64(3))
        >>> tuple(map(float, (pos.x, pos.y, pos.z)))
        (1.0, 2.0, 3.0)
        """
        self.x = x
        self.y = y
        self.z = z
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.reference_system = reference_system


class BuildingBlock(BaseStructure):
    """Building blocks description."""

    def __init__(self, json: DataBB, subassembly: Union[Any, None] = None) -> None:
        """
        Create an instance of the BuildingBlock class with required
        parameters.

        Parameters
        ----------
        json : DataBB
            JSON data containing the building block information.
        subassembly : Any, optional
            Subassembly object containing the building block.

        Examples
        --------
        >>> data = {
        ...     "id": np.int64(1),
        ...     "description": "",
        ...     "slug": "bb",
        ...     "alpha": np.float64(0),
        ...     "beta": np.float64(0),
        ...     "gamma": np.float64(0),
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "title": "BB_1",
        ...     "height": np.float64(0),
        ...     "mass_distribution": np.float64(np.nan),
        ...     "volume_distribution": np.float64(np.nan),
        ...     "area_distribution": np.float64(np.nan),
        ...     "c_d": np.float64(np.nan),
        ...     "c_m": np.float64(np.nan),
        ...     "sub_assembly": np.int64(1),
        ...     "projectsite_name": "Site",
        ...     "asset_name": "T01",
        ...     "subassembly_name": "SA",
        ...     "material_name": "Steel",
        ...     "youngs_modulus": np.float64(np.nan),
        ...     "density": np.float64(np.nan),
        ...     "poissons_ratio": np.float64(np.nan),
        ...     "bottom_outer_diameter": np.float64(np.nan),
        ...     "top_outer_diameter": np.float64(np.nan),
        ...     "wall_thickness": np.float64(np.nan),
        ...     "material": np.float64(np.nan),
        ...     "moment_of_inertia_x": np.float64(1.0),
        ...     "moment_of_inertia_y": np.float64(2.0),
        ...     "moment_of_inertia_z": np.float64(3.0),
        ...     "mass": np.float64(100.0),
        ... }
        >>> BuildingBlock(data).title
        'BB_1'
        """
        self.id = json["id"]
        self.title = json["title"]
        if json["description"]:
            self.description = json["description"]
        else:
            self.description = ""
        self.position = Position(
            x=json["x_position"],
            y=json["y_position"],
            z=json["z_position"],
            alpha=json["alpha"],
            beta=json["beta"],
            gamma=json["gamma"],
            reference_system=json["vertical_position_reference_system"],
        )
        self.material = None
        if "material" in json and subassembly:
            material_id = json["material"]
            if material_id and not np.isnan(material_id):
                for mat in subassembly.materials:
                    if np.int64(mat.id) == np.int64(material_id):
                        self.material = mat
                        break
        self.json = json

    @property
    def type(self) -> str:
        """
        Type of the building block.

        Examples
        --------
        >>> data = {
        ...     "id": np.int64(1),
        ...     "description": "",
        ...     "slug": "bb",
        ...     "alpha": np.float64(0),
        ...     "beta": np.float64(0),
        ...     "gamma": np.float64(0),
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "title": "BB_1",
        ...     "height": np.float64(0),
        ...     "mass_distribution": np.float64(np.nan),
        ...     "volume_distribution": np.float64(np.nan),
        ...     "area_distribution": np.float64(np.nan),
        ...     "c_d": np.float64(np.nan),
        ...     "c_m": np.float64(np.nan),
        ...     "sub_assembly": np.int64(1),
        ...     "projectsite_name": "Site",
        ...     "asset_name": "T01",
        ...     "subassembly_name": "SA",
        ...     "material_name": "Steel",
        ...     "youngs_modulus": np.float64(np.nan),
        ...     "density": np.float64(np.nan),
        ...     "poissons_ratio": np.float64(np.nan),
        ...     "bottom_outer_diameter": np.float64(np.nan),
        ...     "top_outer_diameter": np.float64(np.nan),
        ...     "wall_thickness": np.float64(np.nan),
        ...     "material": np.float64(np.nan),
        ...     "moment_of_inertia_x": np.float64(1.0),
        ...     "moment_of_inertia_y": np.float64(2.0),
        ...     "moment_of_inertia_z": np.float64(3.0),
        ...     "mass": np.float64(100.0),
        ... }
        >>> BuildingBlock(data).type
        'lumped_mass'
        """
        cond = {
            "bottom_outer_diameter": "tubular_section",
            "mass": "lumped_mass",
            "mass_distribution": "distributed_mass",
        }
        for k in cond:
            if (
                k in self.json
                and self.json[k] is not None  # type: ignore
                and not np.isnan(self.json[k])  # type: ignore
            ):
                return cond[k]
        raise ValueError("Could not find supported building block type.")

    @property
    def wall_thickness(self) -> Union[np.float64, None]:
        """Wall thickness of the building block (if exists), mm."""
        if self.type == "tubular_section":
            return self.json["wall_thickness"]
        else:
            return None

    @property
    def bottom_outer_diameter(self) -> Union[np.float64, None]:
        """Bottom outer diameter of the building block (if exists), mm."""
        if self.type == "tubular_section":
            return self.json["bottom_outer_diameter"]
        else:
            return None

    @property
    def top_outer_diameter(self) -> Union[np.float64, None]:
        """Top outer diameter of the building block (if exists), mm."""
        if self.type == "tubular_section":
            return self.json["top_outer_diameter"]
        else:
            return None

    @property
    def diameter_str(self) -> str:
        """Diameter of the building block as a string (if exists), mm."""
        if (
            self.top_outer_diameter
            and self.bottom_outer_diameter
            and not np.isnan(self.top_outer_diameter)
            and not np.isnan(self.bottom_outer_diameter)
        ):
            if self.top_outer_diameter != self.bottom_outer_diameter:
                return str(round(self.bottom_outer_diameter)) + "/" + str(round(self.top_outer_diameter))
            else:
                return str(round(self.bottom_outer_diameter))
        else:
            return ""

    @property
    def height(self) -> Union[np.float64, None]:
        """Height of the building block , mm."""
        if "height" in self.json:
            return self.json["height"]
        else:
            return None

    @property
    def volume(self) -> Union[np.float64, None]:
        """Volume of the building block, m³."""
        if self.type == "tubular_section":
            if self.height:

                def _calc_cone_volume(r_bottom, r_top, height):
                    """Calculate the volume of a cone frustum.
                    Source: https://mathworld.wolfram.com/ConicalFrustum.html.

                    :param r_bottom: Radius of the bottom circle, mm.
                    :param r_top: Radius of the top circle, mm.
                    :param height: Height of the cone frustum, mm.
                    :return: Volume of the cone frustum, mm³.
                    """
                    volume = pi * height / 3 * (r_bottom**2 + r_bottom * r_top + r_top**2)
                    return volume

                r_bottom_inner = self.json["bottom_outer_diameter"] / 2 - self.json["wall_thickness"]
                r_bottom_outer = self.json["bottom_outer_diameter"] / 2
                r_top_inner = self.json["top_outer_diameter"] / 2 - self.json["wall_thickness"]
                r_top_outer = self.json["top_outer_diameter"] / 2
                volume_inner_cone = _calc_cone_volume(r_bottom_inner, r_top_inner, self.json["height"])
                volume_outer_cone = _calc_cone_volume(r_bottom_outer, r_top_outer, self.json["height"])
                return (volume_outer_cone - volume_inner_cone) / 1e9
            else:
                raise ValueError("Height data is missing.")
        elif self.type == "distributed_mass":
            if self.height:
                return np.float64(round(self.json["volume_distribution"] * self.height / 1000))
            else:
                raise ValueError("Height data is missing.")
        else:
            return None

    @property
    def mass(self) -> np.float64:
        """
        Mass of the building block, kg.

        Examples
        --------
        >>> data = {
        ...     "id": np.int64(1),
        ...     "description": "",
        ...     "slug": "bb",
        ...     "alpha": np.float64(0),
        ...     "beta": np.float64(0),
        ...     "gamma": np.float64(0),
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "title": "BB_1",
        ...     "height": np.float64(0),
        ...     "mass_distribution": np.float64(np.nan),
        ...     "volume_distribution": np.float64(np.nan),
        ...     "area_distribution": np.float64(np.nan),
        ...     "c_d": np.float64(np.nan),
        ...     "c_m": np.float64(np.nan),
        ...     "sub_assembly": np.int64(1),
        ...     "projectsite_name": "Site",
        ...     "asset_name": "T01",
        ...     "subassembly_name": "SA",
        ...     "material_name": "Steel",
        ...     "youngs_modulus": np.float64(np.nan),
        ...     "density": np.float64(np.nan),
        ...     "poissons_ratio": np.float64(np.nan),
        ...     "bottom_outer_diameter": np.float64(np.nan),
        ...     "top_outer_diameter": np.float64(np.nan),
        ...     "wall_thickness": np.float64(np.nan),
        ...     "material": np.float64(np.nan),
        ...     "moment_of_inertia_x": np.float64(1.0),
        ...     "moment_of_inertia_y": np.float64(2.0),
        ...     "moment_of_inertia_z": np.float64(3.0),
        ...     "mass": np.float64(100.0),
        ... }
        >>> float(BuildingBlock(data).mass)
        100.0
        """
        if self.type == "lumped_mass":
            return self.json["mass"]
        elif self.type == "distributed_mass":
            if self.height:
                return np.float64(round(self.json["mass_distribution"] * self.height / 1000))
            else:
                raise ValueError("Height data is missing.")
        elif self.type == "tubular_section":
            if self.material:
                if self.material.density and self.volume:
                    return np.float64(round(self.volume * self.material.density, 1))
                else:
                    raise ValueError("Density or volume data is missing.")
            else:
                raise ValueError("Material data is missing.")
        else:
            raise ValueError("Unsupported building block type.")

    @property
    def moment_of_inertia(self) -> dict[str, Union[np.float64, None]]:
        """
        Moment of inertia of the building block, kg*m².

        IMPORTANT! Only works for building blocks of the type
        lumped_mass.

        Returns
        -------
        dict
            Dictionary containing the moment of inertia around the
            three axes, x, y, z.

        Examples
        --------
        >>> data = {
        ...     "id": np.int64(1),
        ...     "description": "",
        ...     "slug": "bb",
        ...     "alpha": np.float64(0),
        ...     "beta": np.float64(0),
        ...     "gamma": np.float64(0),
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "title": "BB_1",
        ...     "height": np.float64(0),
        ...     "mass_distribution": np.float64(np.nan),
        ...     "volume_distribution": np.float64(np.nan),
        ...     "area_distribution": np.float64(np.nan),
        ...     "c_d": np.float64(np.nan),
        ...     "c_m": np.float64(np.nan),
        ...     "sub_assembly": np.int64(1),
        ...     "projectsite_name": "Site",
        ...     "asset_name": "T01",
        ...     "subassembly_name": "SA",
        ...     "material_name": "Steel",
        ...     "youngs_modulus": np.float64(np.nan),
        ...     "density": np.float64(np.nan),
        ...     "poissons_ratio": np.float64(np.nan),
        ...     "bottom_outer_diameter": np.float64(np.nan),
        ...     "top_outer_diameter": np.float64(np.nan),
        ...     "wall_thickness": np.float64(np.nan),
        ...     "material": np.float64(np.nan),
        ...     "moment_of_inertia_x": np.float64(1.0),
        ...     "moment_of_inertia_y": np.float64(2.0),
        ...     "moment_of_inertia_z": np.float64(3.0),
        ...     "mass": np.float64(100.0),
        ... }
        >>> float(BuildingBlock(data).moment_of_inertia["y"])
        2.0
        """
        if self.type == "lumped_mass":
            return {
                "x": self.json["moment_of_inertia_x"],
                "y": self.json["moment_of_inertia_y"],
                "z": self.json["moment_of_inertia_z"],
            }
        else:
            return {"x": None, "y": None, "z": None}

    @property
    def outline(self) -> Union[None, tuple[list[np.float64], list[np.float64]]]:
        """
        Trace of the outlines.

        Returns
        -------
        tuple or None
            A tuple of two lists containing the x and corresponding z
            coordinates of the outline, or None if not applicable.
        """
        if self.type == "tubular_section":
            z_pos_bottom = self.position.z
            z_pos_top = self.position.z + self.json["height"]
            x_pos_bottom = self.json["bottom_outer_diameter"] / 2
            x_pos_top = self.json["top_outer_diameter"] / 2
            x = [
                x_pos_bottom,
                -x_pos_bottom,
                -x_pos_top,
                x_pos_top,
                x_pos_bottom,
            ]
            z = [z_pos_bottom, z_pos_bottom, z_pos_top, z_pos_top, z_pos_bottom]
            return x, z
        else:
            return None

    @property
    def marker(self) -> Union[None, dict[str, Union[np.float64, str]]]:
        """
        Indication for the lumped mass in the building block.

        Returns
        -------
        dict or None
            Dictionary containing the x, y, z coordinates of the
            marker and the radius of the marker, or None if not
            applicable.
        """
        if self.type == "lumped_mass":
            return {
                "x": self.position.x,
                "y": self.position.y,
                "z": self.position.z,
                "radius": np.float64(round(self.json["mass"]) / 10),
                "hovertext": "<br>".join(
                    [
                        self.title,
                        "Mass: " + str(self.json["mass"]) + " kg",
                        "x: " + str(self.position.x),
                        "y: " + str(self.position.y),
                        "z: " + str(self.position.z),
                    ]
                ),
            }
        else:
            return None

    @property
    def line(self) -> Union[None, dict[str, Union[list[np.float64], str]]]:
        """
        Line for the distributed mass in the building block.

        Returns
        -------
        dict or None
            Dictionary containing the x, y, z coordinates of the line
            and the color of the line, or None if not applicable.
        """
        if self.type == "distributed_mass" and self.height:
            return {
                "x": [self.position.x, self.position.x],
                "y": [self.position.y, self.position.y],
                "z": [self.position.z, self.position.z + self.height],
                "color": "black",
            }
        else:
            return None

    def as_dict(
        self,
    ) -> dict[str, Union[str, np.float64, dict[str, Union[np.float64, None]], None]]:
        """
        Transform data into dictionary.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "title": Name of the building block.
            - "x": X coordinate of the building block.
            - "y": Y coordinate of the building block.
            - "z": Z coordinate of the building block.
            - "OD": Outer diameter of the building block.
            - "wall_thickness": Wall thickness of the building block.
            - "height": Height of the building block.
            - "volume": Volume of the building block.
            - "mass": Mass of the building block.
            - "moment_of_inertia": Moment of inertia of the building
              block.
            - "description": Description of the building block.
        """
        return {
            "title": self.title,
            "x": self.position.x,
            "y": self.position.y,
            "z": self.position.z,
            "OD": self.diameter_str,
            "wall_thickness": self.wall_thickness,
            "height": self.height,
            "volume": self.volume,
            "mass": self.mass,
            "moment_of_inertia": self.moment_of_inertia,
            "description": self.description,
        }

    def __str__(self) -> str:
        """
        Examples
        --------
        >>> data = {
        ...     "id": np.int64(1),
        ...     "description": "",
        ...     "slug": "bb",
        ...     "alpha": np.float64(0),
        ...     "beta": np.float64(0),
        ...     "gamma": np.float64(0),
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "title": "BB_1",
        ...     "height": np.float64(0),
        ...     "mass_distribution": np.float64(np.nan),
        ...     "volume_distribution": np.float64(np.nan),
        ...     "area_distribution": np.float64(np.nan),
        ...     "c_d": np.float64(np.nan),
        ...     "c_m": np.float64(np.nan),
        ...     "sub_assembly": np.int64(1),
        ...     "projectsite_name": "Site",
        ...     "asset_name": "T01",
        ...     "subassembly_name": "SA",
        ...     "material_name": "Steel",
        ...     "youngs_modulus": np.float64(np.nan),
        ...     "density": np.float64(np.nan),
        ...     "poissons_ratio": np.float64(np.nan),
        ...     "bottom_outer_diameter": np.float64(np.nan),
        ...     "top_outer_diameter": np.float64(np.nan),
        ...     "wall_thickness": np.float64(np.nan),
        ...     "material": np.float64(np.nan),
        ...     "moment_of_inertia_x": np.float64(1.0),
        ...     "moment_of_inertia_y": np.float64(2.0),
        ...     "moment_of_inertia_z": np.float64(3.0),
        ...     "mass": np.float64(100.0),
        ... }
        >>> str(BuildingBlock(data))
        'BB_1 (lumped_mass)'
        """
        return self.title + " (" + self.type + ")"


class SubAssembly(BaseStructure):
    """Subassemblies description."""

    def __init__(
        self,
        materials: Union[pd.DataFrame, bool, np.int64, None],
        json: DataSA,
        api_object: Union[Any, None] = None,
    ) -> None:
        """
        Create an instance of the SubAssembly class with required
        parameters.

        Parameters
        ----------
        materials : pd.DataFrame or bool or np.int64 or None
            Pandas dataframe containing the material information.
        json : DataSA
            JSON data containing the subassembly information.
        api_object : Any, optional
            API object to access the building blocks.

        Examples
        --------
        >>> materials = pd.DataFrame([
        ...     {
        ...         "title": "Steel",
        ...         "slug": "steel",
        ...         "id": np.int64(1),
        ...         "description": "",
        ...         "young_modulus": np.float64(210000.0),
        ...         "density": np.float64(7850.0),
        ...         "poisson_ratio": np.float64(0.3),
        ...     }
        ... ])
        >>> data = {
        ...     "id": np.int64(1),
        ...     "title": "SA_1",
        ...     "description": "",
        ...     "slug": "sa",
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "subassembly_type": "TW",
        ...     "source": "api",
        ...     "asset": np.int64(1),
        ...     "model_definition": np.int64(1),
        ... }
        >>> sa = SubAssembly(materials, data)
        >>> sa.title
        'SA_1'
        """
        self.api = api_object
        self.id = json["id"]
        self.title = json["title"]
        self.description = json["description"]
        self.position = Position(
            x=json["x_position"],
            y=json["y_position"],
            z=json["z_position"],
            reference_system=json["vertical_position_reference_system"],
        )
        self.type = json["subassembly_type"]
        self.source = json["source"]
        self.asset = json["asset"]
        self.bb = None
        materials_df = cast(pd.DataFrame, materials)
        self.materials = [Material(cast(DataMat, m.to_dict())) for _, m in materials_df.iterrows()]

    @property
    def color(self) -> str:
        """
        Color based on subassembly type.

        Examples
        --------
        >>> materials = pd.DataFrame([
        ...     {
        ...         "title": "Steel",
        ...         "slug": "steel",
        ...         "id": np.int64(1),
        ...         "description": "",
        ...         "young_modulus": np.float64(210000.0),
        ...         "density": np.float64(7850.0),
        ...         "poisson_ratio": np.float64(0.3),
        ...     }
        ... ])
        >>> data = {
        ...     "id": np.int64(1),
        ...     "title": "SA_1",
        ...     "description": "",
        ...     "slug": "sa",
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "subassembly_type": "TW",
        ...     "source": "api",
        ...     "asset": np.int64(1),
        ...     "model_definition": np.int64(1),
        ... }
        >>> SubAssembly(materials, data).color
        'grey'
        """
        return PLOT_SETTINGS_SUBASSEMBLY[self.type]["color"]

    @property
    def building_blocks(self) -> Union[list[BuildingBlock], None]:
        """
        Building blocks of the subassembly.

        Returns
        -------
        list of BuildingBlock or None
            List of instances of building block class.

        Raises
        ------
        ValueError
            If no API configured or no building blocks found.
        """
        if self.bb:
            return self.bb
        else:
            if self.api is None:
                raise ValueError("No API configured")
            else:
                bb = self.api.get_buildingblocks(subassembly_id=str(self.id))
                if bb["exists"]:
                    bb_data = cast(pd.DataFrame, bb["data"])
                    self.bb = [
                        BuildingBlock(cast(DataBB, b.to_dict()), subassembly=self) for _, b in bb_data.iterrows()
                    ]
                    return self.bb
                else:
                    raise ValueError("No building blocks found")

    @property
    def height(self) -> np.float64:
        """Height of the subassembly."""
        height = np.float64(0.0)
        if self.building_blocks:
            for bb in self.building_blocks:
                if (
                    bb.type == "tubular_section"
                    and "grout" not in bb.title.lower()
                    and bb.height
                    and not np.isnan(bb.height)
                ):
                    height += bb.height
                else:
                    continue
        else:
            raise ValueError("No building blocks found")
        return height

    @property
    def mass(self) -> np.float64:
        """Mass of the subassembly."""
        mass = np.float64(0.0)
        if self.building_blocks:
            for bb in self.building_blocks:
                if bb.mass and not np.isnan(bb.mass):
                    mass += bb.mass
                else:
                    continue
        else:
            raise ValueError("No building blocks found")
        return mass

    @property
    def properties(self) -> dict[str, np.float64]:
        """Mass and height of the subassembly."""
        property_dict = {"mass": self.mass, "height": self.height}
        return property_dict

    @property
    def outline(self) -> tuple[list[np.float64], list[np.float64]]:
        """
        Defines the traces of the outline of the subassembly.

        Returns
        -------
        tuple
            A tuple of two lists containing the x and corresponding z
            coordinates of the outline.
        """
        building_blocks = self.building_blocks
        x = []
        z = []
        z_pos = []
        if building_blocks:
            for bb in building_blocks:
                if bb.outline:
                    z_pos.append(bb.position.z)
                    x_local, z_local = bb.outline
                    x.append(x_local)
                    z.append(z_local)
        outlines = [(x, z) for _, x, z in sorted(zip(z_pos, x, z), key=lambda pair: pair[0])]
        x_all = []
        z_all = []
        for ol in outlines:
            x_all.extend([ol[0][0], ol[0][3]])
            z_all.extend([ol[1][0], ol[1][3]])
        for ol in outlines[::-1]:
            x_all.extend([ol[0][2], ol[0][1]])
            z_all.extend([ol[1][2], ol[1][1]])
        z_absolute = [z + self.position.z for z in z_all]
        return x_all, z_absolute

    def plot(self, x_offset: np.float64 = DEFAULT_NP_FLOAT64_VALUE) -> None:
        """Plot the subassembly."""
        x0, z = self.outline
        plt.plot(
            [x + x_offset for x in x0],
            z,
            color=PLOT_SETTINGS_SUBASSEMBLY[self.type]["color"],
        )
        patches = []
        if self.building_blocks:
            for bb in self.building_blocks:
                if bb.marker:
                    marker = bb.marker
                    patches.append(
                        mpatches.Circle(
                            (
                                float(marker["x"]),
                                float(marker["z"]) + float(self.position.z),
                            ),
                            float(marker["radius"]),
                            facecolor="black",
                            alpha=0.1,
                            edgecolor="black",
                        )
                    )
                if bb.line:
                    line = bb.line
                    xs = cast(list[float], line["x"])
                    zs = cast(list[float], line["z"])
                    plt.plot(
                        [float(x) + float(x_offset) for x in xs],
                        [float(z) + float(self.position.z) for z in zs],
                        color=line["color"],
                    )
        for p in patches:
            plt.gca().add_patch(p)
            plt.ylabel("Height , mm")
            plt.axis("equal")
            plt.grid(which="both", linestyle=":")

    def plotly(
        self,
        x_offset: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
        y_offset: np.float64 = DEFAULT_NP_FLOAT64_VALUE,
    ):
        """
        Plot the subassembly.

        Parameters
        ----------
        x_offset : np.float64, optional
            Offset in the x direction.
        y_offset : np.float64, optional
            Offset in the y direction.

        Returns
        -------
        tuple
            Plotly data and layout.
        """
        x0, z = self.outline
        data = [
            go.Scattergl(
                x=[x + x_offset for x in x0],
                y=z,
                mode="lines",
                name=self.title,
                line={"color": self.color, "width": 1},
            )
        ]
        layout = go.Layout(
            scene={"aspectmode": "data"},
            yaxis={
                "title": go.layout.yaxis.Title(text="Height , mm"),
                "scaleanchor": "x",
                "scaleratio": 1,
                "type": "linear",
            },
        )
        markers: list[dict[str, Any]] = []
        if self.bb:
            for bb in self.bb:
                if bb.marker:
                    marker = bb.marker
                    marker_dict = {
                        "x": [x_offset + float(marker["x"])],
                        "y": [float(marker["z"]) + self.position.z],
                        "mode": "markers",
                        "marker": {
                            "size": [np.float64(round(float(marker["radius"]) ** (1 / 3)))],
                            "color": "grey",
                        },
                        "hovertext": marker["hovertext"],
                        "hoverinfo": "text",
                        "name": bb.title,
                    }
                    markers.append(marker_dict)
        data.extend(markers)
        return data, layout

    def as_df(self, include_absolute_postion: bool = False) -> pd.DataFrame:
        """
        Transform data into pandas dataframe.

        Parameters
        ----------
        include_absolute_postion : bool, optional
            Include absolute position of the building blocks, default
            is False.

        Returns
        -------
        pd.DataFrame
            Pandas dataframe with the building block information.
        """
        out = []
        if self.building_blocks:
            for bb in self.building_blocks:
                out.append(bb.as_dict())
        df = pd.DataFrame(out)
        df = df.set_index("title")
        df = df.sort_values("z", ascending=False)
        cols_at_end = ["description"]
        df = df[[c for c in df if c not in cols_at_end] + [c for c in cols_at_end if c in df]]
        if include_absolute_postion:
            df["absolute_position, m"] = (df["z"] + self.position.z) / 1000
        return df

    @property
    def absolute_bottom(self) -> np.float64:
        """Absolute bottom of the subassembly, m."""
        temp_df = self.as_df(include_absolute_postion=True)
        return temp_df["absolute_position, m"].iloc[-1]

    @property
    def absolute_top(self) -> np.float64:
        """Absolute top of the subassembly, m."""
        temp_df = self.as_df(include_absolute_postion=True)
        temp_df.dropna(inplace=True, how="any", axis=0)
        return np.float64(
            round(
                temp_df["absolute_position, m"].iloc[0] + temp_df["height"].iloc[0] / 1000,
                3,
            )
        )

    def _repr_html_(self) -> str:
        html_str = self.as_df()._repr_html_()  # type: ignore
        return html_str

    def __str__(self) -> str:
        """Return a string representation of the subassembly."""
        """
        Examples
        --------
        >>> materials = pd.DataFrame([
        ...     {
        ...         "title": "Steel",
        ...         "slug": "steel",
        ...         "id": np.int64(1),
        ...         "description": "",
        ...         "young_modulus": np.float64(210000.0),
        ...         "density": np.float64(7850.0),
        ...         "poisson_ratio": np.float64(0.3),
        ...     }
        ... ])
        >>> data = {
        ...     "id": np.int64(1),
        ...     "title": "SA_1",
        ...     "description": "",
        ...     "slug": "sa",
        ...     "x_position": np.float64(0),
        ...     "y_position": np.float64(0),
        ...     "z_position": np.float64(0),
        ...     "vertical_position_reference_system": "LAT",
        ...     "subassembly_type": "TW",
        ...     "source": "api",
        ...     "asset": np.int64(1),
        ...     "model_definition": np.int64(1),
        ... }
        >>> str(SubAssembly(materials, data))
        'SA_1 subassembly'
        """
        s = str(self.title) + " subassembly"
        return s
