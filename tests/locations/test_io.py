from typing import cast
from unittest import mock

import numpy as np
import pandas as pd
import pytest

from owi.metadatabase.locations.io import LocationsAPI


def test_get_projectsites(api_root: str, header: dict[str, str], mock_requests_get_advanced: mock.Mock) -> None:
    api_test = LocationsAPI(api_root, header=header)
    data = api_test.get_projectsites()
    assert isinstance(data["data"], pd.DataFrame)
    assert isinstance(data["exists"], bool)
    assert data["exists"]


def test_get_projectsite_detail(
    api_root: str,
    header: dict[str, str],
    mock_requests_get_projectsite_detail: mock.Mock,
) -> None:
    api_test = LocationsAPI(api_root, header=header)
    data = api_test.get_projectsite_detail(projectsite="Nobelwind")
    assert isinstance(data["id"], np.int64)
    assert isinstance(data["data"], pd.DataFrame)
    assert isinstance(data["exists"], bool)
    assert data["id"] == 239
    assert data["exists"]


def test_get_assetlocations_single(
    api_root: str,
    header: dict[str, str],
    mock_requests_get_assetlocations: mock.Mock,
) -> None:
    api_test = LocationsAPI(api_root, header=header)
    data = api_test.get_assetlocations(projectsite="Nobelwind")
    assert isinstance(data["data"], pd.DataFrame)
    assert isinstance(data["exists"], bool)
    assert data["exists"]
    assert data["data"].__len__() == 2
    assert data["data"]["project"][0] == "Nobelwind"
    assert data["data"]["project"][1] == "Nobelwind"


def test_get_assetlocations_all(
    api_root: str,
    header: dict[str, str],
    mock_requests_get_assetlocations: mock.Mock,
) -> None:
    api_test = LocationsAPI(api_root, header=header)
    data = api_test.get_assetlocations()
    assert isinstance(data["data"], pd.DataFrame)
    assert isinstance(data["exists"], bool)
    assert data["exists"]
    assert data["data"].__len__() == 3
    assert data["data"]["project"][0] == "Nobelwind"
    assert data["data"]["project"][1] == "Nobelwind"
    assert data["data"]["project"][2] == "Another"


def test_get_assetlocation_detail(
    api_root: str,
    header: dict[str, str],
    mock_requests_get_projectsite_detail: mock.Mock,
) -> None:
    api_test = LocationsAPI(api_root, header=header)
    data = api_test.get_assetlocation_detail(projectsite="Nobelwind", assetlocation="BBK01")
    assert isinstance(data["id"], np.int64)
    assert isinstance(data["data"], pd.DataFrame)
    assert isinstance(data["exists"], bool)
    assert data["id"] == 239
    assert data["exists"]


def test_get_assetlocations_list_branch(api_root: str, header: dict[str, str]) -> None:
    api_test = LocationsAPI(api_root, header=header)
    df_1 = pd.DataFrame({"project": ["Nobelwind"], "title": ["BBK01"]})
    df_2 = pd.DataFrame({"project": ["Nobelwind"], "title": ["BBK02"]})
    with mock.patch.object(
        LocationsAPI,
        "process_data",
        side_effect=[(df_1, {"existance": True}), (df_2, {"existance": True})],
    ):
        data = api_test.get_assetlocations(assetlocations=["BBK01", "BBK02"])
    assert data["exists"] == [True, True]
    data_df = cast(pd.DataFrame, data["data"])
    assert list(data_df["title"]) == ["BBK01", "BBK02"]


def test_plot_assetlocations_raises_without_data(api_root: str, header: dict[str, str]) -> None:
    api_test = LocationsAPI(api_root, header=header)
    with (
        mock.patch.object(
            LocationsAPI,
            "get_assetlocations",
            return_value={"exists": False, "data": pd.DataFrame()},
        ),
        pytest.raises(ValueError),
    ):
        api_test.plot_assetlocations(return_fig=True)
