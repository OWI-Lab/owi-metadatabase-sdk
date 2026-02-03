"""Module to connect to the database API to retrieve and operate on locations data."""

from typing import Any, Union

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from owi.metadatabase.io import API


class LocationsAPI(API):
    """
    Class to connect to the location data API with methods to retrieve data.

    A number of methods are provided to query the database via the
    owimetadatabase API. In the majority of cases, the methods return a
    dataframe based on the URL parameters provided. The methods are written
    such that a number of mandatory URL parameters are required (see
    documentation of the methods). The URL parameters can be expanded with
    Django-style additional filtering arguments (e.g.
    ``location__title__icontains="BB"``) as optional keyword arguments.
    Knowledge of the Django models is required for this (see
    ``owimetadatabase`` code).
    """

    def __init__(
        self,
        api_subdir: str = "/locations/",
        **kwargs: Any,
    ) -> None:
        """
        Create an instance of the LocationsAPI class with required
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
        >>> api = LocationsAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> api.api_root.endswith("/locations/")
        True
        """
        super().__init__(**kwargs)
        self.api_root = self.api_root + api_subdir

    def get_projectsites(self, **kwargs: Any) -> dict[str, Union[pd.DataFrame, bool, np.int64, None]]:
        """
        Get all available projects.

        Parameters
        ----------
        **kwargs
            Additional parameters to pass to the API.

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
                >>> api = LocationsAPI(
                ...     api_root="https://example",
                ...     header={"Authorization": "Token test"},
                ... )
                >>> df = pd.DataFrame({"id": [1]})
                >>> with mock.patch.object(
                ...     LocationsAPI,
                ...     "process_data",
                ...     return_value=(df, {"existance": True}),
                ... ):
                ...     out = api.get_projectsites()
                >>> out["exists"]
                True
        """
        url_params = {}  # type: dict[str, str]
        url_params = {**url_params, **kwargs}
        url_data_type = "projectsites"
        output_type = "list"
        df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"data": df, "exists": df_add["existance"]}

    def get_projectsite_detail(
        self, projectsite: str, **kwargs: Any
    ) -> dict[str, Union[pd.DataFrame, bool, np.int64, None]]:
        """
        Get details for a specific projectsite.

        Parameters
        ----------
        projectsite : str
            Title of the projectsite.
        **kwargs
            Additional parameters to pass to the API.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "id": ID of the selected project site.
            - "data": Pandas dataframe with the location data for each
              projectsite.
            - "exists": Boolean indicating whether matching records
              are found.

        Examples
        --------
                >>> from unittest import mock
                >>> api = LocationsAPI(
                ...     api_root="https://example",
                ...     header={"Authorization": "Token test"},
                ... )
                >>> df = pd.DataFrame({"id": [1]})
                >>> with mock.patch.object(
                ...     LocationsAPI,
                ...     "process_data",
                ...     return_value=(df, {"existance": True, "id": 1}),
                ... ):
                ...     out = api.get_projectsite_detail("Site")
                >>> out["id"]
                1
        """
        url_params = {"projectsite": projectsite}
        url_params = {**url_params, **kwargs}
        url_data_type = "projectsites"
        output_type = "single"
        df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"id": df_add["id"], "data": df, "exists": df_add["existance"]}

    def get_assetlocations(
        self, projectsite: Union[str, None] = None, **kwargs: Any
    ) -> dict[str, Union[pd.DataFrame, bool, list[bool], np.int64, None]]:
        """
        Get all available asset locations.

        Get all available asset locations for all projectsites or a
        specific projectsite.

        Parameters
        ----------
        projectsite : str, optional
            String with the projectsite title (e.g. "Nobelwind").
        **kwargs
            Additional parameters to pass to the API.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "data": Pandas dataframe with the location data for each
              location in the projectsite.
            - "exists": Boolean indicating whether matching records
              are found.

        Examples
        --------
                >>> from unittest import mock
                >>> api = LocationsAPI(
                ...     api_root="https://example",
                ...     header={"Authorization": "Token test"},
                ... )
                >>> df = pd.DataFrame({"id": [1]})
                >>> with mock.patch.object(
                ...     LocationsAPI,
                ...     "process_data",
                ...     return_value=(df, {"existance": True}),
                ... ):
                ...     out = api.get_assetlocations(projectsite="Site")
                >>> out["exists"]
                True
        """
        url_params = {}  # type: dict[str, str]
        url_params = {**url_params, **kwargs}
        if projectsite:
            url_params["projectsite__title"] = projectsite
        url_data_type = "assetlocations"
        if "assetlocations" in url_params and isinstance(url_params["assetlocations"], list):
            df = []
            df_add = {"existance": []}
            for assetlocation in url_params["assetlocations"]:
                output_type = "single"
                url_params["assetlocation"] = assetlocation
                df_temp, df_add_temp = self.process_data(url_data_type, url_params, output_type)
                df.append(df_temp)
                df_add["existance"].append(df_add_temp["existance"])
            df = pd.concat(df)
        else:
            output_type = "list"
            df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"data": df, "exists": df_add["existance"]}

    def get_assetlocation_detail(
        self,
        assetlocation: str,
        projectsite: Union[None, str] = None,
        **kwargs: Any,
    ) -> dict[str, Union[pd.DataFrame, bool, np.int64, None]]:
        """
        Get a selected turbine.

        Parameters
        ----------
        assetlocation : str
            Title of the asset location (e.g. "BBK05").
        projectsite : str, optional
            Name of the projectsite (e.g. "Nobelwind").
        **kwargs
            Additional parameters to pass to the API.

        Returns
        -------
        dict
            Dictionary with the following keys:

            - "id": ID of the selected projectsite site.
            - "data": Pandas dataframe with the location data for the
              individual location.
            - "exists": Boolean indicating whether a matching location
              is found.

        Examples
        --------
                >>> from unittest import mock
                >>> api = LocationsAPI(
                ...     api_root="https://example",
                ...     header={"Authorization": "Token test"},
                ... )
                >>> df = pd.DataFrame({"id": [1]})
                >>> with mock.patch.object(
                ...     LocationsAPI,
                ...     "process_data",
                ...     return_value=(df, {"existance": True, "id": 1}),
                ... ):
                ...     out = api.get_assetlocation_detail("T01")
                >>> out["id"]
                1
        """
        if projectsite is None:
            url_params = {"assetlocation": assetlocation}
        else:
            url_params = {
                "projectsite": projectsite,
                "assetlocation": assetlocation,
            }
        url_params = {**url_params, **kwargs}
        url_data_type = "assetlocations"
        output_type = "single"
        df, df_add = self.process_data(url_data_type, url_params, output_type)
        return {"id": df_add["id"], "data": df, "exists": df_add["existance"]}

    def plot_assetlocations(self, return_fig: bool = False, **kwargs: Any) -> Union[go.Figure, None]:
        """
        Retrieve asset locations and generate a Plotly plot.

        Retrieves asset locations and generates a Plotly plot to show
        them.

        Parameters
        ----------
        return_fig : bool, optional
            Boolean indicating whether to return the figure, default
            is False.
        **kwargs
            Keyword arguments for the search (see
            ``get_assetlocations``).

        Returns
        -------
        plotly.graph_objects.Figure or None
            Plotly figure object with selected asset locations plotted
            on OpenStreetMap tiles (if requested) or nothing.

        Raises
        ------
        ValueError
            If no asset locations found for the given parameters.

        Examples
        --------
        >>> from unittest import mock
        >>> api = LocationsAPI(
        ...     api_root="https://example",
        ...     header={"Authorization": "Token test"},
        ... )
        >>> data = pd.DataFrame(
        ...     {
        ...         "northing": [51.5],
        ...         "easting": [2.8],
        ...         "title": ["T01"],
        ...         "projectsite_name": ["Site"],
        ...         "description": [""],
        ...     }
        ... )
        >>> with mock.patch.object(
        ...     LocationsAPI,
        ...     "get_assetlocations",
        ...     return_value={"exists": True, "data": data},
        ... ):
        ...     fig = api.plot_assetlocations(return_fig=True)
        >>> fig is not None
        True
        """
        assetlocations_data = self.get_assetlocations(**kwargs)
        if assetlocations_data["exists"]:
            assetlocations = assetlocations_data["data"]
        else:
            raise ValueError(
                f"No asset locations found for the given parameters: {kwargs}. \
                Please check for typos or if it is expected to exists."
            )
        fig = px.scatter_mapbox(
            assetlocations,
            lat="northing",
            lon="easting",
            hover_name="title",
            hover_data=["projectsite_name", "description"],
            zoom=9.6,
            height=500,
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        if return_fig:
            return fig
        else:
            fig.show()
            return None
