"""Module for the base class handling the access to the Database API."""

import json
import warnings
from collections.abc import Mapping, Sequence
from typing import Any, TypedDict, Union

import numpy as np
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

from owi.metadatabase._utils.exceptions import (
    APIConnectionError,
    DataProcessingError,
    InvalidParameterError,
)
from owi.metadatabase._utils.utils import deepcompare


class PostprocessData(TypedDict):
    existance: bool
    id: Union[np.int64, None]
    response: Union[requests.Response, None]


class API:
    """Base API class handling user access information to the Database API."""

    def __init__(
        self,
        api_root: str = "https://owimetadatabase.azurewebsites.net/api/v1",
        token: Union[str, None] = None,
        uname: Union[str, None] = None,
        password: Union[str, None] = None,
        **kwargs: Any,
    ) -> None:
        """
        Create an instance of the API class with required parameters.

        Parameters
        ----------
        api_root : str, optional
            Root URL of the API endpoint, the default working database
            url is provided.
        token : str, optional
            Token to access the API.
        uname : str, optional
            Username to access the API.
        password : str, optional
            Password to access the API.
        **kwargs
            Additional parameters to pass to the API.

        Raises
        ------
        InvalidParameterError
            If header format is invalid or if neither header, token,
            nor username and password are defined.

        Examples
        --------
        >>> api = API(api_root="https://example", token="test")
        >>> api.api_root
        'https://example'
        """
        self.api_root = api_root
        self.uname = uname
        self.password = password
        self.auth = None
        self.header = None
        if "header" in kwargs:
            self.header = kwargs["header"]
            if self.header and isinstance(self.header, dict) and "Authorization" in self.header:
                if not self.header["Authorization"].startswith("Token "):
                    if self.header["Authorization"].startswith("token "):
                        self.header = {"Authorization": f"Token {self.header['Authorization'][6:]}"}
                    elif self.header["Authorization"].startswith("token") or self.header["Authorization"].startswith(
                        "Token"
                    ):
                        self.header = {"Authorization": f"Token {self.header['Authorization'][5:]}"}
                    else:
                        self.header = {"Authorization": f"Token {self.header['Authorization']}"}
            else:
                raise InvalidParameterError(
                    "If you provide a header directly, \
                    the header must contain the 'Authorization' \
                    key with the value starting with 'Token'."
                )
        elif token:
            self.header = {"Authorization": f"Token {token}"}
        elif self.uname and self.password:
            self.auth = HTTPBasicAuth(self.uname, self.password)
        else:
            raise InvalidParameterError("Either header, token or user name and password must be defined.")

    def __eq__(self, other: object) -> bool:
        """
        Compare two instances of the API class.

        Parameters
        ----------
        other : object
            Another instance of the API class or a dictionary.

        Returns
        -------
        bool
            True if the instances are equal, False otherwise.

        Raises
        ------
        AssertionError
            If comparison is not possible due to incompatible types.

        Examples
        --------
        >>> api_1 = API(api_root="https://example", token="test")
        >>> api_2 = API(api_root="https://example", token="test")
        >>> api_1 == api_2
        True
        """
        if not isinstance(other, (API, dict)):
            return NotImplemented
        if isinstance(other, type(self)):
            comp = deepcompare(self, other)
            assert comp[0], comp[1]
        elif isinstance(other, dict):
            comp = deepcompare(self.__dict__, other)
            assert comp[0], comp[1]
        else:
            raise AssertionError("Comparison is not possible due to incompatible types!")
        return comp[0]

    def send_request(
        self,
        url_data_type: str,
        url_params: Mapping[str, Union[str, float, int, Sequence[Union[str, float, int]], None]],
    ) -> requests.Response:
        """
        Handle sending appropriate request.

        Handles sending appropriate request according to the type of
        authentication.

        Parameters
        ----------
        url_data_type : str
            Type of the data we want to request (according to database
            model).
        url_params : Mapping
            Parameters to send with the request to the database.

        Returns
        -------
        requests.Response
            An instance of the Response object.

        Raises
        ------
        InvalidParameterError
            If neither header nor username and password are defined.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> from unittest import mock
        >>> response = SimpleNamespace(status_code=200, reason="OK")
        >>> with mock.patch("requests.get", return_value=response):
        ...     api = API(api_root="https://example", token="test")
        ...     resp = api.send_request("/projects", {})
        >>> resp is response
        True
        """
        if self.header is not None:
            response = requests.get(
                url=self.api_root + url_data_type,
                headers=self.header,
                params=url_params,
            )
        else:
            if self.uname is None or self.password is None:
                e = "Either self.header or self.uname and self.password must be defined."
                raise InvalidParameterError(e)
            else:
                response = requests.get(
                    url=self.api_root + url_data_type,
                    auth=self.auth,
                    params=url_params,
                )
        return response

    @staticmethod
    def check_request_health(resp: requests.Response) -> None:
        """
        Check status code of the response and provide details.

        Checks status code of the response to request and provides
        details if unexpected.

        Parameters
        ----------
        resp : requests.Response
            Instance of the Response object.

        Raises
        ------
        APIConnectionError
            If response status code is not 200.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> ok = SimpleNamespace(status_code=200, reason="OK")
        >>> API.check_request_health(ok)
        """
        if resp.status_code != 200:
            raise APIConnectionError(
                message=f"Error {resp.status_code}.\n{resp.reason}",
                response=resp,
            )

    @staticmethod
    def output_to_df(response: requests.Response) -> pd.DataFrame:
        """
        Transform output to Pandas dataframe.

        Parameters
        ----------
        response : requests.Response
            Raw output of the sent request.

        Returns
        -------
        pd.DataFrame
            Pandas dataframe of the data from the output.

        Raises
        ------
        DataProcessingError
            If failed to decode JSON from API response.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> resp = SimpleNamespace(text='[{"a": 1}]')
        >>> int(API.output_to_df(resp)["a"].iloc[0])
        1
        """
        try:
            data = json.loads(response.text)
        except Exception as err:
            raise DataProcessingError("Failed to decode JSON from API response") from err
        return pd.DataFrame(data)

    @staticmethod
    def postprocess_data(df: pd.DataFrame, output_type: str) -> PostprocessData:
        """
        Process dataframe information to extract additional data.

        Processes dataframe information to extract the necessary
        additional data.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe of the output data.
        output_type : str
            Expected type (amount) of the data extracted.

        Returns
        -------
        PostprocessData
            Dictionary of the additional data extracted.

        Raises
        ------
        InvalidParameterError
            If more than one record was returned for 'single' output
            type, or if output type is not 'single' or 'list'.

        Examples
        --------
        >>> df = pd.DataFrame({"id": [1]})
        >>> int(API.postprocess_data(df, "single")["id"])
        1
        """
        if output_type == "single":
            if df.__len__() == 0:
                exists = False
                project_id = None
            elif df.__len__() == 1:
                exists = True
                project_id = df["id"].iloc[0]
            else:
                raise InvalidParameterError("More than one project site was returned, check search criteria.")
            data_add: PostprocessData = {
                "existance": exists,
                "id": project_id,
                "response": None,
            }
        elif output_type == "list":
            exists = df.__len__() != 0
            data_add: PostprocessData = {
                "existance": exists,
                "id": None,
                "response": None,
            }
        else:
            raise InvalidParameterError("Output type must be either 'single' or 'list', not " + output_type + ".")
        return data_add

    @staticmethod
    def validate_data(df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """
        Validate the data extracted from the database.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe of the output data.
        data_type : str
            Type of the data we want to request (according to database
            model).

        Returns
        -------
        pd.DataFrame
            Dataframe with corrected data.

        Examples
        --------
        >>> df = pd.DataFrame()
        >>> API.validate_data(df, "subassemblies").empty
        True
        """
        z_sa_mp = {"min": -100000, "max": -10000}
        z_sa_tp = {"min": -20000, "max": -1000}
        z_sa_tw = {"min": 1000, "max": 100000}
        sa_type = ["TW", "TP", "MP"]
        z = [z_sa_tw, z_sa_tp, z_sa_mp]
        if data_type == "subassemblies":
            if df.__len__() == 0:
                return df
            for i, sat in enumerate(sa_type):
                cond_small_units = (df["subassembly_type"] == sat) & (df["z_position"] < z[i]["min"])
                cond_big_units = (df["subassembly_type"] == sat) & (df["z_position"] > z[i]["max"])
                if df[cond_small_units].__len__() > 0:
                    df.loc[cond_small_units, "z_position"] = df.loc[cond_small_units, "z_position"] / 1e3
                    warnings.warn(
                        f"The value of z location for {df.loc[cond_small_units | cond_big_units, 'title'].values} \
                        might be wrong or in wrong units! There will be an attempt to correct the units.",
                        stacklevel=2,
                    )
                if df[cond_big_units].__len__() > 0:
                    df.loc[cond_big_units, "z_position"] = df.loc[cond_big_units, "z_position"] * 1e3
                    warnings.warn(
                        f"The value of z location for {df.loc[cond_small_units | cond_big_units, 'title'].values} \
                        might be wrong or in wrong units! There will be an attempt to correct the units.",
                        stacklevel=2,
                    )
        return df

    def process_data(
        self,
        url_data_type: str,
        url_params: Mapping[str, Union[str, float, int, Sequence[Union[str, float, int]], None]],
        output_type: str,
    ) -> tuple[pd.DataFrame, PostprocessData]:
        """
        Process output data according to specified request parameters.

        Parameters
        ----------
        url_data_type : str
            Type of the data we want to request (according to database
            model).
        url_params : Mapping
            Parameters to send with the request to the database.
        output_type : str
            Expected type (amount) of the data extracted.

        Returns
        -------
        tuple
            A tuple of dataframe with the requested data and
            additional data from postprocessing.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> from unittest import mock
        >>> response = SimpleNamespace(text="[]", status_code=200, reason="OK")
        >>> api = API(api_root="https://example", token="test")
        >>> with mock.patch.object(API, "send_request", return_value=response):
        ...     df, info = api.process_data("projects", {}, "list")
        >>> df.empty
        True
        >>> info["existance"]
        False
        """
        resp = self.send_request(url_data_type, url_params)
        self.check_request_health(resp)
        df = self.output_to_df(resp)
        df = self.validate_data(df, url_data_type)
        df_add = self.postprocess_data(df, output_type)
        # Add the response object to the returned dictionary so tests can inspect it
        df_add["response"] = resp
        return df, df_add
