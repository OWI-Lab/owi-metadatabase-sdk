"""Module to connect to the database API to retrieve and operate on geometry data."""

# mypy: ignore-errors

import warnings
from contextlib import contextmanager
from typing import Union, cast

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from owi.metadatabase.geometry.processing import OWT, OWTs
from owi.metadatabase.geometry.structures import DataSA, SubAssembly
from owi.metadatabase.io import API
from owi.metadatabase.locations.io import LocationsAPI


class GeometryAPI(API):
    """Class to connect to the geometry data API with methods to retrieve data."""

    def __init__(
        self,
        api_subdir: str = "/geometry/userroutes/",
        **kwargs,
    ) -> None:
        """
        Create an instance of the GeometryAPI class with required
        parameters.

        Parameters
        ----------
        api_subdir : str, optional
            Subdirectory of the API endpoint url for specific type of
            data.
        **kwargs
            Additional parameters to pass to the API (see the base
            class).

        Examples
        --------
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> api.api_root.endswith("/geometry/userroutes/")
        True
        """
        super().__init__(**kwargs)
        self.loc_api = LocationsAPI(**kwargs)
        self.api_root = self.api_root + api_subdir

    @contextmanager
    def _temp_api_root(self, new_api_root: str):
        """
        Temporarily change the api_root.

        Parameters
        ----------
        new_api_root : str
            Temporary API root URL.

        Examples
        --------
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> original = api.api_root
        >>> with api._temp_api_root("https://tmp"):
        ...     api.api_root
        'https://tmp'
        >>> api.api_root == original
        True
        """
        original_root = self.api_root
        self.api_root = new_api_root
        try:
            yield
        finally:
            self.api_root = original_root

    def get_model_definitions(
        self,
        projectsite: Union[str, None] = None,
    ) -> dict[str, Union[pd.DataFrame, bool, np.int64, None]]:
        """
        Get all relevant model definitions.

        Parameters
        ----------
        projectsite : str, optional
            Title of the projectsite.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "data": Pandas dataframe with the model definitions
            - "exists": Boolean indicating whether matching records
              are found

        Examples
        --------
                >>> from unittest import mock
                >>> api = GeometryAPI(
                ...     api_root="https://example",
                ...     header={"Authorization": "Token test"},
                ... )
                >>> df = pd.DataFrame({"id": [1]})
                >>> with mock.patch.object(
                ...     GeometryAPI,
                ...     "process_data",
                ...     return_value=(df, {"existance": True}),
                ... ):
                ...     out = api.get_model_definitions(projectsite="Site")
                >>> out["exists"]
                True
        """
        url_params = {}
        if projectsite is not None:
            url_params["site"] = projectsite
        url_data_type = "modeldefinitions"
        output_type = "list"
        with self._temp_api_root(self.api_root.replace("userroutes", "routes")):
            df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"data": df, "exists": df_add["existance"]}

    def get_modeldefinition_id(
        self,
        assetlocation: Union[str, None] = None,
        projectsite: Union[str, None] = None,
        model_definition: Union[str, None] = None,
    ) -> dict[str, Union[int, np.int64, bool, None]]:
        """
        Get the ID of a model definition.

        Either the asset location or the project site must be specified.

        Parameters
        ----------
        assetlocation : str, optional
            Title of the asset location.
        projectsite : str, optional
            Title of the projectsite.
        model_definition : str, optional
            Title of the model definition.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "id": ID of the specified model definition
            - "multiple_modeldef": Boolean indicating whether there
              are multiple model definitions for the asset location
              in general

        Raises
        ------
        ValueError
            If at least one of assetlocation or projectsite is not
            specified, if no location found, if no model definitions
            found, if multiple model definitions found without
            specification, or if specified model definition not found.

        Examples
        --------
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> api.get_modeldefinition_id()  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: At least either of the related ... must be specified!
        """
        if assetlocation is None and projectsite is None:
            raise ValueError("At least either of the related `assetlocation` or `projectsite` must be specified!")

        result = {}
        if projectsite is None:
            if assetlocation is None:
                raise ValueError("Asset location must be specified when projectsite is None.")
            location_data = self.loc_api.get_assetlocation_detail(assetlocation=assetlocation)
            if location_data["exists"]:
                location = cast(pd.DataFrame, location_data["data"])
            else:
                raise ValueError(f"No location found for asset {assetlocation}.")
            projectsite = location["projectsite_name"].loc[0]
        model_definitions_data = self.get_model_definitions(projectsite=projectsite)
        if model_definitions_data["exists"]:
            model_definitions = cast(pd.DataFrame, model_definitions_data["data"])
        else:
            raise ValueError(f"No model definitions found for project site {projectsite}.")
        if model_definition is None and len(model_definitions) > 1:
            raise ValueError(
                f"Multiple model definitions found for project site {projectsite}. Please specify which one to use."
            )
        if model_definition is None:
            model_definition_id = model_definitions["id"].values[0]
            result["id"] = model_definition_id
            result["multiple_modeldef"] = False
        else:
            matching_definitions = model_definitions[model_definitions["title"] == model_definition]
            if matching_definitions.empty:
                raise ValueError(f"Model definition '{model_definition}' not found for project site {projectsite}.")
            if len(matching_definitions) > 1:
                raise ValueError(
                    f"Multiple model definitions found for '{model_definition}' in project site {projectsite}.\n"
                    f"Please check the data consistency."
                )
            model_definition_id = matching_definitions["id"].values[0]
            result["id"] = model_definition_id
            result["multiple_modeldef"] = len(model_definitions) > 1
        return result

    def get_subassemblies(
        self,
        projectsite: Union[str, None] = None,
        assetlocation: Union[str, None] = None,
        subassembly_type: Union[str, None] = None,
        model_definition: Union[str, None] = None,
    ) -> dict[str, Union[pd.DataFrame, bool, np.int64, None]]:
        """
        Get all relevant structure subassemblies.

        If you specify a model definition, you also must specify either
        the projectsite or the asset location.

        Parameters
        ----------
        projectsite : str, optional
            Title of the projectsite.
        assetlocation : str, optional
            Title of the asset location.
        subassembly_type : str, optional
            Type of the subassembly.
        model_definition : str, optional
            Title of the model definition.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "data": Pandas dataframe with the location data for each
              project
            - "exists": Boolean indicating whether matching records
              are found

        Raises
        ------
        ValueError
            If model definition specified without projectsite or
            assetlocation, or if specified model definition not found.

        Examples
        --------
        >>> from unittest import mock
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> df = pd.DataFrame({"id": [1]})
        >>> with mock.patch.object(
        ...     GeometryAPI,
        ...     "process_data",
        ...     return_value=(df, {"existance": True}),
        ... ):
        ...     out = api.get_subassemblies(projectsite="Site")
        >>> out["exists"]
        True
        """
        url_params = {}
        func_args = {}
        if projectsite is not None:
            url_params["asset__projectsite__title"] = projectsite
            func_args["projectsite"] = projectsite
        if assetlocation is not None:
            url_params["asset__title"] = assetlocation
            func_args["assetlocation"] = assetlocation
        if subassembly_type is not None:
            url_params["subassembly_type"] = subassembly_type
        if model_definition is not None:
            if projectsite is not None or assetlocation is not None:
                func_args["model_definition"] = model_definition
                modeldef_data = self.get_modeldefinition_id(**func_args)
                if modeldef_data["id"] is not None:
                    url_params["model_definition"] = str(modeldef_data["id"])
                else:
                    raise ValueError(
                        f"No model definition {model_definition} found for project site {projectsite} "
                        f"or asset location {assetlocation}."
                    )
            else:
                raise ValueError(
                    "If you specify a model definition, you also must specify either "
                    "the projectsite or the asset location!"
                )
        url_data_type = "subassemblies"
        output_type = "list"
        df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"data": df, "exists": df_add["existance"]}

    def get_buildingblocks(
        self,
        projectsite: Union[str, None] = None,
        assetlocation: Union[str, None] = None,
        subassembly_type: Union[str, None] = None,
        subassembly_id: Union[int, np.int64, None] = None,
    ) -> dict[str, Union[pd.DataFrame, bool, np.int64, None]]:
        """
        Get all relevant building blocks.

        Parameters
        ----------
        projectsite : str, optional
            Title of the projectsite.
        assetlocation : str, optional
            Title of the asset location.
        subassembly_type : str, optional
            Type of the subassemblies (e.g. 'MP', 'TW', 'TP').
        subassembly_id : int or np.int64, optional
            ID of the subassembly.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "data": Pandas dataframe with the location data for each
              project
            - "exists": Boolean indicating whether matching records
              are found

        Examples
        --------
                >>> from unittest import mock
                >>> api = GeometryAPI(
                ...     api_root="https://example",
                ...     header={"Authorization": "Token test"},
                ... )
                >>> df = pd.DataFrame({"id": [1]})
                >>> with mock.patch.object(
                ...     GeometryAPI,
                ...     "process_data",
                ...     return_value=(df, {"existance": True}),
                ... ):
                ...     out = api.get_buildingblocks(projectsite="Site")
                >>> out["exists"]
                True
        """
        url_params = {}
        if projectsite is not None:
            url_params["sub_assembly__asset__projectsite__title"] = projectsite
        if assetlocation is not None:
            url_params["sub_assembly__asset__title"] = assetlocation
        if subassembly_type is not None:
            url_params["sub_assembly__subassembly_type"] = subassembly_type
        if subassembly_id is not None:
            url_params["sub_assembly__id"] = str(subassembly_id)
        url_data_type = "buildingblocks"
        output_type = "list"
        df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"data": df, "exists": df_add["existance"]}

    def get_materials(
        self,
    ) -> dict[str, Union[pd.DataFrame, bool, np.int64, None]]:
        """
        Get all the materials of building blocks.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "data": Pandas dataframe with the location data for each
              project
            - "exists": Boolean indicating whether matching records
              are found

        Examples
        --------
                >>> from unittest import mock
                >>> api = GeometryAPI(
                ...     api_root="https://example",
                ...     header={"Authorization": "Token test"},
                ... )
                >>> df = pd.DataFrame({"id": [1]})
                >>> with mock.patch.object(
                ...     GeometryAPI,
                ...     "process_data",
                ...     return_value=(df, {"existance": True}),
                ... ):
                ...     out = api.get_materials()
                >>> out["exists"]
                True
        """
        url_params = {}  # type: dict[str, str]
        url_data_type = "materials"
        output_type = "list"
        df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"data": df, "exists": df_add["existance"]}

    def get_subassembly_objects(
        self,
        turbine: str,
        subassembly: Union[str, None] = None,
        model_definition_id: Union[int, np.int64, None] = None,
    ) -> dict[str, SubAssembly]:
        """
        Get all subassemblies for a given turbine, divided by type.

        Parameters
        ----------
        turbine : str
            Turbine title.
        subassembly : str, optional
            Sub-assembly type (e.g. 'MP', 'TW', 'TP').
        model_definition_id : int or np.int64, optional
            ID of the model definition to filter the subassemblies.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "TW": SubAssembly object for the tower
            - "TP": SubAssembly object for the transition piece
            - "MP": SubAssembly object for the monopile

        Raises
        ------
        ValueError
            If no subassemblies found for the turbine or if no
            materials found in the database.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> from unittest import mock
        >>> materials = pd.DataFrame(
        ...     [
        ...         {
        ...             "title": "Steel",
        ...             "slug": "steel",
        ...             "id": np.int64(1),
        ...             "description": "",
        ...             "young_modulus": np.float64(210000.0),
        ...             "density": np.float64(7850.0),
        ...             "poisson_ratio": np.float64(0.3),
        ...         }
        ...     ]
        ... )
        >>> item = {
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
        >>> response = SimpleNamespace(
        ...     status_code=200,
        ...     reason="OK",
        ...     json=lambda: [item],
        ... )
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> with mock.patch.object(
        ...     GeometryAPI,
        ...     "send_request",
        ...     return_value=response,
        ... ), mock.patch.object(
        ...     GeometryAPI,
        ...     "get_materials",
        ...     return_value={"exists": True, "data": materials},
        ... ):
        ...     out = api.get_subassembly_objects("T01")
        >>> sorted(out.keys())
        ['TW']
        """
        url_data_type = "subassemblies"
        url_params = {"asset__title": turbine}
        if subassembly is not None:
            url_params["subassembly_type"] = subassembly
        if model_definition_id is not None:
            url_params["model_definition"] = str(model_definition_id)
        resp = self.send_request(url_data_type, url_params)
        self.check_request_health(resp)
        if not resp.json():
            raise ValueError("No subassemblies found for " + str(turbine))

        material_data = self.get_materials()
        if material_data["exists"]:
            materials = material_data["data"]
        else:
            raise ValueError("No materials found in the database.")

        subassemblies = {}
        for item in resp.json():
            subassembly_type = item["subassembly_type"]
            subassembly_obj = SubAssembly(materials, item, api_object=self)
            if subassembly_type in subassemblies:
                if not isinstance(subassemblies[subassembly_type], list):
                    subassemblies[subassembly_type] = [subassemblies[subassembly_type]]
                subassemblies[subassembly_type].append(subassembly_obj)
            else:
                subassemblies[subassembly_type] = subassembly_obj

        return subassemblies

    def _check_if_need_modeldef(self, subassemblies, turbine):
        """
        Check if the user needs to specify a model definition.

        Parameters
        ----------
        subassemblies : pd.DataFrame
            Subassemblies dataframe.
        turbine : str
            Turbine title.

        Raises
        ------
        ValueError
            If multiple model definitions found for turbine.

        Examples
        --------
        >>> df = pd.DataFrame({"subassembly_type": ["TW", "TW"]})
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> api._check_if_need_modeldef(df, "T01")  # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        ValueError: Multiple model definitions found for turbine T01...
        """
        sa_list_length = len(list(subassemblies["subassembly_type"].values))
        sa_unique_list_length = len(set(list(subassemblies["subassembly_type"].values)))  # noqa: C414
        if sa_list_length > sa_unique_list_length:
            raise ValueError(
                f"Multiple model definitions found for turbine {turbine}. Please specify which one to use."
            )

    def get_owt_geometry_processor(
        self,
        turbines: Union[str, list[str]],
        model_definition: Union[str, None] = None,
        tower_base: Union[float, list[float], None] = None,
        monopile_head: Union[float, list[float], None] = None,
    ) -> OWTs:
        """
        Return the required processing class.

        Will return data even if some turbines have issues given that at
        least one is fully OK.

        Parameters
        ----------
        turbines : str or list of str
            Title(s) of the turbines.
        model_definition : str, optional
            Title of the model definition.
        tower_base : float or list of float, optional
            Height(s) of the tower base.
        monopile_head : float or list of float, optional
            Height(s) of the monopile head.

        Returns
        -------
        OWTs
            Object containing information about all the requested
            turbines.

        Raises
        ------
        ValueError
            If no materials found in the database or if all turbines
            encounter processing errors.

        Examples
        --------
        >>> from unittest import mock
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> materials = pd.DataFrame({"id": [1]})
        >>> location = pd.DataFrame({"projectsite_name": ["Site"]})
        >>> subassemblies = pd.DataFrame({"subassembly_type": ["TW"]})
        >>> def _make_owt(*args, **kwargs):
        ...     return "owt"
        >>> def _make_owts(turbines, owts):
        ...     return {"turbines": turbines, "owts": owts}
        >>> with mock.patch.object(
        ...     GeometryAPI,
        ...     "get_materials",
        ...     return_value={"exists": True, "data": materials},
        ... ), mock.patch.object(
        ...     api.loc_api,
        ...     "get_assetlocation_detail",
        ...     return_value={"exists": True, "data": location},
        ... ), mock.patch.object(
        ...     GeometryAPI,
        ...     "get_subassemblies",
        ...     return_value={"exists": True, "data": subassemblies},
        ... ), mock.patch.object(
        ...     GeometryAPI,
        ...     "_check_if_need_modeldef",
        ...     return_value=None,
        ... ), mock.patch(
        ...     "geometry.io.OWT",
        ...     _make_owt,
        ... ), mock.patch(
        ...     "geometry.io.OWTs",
        ...     _make_owts,
        ... ):
        ...     out = api.get_owt_geometry_processor("T01")
        >>> out["turbines"]
        ['T01']
        """
        materials_data = self.get_materials()
        if materials_data["exists"]:
            materials = cast(pd.DataFrame, materials_data["data"])
        else:
            raise ValueError("No materials found in the database.")
        owts = []
        successful_turbines = []
        errors = []
        turbines = [turbines] if isinstance(turbines, str) else turbines
        if not isinstance(tower_base, list) and not isinstance(monopile_head, list):
            tower_base = [tower_base] * len(turbines)  # type: ignore
            monopile_head = [monopile_head] * len(turbines)  # type: ignore
        for i, turbine in enumerate(turbines):
            try:
                location_data = self.loc_api.get_assetlocation_detail(assetlocation=turbine)
                if location_data["exists"]:
                    location = cast(pd.DataFrame, location_data["data"])
                else:
                    raise ValueError(f"No location found for turbine {turbine}.")
                projectsite = location["projectsite_name"].loc[0]
                subassemblies_data = self.get_subassemblies(
                    projectsite=projectsite,
                    assetlocation=turbine,
                    model_definition=model_definition,
                )
                if subassemblies_data["exists"]:
                    subassemblies = subassemblies_data["data"]
                    self._check_if_need_modeldef(subassemblies, turbine)
                else:
                    raise ValueError(
                        f"No subassemblies found for turbine {turbine}. Please check model definition or database data."
                    )
                owts.append(
                    OWT(
                        self,
                        materials,
                        subassemblies,
                        location,
                        tower_base[i] if isinstance(tower_base, list) else tower_base,
                        (monopile_head[i] if isinstance(monopile_head, list) else monopile_head),
                    )
                )
                successful_turbines.append(turbine)
            except ValueError as e:
                errors.append(str(e))
        if errors:
            if successful_turbines:
                warnings.warn(
                    f"There were some errors during processing the request. "
                    f"But some turbines were processed successfully: {', '.join(successful_turbines)}."
                    f"\nErrors:\n" + "\n".join(errors),
                    stacklevel=2,
                )
            else:
                raise ValueError("\n".join(errors))
        return OWTs(successful_turbines, owts)

    def get_monopile_pyles(
        self,
        projectsite,
        assetlocation,
        cutoff_point=np.nan,
        model_definition: Union[str, None] = None,
    ):
        """
        Return a dataframe with the monopile geometry.

        Uses the mudline as reference.

        Parameters
        ----------
        projectsite : str
            Name of the project site.
        assetlocation : str
            Name of the wind turbine location.
        cutoff_point : float, optional
            Elevation of the load application point in (mLAT) above the
            mudline.
        model_definition : str, optional
            Title of the model definition.

        Returns
        -------
        pd.DataFrame
            Dataframe with the monopile geometry.

        Raises
        ------
        ValueError
            If no subassemblies or location found for turbine.

        Examples
        --------
        >>> from unittest import mock
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> bbs = pd.DataFrame(
        ...     [
        ...         {
        ...             "z_position": 0,
        ...             "material_name": "Steel",
        ...             "density": 7850.0,
        ...             "wall_thickness": 20.0,
        ...             "bottom_outer_diameter": 6.0,
        ...             "top_outer_diameter": 6.0,
        ...             "youngs_modulus": 210000.0,
        ...             "poissons_ratio": 0.3,
        ...         },
        ...         {
        ...             "z_position": -1000,
        ...             "material_name": "Steel",
        ...             "density": 7850.0,
        ...             "wall_thickness": 20.0,
        ...             "bottom_outer_diameter": 6.0,
        ...             "top_outer_diameter": 6.0,
        ...             "youngs_modulus": 210000.0,
        ...             "poissons_ratio": 0.3,
        ...         },
        ...     ]
        ... )
        >>> sas = pd.DataFrame({"z_position": [-50000]})
        >>> location = pd.DataFrame({"elevation": [30.0]})
        >>> with mock.patch.object(
        ...     GeometryAPI,
        ...     "get_buildingblocks",
        ...     return_value={"exists": True, "data": bbs},
        ... ), mock.patch.object(
        ...     GeometryAPI,
        ...     "get_subassemblies",
        ...     return_value={"exists": True, "data": sas},
        ... ), mock.patch.object(
        ...     GeometryAPI,
        ...     "_check_if_need_modeldef",
        ...     return_value=None,
        ... ), mock.patch.object(
        ...     api.loc_api,
        ...     "get_assetlocation_detail",
        ...     return_value={"exists": True, "data": location},
        ... ):
        ...     pile = api.get_monopile_pyles("Site", "T01")
        >>> "Depth from [m]" in pile.columns
        True
        """
        # Retrieve the monopile cans
        bbs = self.get_buildingblocks(
            projectsite=projectsite,
            assetlocation=assetlocation,
            subassembly_type="MP",
        )
        # Retrieve the monopile subassembly
        sas = self.get_subassemblies(
            projectsite=projectsite,
            assetlocation=assetlocation,
            subassembly_type="MP",
            model_definition=model_definition,
        )
        if sas["exists"]:
            subassemblies = cast(pd.DataFrame, sas["data"])
            self._check_if_need_modeldef(subassemblies, assetlocation)
        else:
            raise ValueError(
                f"No subassemblies found for turbine {assetlocation}. Please check model definition or database data."
            )
        # Water depth
        location_data = self.loc_api.get_assetlocation_detail(assetlocation=assetlocation, projectsite=projectsite)
        if location_data["exists"]:
            location = cast(pd.DataFrame, location_data["data"])
            water_depth = location["elevation"].values[0]
        else:
            raise ValueError(
                f"No location found for turbine {assetlocation} and hence no water depth can be retrieved."
            )

        # Calculate the pile penetration
        sas_df = cast(pd.DataFrame, sas["data"])
        toe_depth_lat = sas_df["z_position"].iloc[0]
        penetration = -((1e-3 * toe_depth_lat) - water_depth)

        # Create the pile for subsequent response analysis
        pile = pd.DataFrame()

        bbs_df = cast(pd.DataFrame, bbs["data"])
        for index in range(1, len(bbs_df)):
            prev_row = bbs_df.iloc[index - 1]
            row = bbs_df.iloc[index]
            pile.loc[index, "Depth to [m]"] = penetration - 1e-3 * float(prev_row.at["z_position"])
            pile.loc[index, "Depth from [m]"] = penetration - 1e-3 * float(row.at["z_position"])
            pile.loc[index, "Pile material"] = str(row.at["material_name"])
            pile.loc[index, "Pile material submerged unit weight [kN/m3]"] = 1e-2 * float(row.at["density"]) - 10
            pile.loc[index, "Wall thickness [mm]"] = float(row.at["wall_thickness"])
            pile.loc[index, "Diameter [m]"] = (
                1e-3 * 0.5 * (float(row.at["bottom_outer_diameter"]) + float(row.at["top_outer_diameter"]))
            )
            pile.loc[index, "Youngs modulus [GPa]"] = float(row.at["youngs_modulus"])
            pile.loc[index, "Poissons ratio [-]"] = float(row.at["poissons_ratio"])

        pile.sort_values("Depth from [m]", inplace=True)
        pile.reset_index(drop=True, inplace=True)

        # Cut off at the mudline
        if not np.isnan(cutoff_point):
            pile = pile.loc[pile["Depth to [m]"] > cutoff_point].reset_index(drop=True)
            pile.loc[0, "Depth from [m]"] = cutoff_point

        return pile

    def plot_turbines(
        self,
        turbines: Union[list[str], str],
        figures_per_line: int = 5,
        return_fig: bool = False,
        model_definition: Union[str, None] = None,
    ) -> Union[go.Figure, None]:
        """
        Plot turbines' frontal geometry.

        Parameters
        ----------
        turbines : str or list of str
            Title(s) of the turbines.
        figures_per_line : int, optional
            Number of figures per line, default is 5.
        return_fig : bool, optional
            Boolean indicating whether to return the figure, default
            is False.
        model_definition : str, optional
            Title of the model definition.

        Returns
        -------
        plotly.graph_objects.Figure or None
            Plotly figure object with selected turbines front profiles
            (if requested) or nothing.

        Raises
        ------
        ValueError
            If no materials or subassemblies found in the database.

        Examples
        --------
        >>> from unittest import mock
        >>> class _StubSubassembly:
        ...     def __init__(self, *args, **kwargs):
        ...         self.building_blocks = []
        ...     def plotly(self):
        ...         layout = {
        ...             "scene": {},
        ...             "yaxis": {
        ...                 "title": {"text": "Height , mm"},
        ...                 "scaleanchor": "x",
        ...                 "scaleratio": 1,
        ...                 "type": "linear",
        ...             },
        ...         }
        ...         return [], layout
        >>> api = GeometryAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> materials = pd.DataFrame({"id": [1]})
        >>> subassemblies = pd.DataFrame({"subassembly_type": ["TW"]})
        >>> with mock.patch.object(
        ...     GeometryAPI,
        ...     "get_materials",
        ...     return_value={"exists": True, "data": materials},
        ... ), mock.patch.object(
        ...     GeometryAPI,
        ...     "get_subassemblies",
        ...     return_value={"exists": True, "data": subassemblies},
        ... ), mock.patch.object(
        ...     GeometryAPI,
        ...     "_check_if_need_modeldef",
        ...     return_value=None,
        ... ), mock.patch(
        ...     "geometry.io.SubAssembly",
        ...     _StubSubassembly,
        ... ):
        ...     fig = api.plot_turbines(["T01"], return_fig=True)
        >>> fig is not None
        True
        """
        materials_data = self.get_materials()
        if materials_data["exists"]:
            materials = materials_data["data"]
        else:
            raise ValueError("No materials found in the database.")
        turbines = [turbines] if isinstance(turbines, str) else turbines
        if len(turbines) > figures_per_line:
            n_rows = len(turbines) // figures_per_line + 1
            n_cols = figures_per_line
            rows = [i for i in range(1, n_rows + 1) for _ in range(n_cols)]
            cols = [i for _ in range(n_rows) for i in range(1, n_cols + 1)]
        else:
            n_rows = 1
            n_cols = len(turbines)
            rows = [1 for _ in range(n_cols)]
            cols = list(range(1, n_cols + 1))
        autosize = not len(turbines) < 3
        fig = make_subplots(n_rows, n_cols, subplot_titles=turbines)
        for i, turbine in enumerate(turbines):
            subassemblies_data = self.get_subassemblies(
                assetlocation=turbine,
                model_definition=model_definition,
            )
            if subassemblies_data["exists"]:
                subassemblies = cast(pd.DataFrame, subassemblies_data["data"])
                self._check_if_need_modeldef(subassemblies, turbine)
            else:
                raise ValueError(
                    f"No subassemblies found for turbine {turbine}. Please check model definition or database data."
                )
            for _, sa in subassemblies.iterrows():
                subassembly = SubAssembly(materials, cast(DataSA, sa.to_dict()), api_object=self)
                subassembly.building_blocks  # noqa: B018
                plotly_data = subassembly.plotly()
                for k in range(len(plotly_data[0])):
                    fig.add_trace(plotly_data[0][k], row=rows[i], col=cols[i])
            plotly_layout = plotly_data[1]
            if i > 0:
                plotly_layout["scene" + str(i + 1)] = plotly_layout["scene"]
                plotly_layout["yaxis" + str(i + 1)] = plotly_layout["yaxis"]
                plotly_layout["yaxis" + str(i + 1)]["scaleanchor"] = "x" + str(i + 1)
                plotly_layout.pop("scene")
                plotly_layout.pop("yaxis")
                plotly_layout["yaxis" + str(i + 1)].pop("title")
            fig.update_layout(plotly_layout, autosize=autosize)
        if return_fig:
            return fig
        else:
            fig.show()
