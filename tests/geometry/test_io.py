from typing import Any, Union
from unittest import mock

import pandas as pd
import pandas.testing as pd_testing
import pytest

from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.geometry.processing import OWTs


@pytest.mark.parametrize(
    "params, data_subassemblies",
    [
        ({}, "empty"),
        ({"projectsite": "Nobelwind"}, "project"),
        ({"assetlocation": "BBK01"}, "asset"),
        ({"subassembly_type": "TW"}, "subassembly"),
        (
            {"projectsite": "Nobelwind", "assetlocation": "BBK01"},
            "project_asset",
        ),
        (
            {"projectsite": "Nobelwind", "subassembly_type": "TW"},
            "project_subassembly",
        ),
        (
            {"assetlocation": "BBK01", "subassembly_type": "TW"},
            "asset_subassembly",
        ),
        (
            {
                "projectsite": "Nobelwind",
                "assetlocation": "BBK01",
                "subassembly_type": "TW",
            },
            "project_asset_subassembly",
        ),
    ],
    indirect=["data_subassemblies"],
)
def test_get_subassemblies(
    api_root: str,
    header: dict[str, str],
    mock_requests_get_subassemblies: mock.Mock,
    params: Union[dict[str, Union[str, int]], None],
    data_subassemblies: Union[dict[str, str], None],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    data_ = api_test.get_subassemblies(**params)  # type: ignore
    expected_data = pd.DataFrame(data_subassemblies)
    assert isinstance(data_["data"], pd.DataFrame)
    assert isinstance(data_["exists"], bool)
    assert data_["exists"]
    pd_testing.assert_frame_equal(data_["data"], expected_data)


@pytest.mark.parametrize(
    "params, data_buildingblocks",
    [
        ({}, "empty"),
        ({"projectsite": "Nobelwind"}, "project"),
        ({"assetlocation": "BBK01"}, "asset"),
        ({"subassembly_type": "TW"}, "subassembly"),
        ({"subassembly_id": str(235)}, "id"),
        (
            {"projectsite": "Nobelwind", "assetlocation": "BBK01"},
            "project_asset",
        ),
        (
            {"projectsite": "Nobelwind", "subassembly_type": "TW"},
            "project_subassembly",
        ),
        (
            {"assetlocation": "BBK01", "subassembly_type": "TW"},
            "asset_subassembly",
        ),
        (
            {
                "projectsite": "Nobelwind",
                "assetlocation": "BBK01",
                "subassembly_type": "TW",
            },
            "project_asset_subassembly",
        ),
        (
            {"projectsite": "Nobelwind", "subassembly_id": 235},
            "project_id",
        ),
        (
            {"assetlocation": "BBK01", "subassembly_id": 235},
            "asset_id",
        ),
        (
            {"subassembly_type": "TW", "subassembly_id": 235},
            "subassembly_id",
        ),
        (
            {
                "projectsite": "Nobelwind",
                "subassembly_type": "TW",
                "subassembly_id": 235,
            },
            "project_subassembly_id",
        ),
        (
            {
                "assetlocation": "BBK01",
                "subassembly_type": "TW",
                "subassembly_id": 235,
            },
            "asset_subassembly_id",
        ),
        (
            {
                "projectsite": "Nobelwind",
                "assetlocation": "BBK01",
                "subassembly_type": "TW",
                "subassembly_id": 235,
            },
            "project_asset_subassembly_id",
        ),
        (
            {
                "projectsite": "Nobelwind",
                "assetlocation": "BBK01",
                "subassembly_id": 235,
            },
            "project_asset_id",
        ),
    ],
    indirect=["data_buildingblocks"],
)
def test_get_buildingblocks(
    api_root: str,
    header: dict[str, str],
    mock_requests_get_buildingblocks: mock.Mock,
    params: Union[dict[str, Union[str, int]], None],
    data_buildingblocks: Union[dict[str, str], None],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    data_ = api_test.get_buildingblocks(**params)  # type: ignore
    expected_data = pd.DataFrame(data_buildingblocks)
    assert isinstance(data_["data"], pd.DataFrame)
    assert isinstance(data_["exists"], bool)
    assert data_["exists"]
    pd_testing.assert_frame_equal(data_["data"], expected_data)


def test_get_materials(api_root: str, header: dict[str, str], mock_requests_get_advanced: mock.Mock) -> None:
    api_test = GeometryAPI(api_root, header=header)
    data = api_test.get_materials()
    assert isinstance(data["data"], pd.DataFrame)
    assert isinstance(data["exists"], bool)
    assert data["exists"]


def test_get_owt_geometry_processor(api_test: Any, owts_init: OWTs, mock_requests_for_proc: mock.Mock) -> None:
    processor = api_test.get_owt_geometry_processor(turbines=["AAA01", "AAB02"])
    assert processor == owts_init


def test_get_modeldefinition_id_multiple_definitions(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    model_defs = pd.DataFrame({"id": [1, 2], "title": ["A", "B"]})
    location = pd.DataFrame({"projectsite_name": ["Site"]})
    with (
        mock.patch.object(
            api_test.loc_api,
            "get_assetlocation_detail",
            return_value={"exists": True, "data": location},
        ),
        mock.patch.object(
            GeometryAPI,
            "get_model_definitions",
            return_value={"exists": True, "data": model_defs},
        ),
        pytest.raises(ValueError),
    ):
        api_test.get_modeldefinition_id(assetlocation="T01")


def test_get_modeldefinition_id_missing_definition(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    model_defs = pd.DataFrame({"id": [1], "title": ["A"]})
    with (
        mock.patch.object(
            GeometryAPI,
            "get_model_definitions",
            return_value={"exists": True, "data": model_defs},
        ),
        pytest.raises(ValueError),
    ):
        api_test.get_modeldefinition_id(
            projectsite="Site",
            model_definition="B",
        )


def test_get_modeldefinition_id_single_match(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    model_defs = pd.DataFrame({"id": [1, 2], "title": ["A", "B"]})
    with mock.patch.object(
        GeometryAPI,
        "get_model_definitions",
        return_value={"exists": True, "data": model_defs},
    ):
        result = api_test.get_modeldefinition_id(
            projectsite="Site",
            model_definition="A",
        )
    assert result == {"id": 1, "multiple_modeldef": True}


def test_get_subassemblies_model_definition_missing_scope(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    with pytest.raises(ValueError):
        api_test.get_subassemblies(model_definition="Model")


def test_get_subassemblies_model_definition_not_found(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    with (
        mock.patch.object(
            GeometryAPI,
            "get_modeldefinition_id",
            return_value={"id": None},
        ),
        pytest.raises(ValueError),
    ):
        api_test.get_subassemblies(
            projectsite="Site",
            model_definition="Model",
        )


def test_get_modeldefinition_id_missing_location(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    with (
        mock.patch.object(
            api_test.loc_api,
            "get_assetlocation_detail",
            return_value={"exists": False},
        ),
        pytest.raises(ValueError),
    ):
        api_test.get_modeldefinition_id(assetlocation="T01")


def test_get_modeldefinition_id_no_model_definitions(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    location = pd.DataFrame({"projectsite_name": ["Site"]})
    with (
        mock.patch.object(
            api_test.loc_api,
            "get_assetlocation_detail",
            return_value={"exists": True, "data": location},
        ),
        mock.patch.object(
            GeometryAPI,
            "get_model_definitions",
            return_value={"exists": False, "data": pd.DataFrame()},
        ),
        pytest.raises(ValueError),
    ):
        api_test.get_modeldefinition_id(assetlocation="T01")


def test_get_modeldefinition_id_duplicate_match(
    api_root: str,
    header: dict[str, str],
) -> None:
    api_test = GeometryAPI(api_root, header=header)
    model_defs = pd.DataFrame({"id": [1, 2], "title": ["A", "A"]})
    with (
        mock.patch.object(
            GeometryAPI,
            "get_model_definitions",
            return_value={"exists": True, "data": model_defs},
        ),
        pytest.raises(ValueError),
    ):
        api_test.get_modeldefinition_id(
            projectsite="Site",
            model_definition="A",
        )
