import warnings

import pandas as pd
import pandas.testing as pd_testing
import pytest

from owi.metadatabase.geometry.processing import OWT


class TestOWT:
    def test_init(self, owt, owt_init, mock_requests_sa_get_bb):
        assert owt == owt_init

    @pytest.mark.parametrize(
        "idx, df_set_tube_true",
        [
            ("tp", 0),
            ("mp", 1),
            ("tw", 2),
        ],
        indirect=["df_set_tube_true"],
    )
    def test_set_df_structure(self, owt, idx, df_set_tube_true, mock_requests_sa_get_bb):
        df = owt.set_df_structure(idx)
        pd_testing.assert_frame_equal(df, df_set_tube_true)

    @pytest.mark.parametrize(
        "idx, df_proc_tube_true",
        [
            ("tp", 0),
            ("mp", 1),
            ("tw", 2),
        ],
        indirect=["df_proc_tube_true"],
    )
    def test_process_structure_geometry(self, owt, idx, df_proc_tube_true, mock_requests_sa_get_bb):
        df = owt.process_structure_geometry(idx)
        pd_testing.assert_frame_equal(df, df_proc_tube_true)

    def test_process_rna(self, owt, df_rna_true, mock_requests_sa_get_bb):
        owt.process_rna()
        pd_testing.assert_frame_equal(owt.rna, df_rna_true)

    @pytest.mark.parametrize(
        "idx, df_set_lump_mass_true",
        [
            ("TP", 0),
            ("TW", 1),
        ],
        indirect=["df_set_lump_mass_true"],
    )
    def test_set_df_appurtenances(self, owt, idx, df_set_lump_mass_true, mock_requests_sa_get_bb):
        df = owt.set_df_appurtenances(idx)
        pd_testing.assert_frame_equal(df, df_set_lump_mass_true)

    @pytest.mark.parametrize(
        "idx, df_proc_lump_mass_true",
        [
            ("TP", 0),
            ("TW", 1),
        ],
        indirect=["df_proc_lump_mass_true"],
    )
    def test_process_lumped_masses(self, owt, idx, df_proc_lump_mass_true, mock_requests_sa_get_bb):
        df = owt.process_lumped_masses(idx)
        pd_testing.assert_frame_equal(df, df_proc_lump_mass_true)

    @pytest.mark.parametrize(
        "idx, df_set_distr_true",
        [
            ("TP", 0),
            ("grout", 1),
        ],
        indirect=["df_set_distr_true"],
    )
    def test_set_df_distributed_appurtenances(self, owt, idx, df_set_distr_true, mock_requests_sa_get_bb):
        df = owt.set_df_distributed_appurtenances(idx)
        pd_testing.assert_frame_equal(df, df_set_distr_true)

    @pytest.mark.parametrize(
        "idx, df_proc_distr_true",
        [
            ("TP", 0),
            ("grout", 1),
        ],
        indirect=["df_proc_distr_true"],
    )
    def test_process_distributed_lumped_masses(self, owt, idx, df_proc_distr_true, mock_requests_sa_get_bb):
        df = owt.process_distributed_lumped_masses(idx)
        pd_testing.assert_frame_equal(df, df_proc_distr_true)

    @pytest.mark.parametrize(
        "opt, df_proc_struct_true",
        [
            ("full", 0),
            ("TW", 1),
            ("TP", 2),
            ("MP", 3),
        ],
        indirect=["df_proc_struct_true"],
    )
    def test_process_structure(self, owt, opt, df_proc_struct_true, mock_requests_sa_get_bb):
        owt.process_structure(opt)
        assert owt._init_proc
        attr = [
            "rna",
            "tower",
            "transition_piece",
            "monopile",
            "tw_lumped_mass",
            "tp_lumped_mass",
            "mp_lumped_mass",
            "tp_distributed_mass",
            "mp_distributed_mass",
            "grout",
        ]
        for i, v in enumerate(attr):
            attr_val = getattr(owt, v)
            if attr_val is not None:
                pd_testing.assert_frame_equal(attr_val, df_proc_struct_true[i])
            else:
                assert attr_val == df_proc_struct_true[i]

    def test_can_adjust_properties(self, owt, can, mock_requests_sa_get_bb):
        owt.process_structure("full")
        series_adjusted = OWT.can_adjust_properties(owt.transition_piece.iloc[0])
        pd_testing.assert_series_equal(series_adjusted, can)

    @pytest.mark.parametrize(
        "pos, can_mod",
        [
            ["bottom", 0],
            ["top", 1],
        ],
        indirect=["can_mod"],
    )
    def test_can_modification(self, owt, pos, can_mod, mock_requests_sa_get_bb):
        owt.process_structure("full")
        tp = owt.transition_piece
        dff = tp[tp["Elevation from [mLAT]"] > 7.5] if pos == "bottom" else tp[tp["Elevation to [mLAT]"] < 7.5]
        df = owt.can_modification(dff.copy(), 7.5, position=pos)
        pd_testing.assert_frame_equal(df, can_mod)

    def test_assembly_tp_mp(self, owt, assembled_tp_mp, mock_requests_sa_get_bb):
        owt.process_structure("full")
        owt.assembly_tp_mp()
        assert owt._init_spec_part
        pd_testing.assert_frame_equal(owt.substructure, assembled_tp_mp[0])
        pd_testing.assert_frame_equal(owt.tp_skirt, assembled_tp_mp[1])

    def test_assembly_full_structure(self, owt, assembled_full, mock_requests_sa_get_bb):
        owt.process_structure("full")
        owt.assembly_tp_mp()
        owt.assembly_full_structure()
        assert owt._init_spec_full
        pd_testing.assert_frame_equal(owt.full_structure, assembled_full)

    def test_extend_dfs_sets_subassembly(self, owt, mock_requests_sa_get_bb):
        owt.process_structure("full")
        owt.extend_dfs()
        assert set(owt.tower["Subassembly"].unique()) == {"TW"}
        assert set(owt.transition_piece["Subassembly"].unique()) == {"TP"}
        assert set(owt.monopile["Subassembly"].unique()) == {"MP"}
        assert owt._init_spec_part
        assert owt._init_spec_full

    def test_transform_monopile_geometry(self, owt, mock_requests_sa_get_bb):
        cutoff_point = -1_000_000.0
        pile = owt.transform_monopile_geometry(cutoff_point=cutoff_point)
        assert "Elevation from [m]" in pile.columns
        assert pile.iloc[0]["Elevation from [m]"] == cutoff_point

    def test_transform_monopile_geometry_missing(self, owt):
        owt.mp_sub_assemblies = None
        with pytest.raises(ValueError):
            owt.transform_monopile_geometry()

    def test_getattribute_warns_on_unprocessed_access(self, owt):
        with warnings.catch_warnings(record=True) as recorded:
            warnings.simplefilter("always")
            _ = owt.tower
            _ = owt.full_structure
        messages = [str(item.message) for item in recorded]
        assert any("process_structure()" in msg for msg in messages)
        assert any("assembly_tp_mp()" in msg for msg in messages)


class TestOWTs:
    def test_init(self, owts, owts_init):
        assert owts == owts_init

    def test__concat_list(self, data, owts):
        dict_ = data["geo"]["process_tube"][2]
        owts.tower = [
            pd.DataFrame(dict_).set_index("title"),
            pd.DataFrame(dict_).set_index("title"),
        ]
        owts._concat_list(["tower"])
        dict__ = {k: [*v, *v] for k, v in dict_.items()}
        df = pd.DataFrame(dict__).set_index("title")
        pd_testing.assert_frame_equal(owts.tower, df)

    def test_process_structures(self, owts, owts_true):
        owts.process_structures()
        owts_true["_init"] = True
        assert owts._init
        assert owts == owts_true

    def test_select_owt(self, owts, owt):
        turb_1 = owts.select_owt(0)
        turb_2 = owts.select_owt("AAB02")
        assert turb_1 == owt
        assert turb_2 == owt
