"""Module containing the processing functions for the geometry data."""

# mypy: ignore-errors

import typing
import warnings
from copy import deepcopy
from typing import Any, Union, cast

import numpy as np
import pandas as pd

from owi.metadatabase._utils.utils import deepcompare
from owi.metadatabase.geometry.structures import DataSA, SubAssembly

# warnings.simplefilter("always")
# warnings.formatwarning = custom_formatwarning


ATTR_PROC = [
    "pile_toe",
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
ATTR_SPEC = ["full_structure", "tp_skirt", "substructure"]
ATTR_FULL = [
    "all_tubular_structures",
    "all_distributed_mass",
    "all_lumped_mass",
    "all_turbines",
]


class OWT:
    """Class to process the geometry data of a single OWT.

    :param api: API object used to call get_* methods.
    :param materials: Pandas dataframe with the materials data.
    :param sub_assemblies: Dictionary of the subassemblies.
    :param tw_sub_assemblies: Pandas dataframe with the tower subassemblies data for a given turbine.
    :param tp_sub_assemblies: Pandas dataframe with the transition piece subassemblies data for a given turbine.
    :param mp_sub_assemblies: Pandas dataframe with the monopile subassemblies data for a given turbine.
    :param tower_base: Elevation of the OWT tower base in mLAT.
    :param pile_head: Elevation of the pile head in mLAT.
    :param water_depth: Water depth in mLAT.
    :param pile_toe: Elevation of the pile toe in mLAT.
    :param rna: Pandas dataframe with the RNA data.
    :param tower: Pandas dataframe with the tower data.
    :param transition_piece: Pandas dataframe with the transition piece data.
    :param monopile: Pandas dataframe with the monopile data.
    :param tw_lumped_mass: Pandas dataframe with the lumped masses data for the tower.
    :param tp_lumped_mass: Pandas dataframe with the lumped masses data for the transition piece.
    :param mp_lumped_mass: Pandas dataframe with the lumped masses data for the monopile.
    :param tp_distributed_mass: Pandas dataframe with the distributed masses data for the transition piece.
    :param mp_distributed_mass: Pandas dataframe with the distributed masses data for the monopile.
    :param grout: Pandas dataframe with the grout data.
    :param full_structure: Pandas dataframe with the full structure data.
    :param tp_skirt: Pandas dataframe with the transition piece skirt data.
    :param substructure: Pandas dataframe with the substructure data.
    """

    _init_proc: bool
    _init_spec_part: bool
    _init_spec_full: bool
    api: Any
    materials: pd.DataFrame
    sub_assemblies: dict[str, SubAssembly]
    tw_sub_assemblies: Union[pd.DataFrame, None]
    tp_sub_assemblies: Union[pd.DataFrame, None]
    mp_sub_assemblies: Union[pd.DataFrame, None]
    tower_base: Union[np.float64, float, None]
    pile_head: Union[np.float64, float, None]
    water_depth: np.float64
    pile_toe: Union[np.float64, float, None]
    rna: Union[pd.DataFrame, None]
    tower: Union[pd.DataFrame, None]
    transition_piece: Union[pd.DataFrame, None]
    monopile: Union[pd.DataFrame, None]
    tw_lumped_mass: Union[pd.DataFrame, None]
    tp_lumped_mass: Union[pd.DataFrame, None]
    mp_lumped_mass: Union[pd.DataFrame, None]
    tp_distributed_mass: Union[pd.DataFrame, None]
    mp_distributed_mass: Union[pd.DataFrame, None]
    grout: Union[pd.DataFrame, None]
    full_structure: Union[pd.DataFrame, None]
    tp_skirt: Union[pd.DataFrame, None]
    substructure: Union[pd.DataFrame, None]

    def __init__(
        self,
        api: Any,
        materials: Union[pd.DataFrame, bool, np.int64, None],
        subassemblies: Union[pd.DataFrame, bool, np.int64, None],
        location: Union[pd.DataFrame, bool, np.int64, None],
        tower_base: Union[np.float64, float, None] = None,
        pile_head: Union[np.float64, float, None] = None,
    ) -> None:
        """
        Create an instance of the OWT class with required parameters.

        Parameters
        ----------
        api : Any
            API object used to call get_* methods.
        materials : pd.DataFrame or bool or np.int64 or None
            Pandas dataframe with the materials data.
        subassemblies : pd.DataFrame or bool or np.int64 or None
            Pandas dataframe with the subassemblies data for a given
            turbine.
        location : pd.DataFrame or bool or np.int64 or None
            Pandas dataframe with the location data for a given
            turbine.
        tower_base : np.float64, optional
            Elevation of the OWT tower base in mLAT.
        pile_head : np.float64, optional
            Elevation of the pile head in mLAT.

        Examples
        --------
        >>> from contextlib import ExitStack
        >>> from unittest import mock
        >>> location = pd.DataFrame({"elevation": [30.0]})
        >>> def _set_subassemblies(self, subassemblies):
        ...     self.sub_assemblies = {}
        >>> def _set_members(self):
        ...     return None
        >>> with mock.patch.object(
        ...     OWT,
        ...     "_set_subassemblies",
        ...     _set_subassemblies,
        ... ), mock.patch.object(OWT, "_set_members", _set_members):
        ...     owt = OWT(
        ...         api=object(),
        ...         materials=pd.DataFrame(),
        ...         subassemblies=pd.DataFrame(),
        ...         location=location,
        ...     )
        >>> float(owt.water_depth)
        30.0
        """
        self._init_proc = False
        self._init_spec_part = False
        self._init_spec_full = False
        self.api = api
        materials_df = cast(pd.DataFrame, materials)
        subassemblies_df = cast(pd.DataFrame, subassemblies)
        location_df = cast(pd.DataFrame, location)
        self.materials = materials_df
        self._set_subassemblies(subassemblies_df)
        self.tw_sub_assemblies = None
        self.tp_sub_assemblies = None
        self.mp_sub_assemblies = None
        self._set_members()
        for attr in ATTR_PROC:
            setattr(self, attr, None)
        for attr in ATTR_SPEC:
            setattr(self, attr, None)
        self.water_depth = np.float64(location_df["elevation"].values[0])
        if not tower_base or not pile_head:
            if "TW" in self.sub_assemblies:
                self.tower_base = self.sub_assemblies["TW"].absolute_bottom
            elif "TP" in self.sub_assemblies:
                self.tower_base = self.sub_assemblies["TP"].absolute_top
            else:
                self.tower_base = None
            if "MP" in self.sub_assemblies:
                self.pile_head = self.sub_assemblies["MP"].absolute_top
            else:
                self.pile_head = None
        else:
            self.tower_base = tower_base
            self.pile_head = pile_head

    def _set_subassemblies(self, subassemblies: pd.DataFrame) -> None:
        """
        Create a dictionary containing the subassemblies of the OWT.

        Parameters
        ----------
        subassemblies : pd.DataFrame
            Pandas dataframe with the subassemblies data for a given
            turbine.
        """
        subassemblies_types = [sa["subassembly_type"] for _, sa in subassemblies.iterrows()]
        subassemblies_list = [
            SubAssembly(self.materials, cast(DataSA, sa.to_dict()), api_object=self.api)
            for _, sa in subassemblies.iterrows()
        ]
        self.sub_assemblies = dict(zip(subassemblies_types, subassemblies_list))

    def _set_members(self) -> None:
        """
        Identify and store each part of the support structure.

        Identifies and stores in separate data frames each part of the
        support structure (tower=TW, transition piece=TP, monopile=MP).
        """
        for k, v in self.sub_assemblies.items():
            if k == "TW":
                self.tw_sub_assemblies = v.as_df()
            if k == "TP":
                self.tp_sub_assemblies = v.as_df()
            if k == "MP":
                self.mp_sub_assemblies = v.as_df()

    def set_df_structure(self, idx: str) -> pd.DataFrame:
        """
        Calculate and/or convert geometrical data of subassemblies.

        Calculates and/or converts geometrical data of subassemblies
        from the database.

        Parameters
        ----------
        idx : str
            Possible index to identify corresponding subassembly.

        Returns
        -------
        pd.DataFrame
            Dataframe containing geometry data from database with z in
            mLAT system.

        Raises
        ------
        ValueError
            If subassembly data not found or unknown index.
        """
        cols = [
            "OD",
            "height",
            "mass",
            "volume",
            "wall_thickness",
            "x",
            "y",
            "z",
        ]
        if idx == "tw":
            if self.tw_sub_assemblies is None:
                raise ValueError("Tower subassembly data not found.")
            df_index = self.tw_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.tw_sub_assemblies.loc[df_index, cols])
            depth_to = self.tower_base + df.z * 1e-3
            depth_from = depth_to + df.height * 1e-3
        elif idx == "tp":
            if self.tp_sub_assemblies is None:
                raise ValueError("Transition piece subassembly data not found.")
            # We don't take into account the grout, this element will be modelled as a distributed lumped mass.
            df_index = (self.tp_sub_assemblies.index.str.contains(idx)) & (
                ~self.tp_sub_assemblies.index.str.contains("grout")
            )
            df = deepcopy(self.tp_sub_assemblies.loc[df_index, cols])
            bottom_tp = self.tower_base - df["height"].sum() * 1e-3
            depth_to = bottom_tp + df.z * 1e-3
            depth_from = depth_to + df.height * 1e-3
        elif idx == "mp":
            if self.mp_sub_assemblies is None:
                raise ValueError("Monopile subassembly data not found.")
            df_index = self.mp_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.mp_sub_assemblies.loc[df_index, cols])
            toe = self.pile_head - df["height"].sum() * 1e-3
            self.pile_toe = round(toe, 3)
            depth_to = toe + df.z * 1e-3
            depth_from = depth_to + df.height * 1e-3
        else:
            raise ValueError("Unknown index.")
        df["Elevation from [mLAT]"] = depth_from
        df["Elevation to [mLAT]"] = depth_to
        # Round elevations to mm to avoid numerical inconsistencies later when setting altitude values to apply loads.
        df = df.round({"Elevation from [mLAT]": 3, "Elevation to [mLAT]": 3})
        return df

    def process_structure_geometry(self, idx: str) -> pd.DataFrame:
        """
        Calculate and/or convert geometrical data for FE models.

        Calculates and/or converts geometrical data of subassemblies
        from the database to use as input for FE models.

        Parameters
        ----------
        idx : str
            Possible index to identify corresponding subassembly.

        Returns
        -------
        pd.DataFrame
            Dataframe consisting of the required data to build FE
            models.
        """
        df = self.set_df_structure(idx)
        df["height"] = pd.to_numeric(df["height"])
        df["wall_thickness"] = pd.to_numeric(df["wall_thickness"])
        df.rename(columns={"wall_thickness": "Wall thickness [mm]"}, inplace=True)
        df.rename(columns={"volume": "Volume [m3]"}, inplace=True)
        d_to = [d.split("/", 1)[0] for d in df["OD"].values]
        d_from = [d.split("/", 1)[1] if len(d.split("/", 1)) > 1 else d.split("/", 1)[0] for d in df["OD"].values]
        df["Diameter from [m]"] = np.array(d_from, dtype=float) * 1e-3
        df["Diameter to [m]"] = np.array(d_to, dtype=float) * 1e-3
        df["rho [t/m]"] = df["mass"] / df["height"]
        df["Mass [t]"] = df["mass"] * 1e-3
        df["Height [m]"] = df["height"] * 1e-3
        df["Youngs modulus [GPa]"] = 210
        df["Poissons ratio [-]"] = 0.3
        cols = [
            "Elevation from [mLAT]",
            "Elevation to [mLAT]",
            "Height [m]",
            "Diameter from [m]",
            "Diameter to [m]",
            "Volume [m3]",
            "Wall thickness [mm]",
            "Youngs modulus [GPa]",
            "Poissons ratio [-]",
            "Mass [t]",
            "rho [t/m]",
        ]
        return df[cols]

    def process_rna(self) -> None:
        """
        Set dataframe with required properties to model the RNA system.

        Raises
        ------
        ValueError
            If tower subassembly data not found.
        """
        if self.tw_sub_assemblies is None:
            raise ValueError("Tower subassembly data not found.")
        rna_index = self.tw_sub_assemblies.index.str.contains("RNA")
        rna = deepcopy(
            self.tw_sub_assemblies.loc[
                rna_index,
                ["mass", "moment_of_inertia", "x", "y", "z", "description"],
            ]
        )
        mi = rna["moment_of_inertia"].values
        i_xx, i_yy, i_zz = [], [], []
        for m in mi:
            i_xx.append(m["x"] * 1e-3)
            i_yy.append(m["y"] * 1e-3)
            i_zz.append(m["z"] * 1e-3)
        rna["Ixx [tm2]"] = i_xx
        rna["Iyy [tm2]"] = i_yy
        rna["Izz [tm2]"] = i_zz
        rna["Mass [t]"] = rna["mass"] * 1e-3
        rna["X [m]"] = rna["x"] * 1e-3
        rna["Y [m]"] = rna["y"] * 1e-3
        rna["Z [mLAT]"] = self.tower_base + rna["z"] * 1e-3
        rna.rename(columns={"description": "Description"}, inplace=True)
        cols = [
            "X [m]",
            "Y [m]",
            "Z [mLAT]",
            "Mass [t]",
            "Ixx [tm2]",
            "Iyy [tm2]",
            "Izz [tm2]",
            "Description",
        ]
        self.rna = rna[cols]

    def set_df_appurtenances(self, idx: str) -> pd.DataFrame:
        """
        Set dataframe with required properties for concentrated masses.

        Sets dataframe containing the required properties to model
        concentrated masses from database subassemblies.

        Parameters
        ----------
        idx : str
            Index to identify corresponding subassembly with possible
            values: 'TW', 'TP', 'MP'.

        Returns
        -------
        pd.DataFrame
            Dataframe containing lumped masses data from database with
            Z coordinates in mLAT system.

        Raises
        ------
        ValueError
            If subassembly data not found or unknown index.
        """
        cols = ["mass", "x", "y", "z", "description"]
        if idx == "TW":
            if self.tw_sub_assemblies is None:
                raise ValueError("Tower subassembly data not found.")
            df_index = self.tw_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.tw_sub_assemblies.loc[df_index, cols])
            df["Z [mLAT]"] = self.tower_base + df["z"] * 1e-3
        elif idx == "TP":
            if self.tp_sub_assemblies is None:
                raise ValueError("Transition piece subassembly data not found.")
            df_index = self.tp_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.tp_sub_assemblies.loc[df_index, cols + ["height"]])
            # Lumped masses have 'None' height whereas distributed masses present not 'None' values
            df["height"] = pd.to_numeric(df["height"])
            df = df[df["height"].isnull()]
            bottom = self.sub_assemblies["TP"].position.z * 1e-3  # m
            df["Z [mLAT]"] = bottom + df["z"] * 1e-3  # m
        elif idx == "MP":
            if self.mp_sub_assemblies is None:
                raise ValueError("Monopile subassembly data not found.")
            df_index = self.mp_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.mp_sub_assemblies.loc[df_index, cols + ["height"]])
            # Lumped masses have 'None' height whereas distributed masses present not 'None' values
            df["height"] = pd.to_numeric(df["height"])
            df = df[df["height"].isnull()]
            bottom = self.pile_toe
            df["Z [mLAT]"] = bottom + df["z"] * 1e-3
        else:
            raise ValueError("Unknown index.")
        return df

    def process_lumped_masses(self, idx: str) -> pd.DataFrame:
        """
        Create dataframe with required properties for lumped masses.

        Creates dataframe containing the required properties to model
        lumped mass appurtenances. Note that if the preprocessor
        package does not find any appurtenances it'll return an empty
        dataframe.

        Parameters
        ----------
        idx : str
            Index to identify corresponding subassembly with possible
            values: 'TW', 'TP', 'MP'.

        Returns
        -------
        pd.DataFrame
            Dataframe with lumped mass properties.
        """
        df = self.set_df_appurtenances(idx)
        df["Mass [t]"] = df.mass * 1e-3
        df["X [m]"] = df.x * 1e-3
        df["Y [m]"] = df.y * 1e-3
        df.rename(columns={"description": "Description"}, inplace=True)
        cols = ["X [m]", "Y [m]", "Z [mLAT]", "Mass [t]", "Description"]
        return df[cols]

    def set_df_distributed_appurtenances(self, idx: str) -> pd.DataFrame:
        """
        Set dataframe with required properties for distributed masses.

        Sets dataframe containing the required properties to model
        distributed lumped masses from database.

        Parameters
        ----------
        idx : str
            Index to identify corresponding subassembly with possible
            values: 'TW', 'TP', 'MP'.

        Returns
        -------
        pd.DataFrame
            Dataframe containing distributed lumped masses data from
            database. Z coordinates in mLAT system.

        Raises
        ------
        ValueError
            If subassembly data not found or unknown index or
            distributed lumped masses located outside the transition
            piece.
        """
        cols = ["mass", "x", "y", "z", "height", "volume", "description"]
        if idx == "TP":
            if self.tp_sub_assemblies is None:
                raise ValueError("Transition piece subassembly data not found.")
            df_index = self.tp_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.tp_sub_assemblies.loc[df_index, cols])
            # Lumped masses have 'None' height whereas distributed masses present not 'None' values
            df["height"] = pd.to_numeric(df["height"])
            df = df[df["height"].notnull()]
            bottom_tp = self.tower_base - self.tp_sub_assemblies.iloc[0]["z"] * 1e-3
            df["Z [mLAT]"] = bottom_tp + df["z"] * 1e-3
        elif idx == "MP":
            if self.mp_sub_assemblies is None:
                raise ValueError("Monopile subassembly data not found.")
            df_index = self.mp_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.mp_sub_assemblies.loc[df_index, cols])
            # Lumped masses have 'None' height whereas distributed masses present not 'None' values
            df["height"] = pd.to_numeric(df["height"])
            df = df[df["height"].notnull()]
            bottom = self.pile_toe
            df["Z [mLAT]"] = bottom + df["z"] * 1e-3
        elif idx == "grout":
            if self.tp_sub_assemblies is None:
                raise ValueError("Transition piece subassembly data not found.")
            df_index = self.tp_sub_assemblies.index.str.contains(idx)
            df = deepcopy(self.tp_sub_assemblies.loc[df_index, cols])
            # Lumped masses have 'None' height whereas distributed masses present not 'None' values
            df["height"] = pd.to_numeric(df["height"])
            df = df[df["height"].notnull()]
            bottom_tp = self.tower_base - self.tp_sub_assemblies.iloc[0]["z"] * 1e-3
            df["Z [mLAT]"] = bottom_tp + df["z"] * 1e-3
        else:
            raise ValueError("Unknown index or non distributed lumped masses located outside the transition piece.")
        return df

    def process_distributed_lumped_masses(self, idx: str) -> pd.DataFrame:
        """
        Create dataframe with uniformly distributed appurtenances.

        Creates dataframe containing the required properties to model
        uniformly distributed appurtenances. Note that if the
        preprocessor package does not find any appurtenances it'll
        return an empty dataframe.

        Parameters
        ----------
        idx : str
            Index to identify corresponding subassembly with possible
            values: 'TP', 'MP'.

        Returns
        -------
        pd.DataFrame
            Dataframe with distributed lumped mass properties.
        """
        df = self.set_df_distributed_appurtenances(idx)
        df["Mass [t]"] = df["mass"] * 1e-3
        df["X [m]"] = df["x"] * 1e-3
        df["Y [m]"] = df["y"] * 1e-3
        df["Height [m]"] = df["height"] * 1e-3
        df.rename(columns={"volume": "Volume [m3]"}, inplace=True)
        df.rename(columns={"description": "Description"}, inplace=True)
        cols = [
            "X [m]",
            "Y [m]",
            "Z [mLAT]",
            "Height [m]",
            "Mass [t]",
            "Volume [m3]",
            "Description",
        ]
        return df[cols]

    def process_structure(self, option="full") -> None:
        """
        Set dataframe with required properties to model the tower.

        Sets dataframe containing the required properties to model the
        tower geometry, including the RNA system.

        Parameters
        ----------
        option : str, optional
            Option to process the data for a specific subassembly.
            Possible values:

            - "full": To process all the data for all subassemblies.
            - "tower": To process only the data for the tower
              subassembly.
            - "TP": To process only the data for the transition piece
              subassembly.
            - "monopile": To process only the data for the monopile
              foundation subassembly.

        Examples
        --------
        >>> from contextlib import ExitStack
        >>> from unittest import mock
        >>> location = pd.DataFrame({"elevation": [30.0]})
        >>> def _set_subassemblies(self, subassemblies):
        ...     self.sub_assemblies = {}
        >>> def _set_members(self):
        ...     return None
        >>> with mock.patch.object(
        ...     OWT,
        ...     "_set_subassemblies",
        ...     _set_subassemblies,
        ... ), mock.patch.object(OWT, "_set_members", _set_members):
        ...     owt = OWT(
        ...         api=object(),
        ...         materials=pd.DataFrame(),
        ...         subassemblies=pd.DataFrame(),
        ...         location=location,
        ...     )
        >>> empty_df = pd.DataFrame()
        >>> with ExitStack() as stack:
        ...     _ = stack.enter_context(mock.patch.object(OWT, "process_rna"))
        ...     _ = stack.enter_context(
        ...         mock.patch.object(
        ...             OWT,
        ...             "process_structure_geometry",
        ...             return_value=empty_df,
        ...         )
        ...     )
        ...     _ = stack.enter_context(
        ...         mock.patch.object(
        ...             OWT,
        ...             "process_lumped_masses",
        ...             return_value=empty_df,
        ...         )
        ...     )
        ...     _ = stack.enter_context(
        ...         mock.patch.object(
        ...             OWT,
        ...             "process_distributed_lumped_masses",
        ...             return_value=empty_df,
        ...         )
        ...     )
        ...     owt.process_structure(option="TW")
        >>> owt._init_proc
        True
        """
        self._init_proc = True
        if option == "full":
            self.process_rna()
            self.tower = self.process_structure_geometry("tw")
            self.transition_piece = self.process_structure_geometry("tp")
            self.monopile = self.process_structure_geometry("mp")
            self.tw_lumped_mass = self.process_lumped_masses("TW")
            self.tp_lumped_mass = self.process_lumped_masses("TP")
            self.mp_lumped_mass = self.process_lumped_masses("MP")
            self.tp_distributed_mass = self.process_distributed_lumped_masses("TP")
            self.mp_distributed_mass = self.process_distributed_lumped_masses("MP")
            self.grout = self.process_distributed_lumped_masses("grout")
        elif option == "TW":
            self.process_rna()
            self.tower = self.process_structure_geometry("tw")
            self.tw_lumped_mass = self.process_lumped_masses("TW")
        elif option == "TP":
            self.transition_piece = self.process_structure_geometry("tp")
            self.tp_lumped_mass = self.process_lumped_masses("TP")
            self.tp_distributed_mass = self.process_distributed_lumped_masses("TP")
            self.grout = self.process_distributed_lumped_masses("grout")
        elif option == "MP":
            self.monopile = self.process_structure_geometry("mp")
            self.mp_lumped_mass = self.process_lumped_masses("MP")
            self.mp_distributed_mass = self.process_distributed_lumped_masses("MP")

    @staticmethod
    def can_adjust_properties(row: pd.Series) -> pd.Series:
        """
        Recalculate can properties based on section and elevations.

        Recalculation of can properties based on section properties and
        can elevations: height [m], volume [m3], mass [t], rho [t/m].

        Parameters
        ----------
        row : pd.Series
            Original can properties.

        Returns
        -------
        pd.Series
            Pandas series of recalculated can properties.

        Examples
        --------
        >>> row = pd.Series(
        ...     {
        ...         "Mass [t]": 10.0,
        ...         "Volume [m3]": 5.0,
        ...         "Elevation from [mLAT]": 10.0,
        ...         "Elevation to [mLAT]": 0.0,
        ...         "Diameter from [m]": 6.0,
        ...         "Diameter to [m]": 6.0,
        ...         "Wall thickness [mm]": 10.0,
        ...     }
        ... )
        >>> out = OWT.can_adjust_properties(row)
        >>> float(out["Height [m]"])
        10.0
        """
        density = row["Mass [t]"] / row["Volume [m3]"]
        height = row["Elevation from [mLAT]"] - row["Elevation to [mLAT]"]
        r1 = row["Diameter from [m]"] / 2
        r2 = row["Diameter to [m]"] / 2
        volume_out = 1 / 3 * np.pi * (r1**2 + r1 * r2 + r2**2) * height
        wall_thickness = row["Wall thickness [mm]"] * 1e-3
        r1 = r1 - wall_thickness
        r2 = r2 - wall_thickness
        volume_in = 1 / 3 * np.pi * (r1**2 + r1 * r2 + r2**2) * height
        volume = volume_out - volume_in
        mass = volume * density
        rho_m = mass / height
        can_properties = pd.Series(
            data=[height, volume, mass, rho_m],
            index=["Height [m]", "Volume [m3]", "Mass [t]", "rho [t/m]"],
        )
        return can_properties

    def can_modification(
        self,
        df: pd.DataFrame,
        altitude: Union[np.float64, float, None],
        position: str = "bottom",
    ) -> pd.DataFrame:
        """
        Change can properties based on the altitude.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe containing the can properties.
        altitude : np.float64 or None
            Altitude in mLAT.
        position : str, optional
            Position of the can with respect to the altitude with
            possible values: "bottom" or "top", default is "bottom".

        Returns
        -------
        pd.DataFrame
            Dataframe with the modified can properties.

        Examples
        --------
        >>> df = pd.DataFrame(
        ...     {
        ...         "Elevation from [mLAT]": [10.0],
        ...         "Elevation to [mLAT]": [0.0],
        ...         "Diameter from [m]": [6.0],
        ...         "Diameter to [m]": [6.0],
        ...         "Wall thickness [mm]": [10.0],
        ...         "Volume [m3]": [5.0],
        ...         "Mass [t]": [10.0],
        ...         "rho [t/m]": [1.0],
        ...     },
        ...     index=["A"],
        ... )
        >>> from types import SimpleNamespace
        >>> helper = SimpleNamespace(can_adjust_properties=OWT.can_adjust_properties)
        >>> out = OWT.can_modification(helper, df.copy(), np.float64(5.0))
        >>> float(out["Elevation to [mLAT]"].iloc[0])
        5.0
        """
        if position == "bottom":
            ind = -1
            _col = " to "
        else:
            ind = 0
            _col = " from "
        altitude_val = float(altitude) if altitude is not None else float("nan")
        row_index = df.index[ind]
        df.loc[row_index, "Elevation" + _col + "[mLAT]"] = altitude_val
        col_elev_from = df.columns.get_loc("Elevation from [mLAT]")
        col_elev_to = df.columns.get_loc("Elevation to [mLAT]")
        col_diam_from = df.columns.get_loc("Diameter from [m]")
        col_diam_to = df.columns.get_loc("Diameter to [m]")
        if not isinstance(col_elev_from, int):
            raise ValueError("Expected scalar columns for elevation data.")
        if not isinstance(col_elev_to, int):
            raise ValueError("Expected scalar columns for elevation data.")
        if not isinstance(col_diam_from, int):
            raise ValueError("Expected scalar columns for diameter data.")
        if not isinstance(col_diam_to, int):
            raise ValueError("Expected scalar columns for diameter data.")
        elevation = [
            float(cast(float, df.iat[ind, col_elev_from])),
            float(cast(float, df.iat[ind, col_elev_to])),
        ]
        diameters = [
            float(cast(float, df.iat[ind, col_diam_from])),
            float(cast(float, df.iat[ind, col_diam_to])),
        ]
        df.loc[row_index, "Diameter" + _col + "[m]"] = float(
            np.interp(
                altitude_val,
                elevation,
                diameters,
            )
        )
        cols = ["Height [m]", "Volume [m3]", "Mass [t]", "rho [t/m]"]
        df.loc[df.index[ind], cols] = self.can_adjust_properties(df.iloc[ind])
        return df

    def assembly_tp_mp(self) -> None:
        """
        Process TP structural item to assembly with MP foundation.

        Processes TP structural item to assembly with MP foundation
        ensuring continuity. TP skirt is processed as well.

        Raises
        ------
        TypeError
            If TP or MP items need to be processed before.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> import pandas as pd
        >>> helper = SimpleNamespace(
        ...     transition_piece=None,
        ...     monopile=None,
        ...     _init_spec_part=False,
        ... )
        >>> OWT.assembly_tp_mp(helper)
        Traceback (most recent call last):
            ...
        TypeError: TP or MP items need to be processed before!
        >>> tp = pd.DataFrame(
        ...     {
        ...         "Elevation from [mLAT]": [6.0, 0.0],
        ...         "Elevation to [mLAT]": [8.0, 4.0],
        ...         "Diameter from [m]": [6.0, 6.0],
        ...         "Diameter to [m]": [6.0, 6.0],
        ...         "Wall thickness [mm]": [10.0, 10.0],
        ...         "Volume [m3]": [5.0, 5.0],
        ...         "Mass [t]": [10.0, 10.0],
        ...         "rho [t/m]": [1.0, 1.0],
        ...     }
        ... )
        >>> mp = pd.DataFrame(
        ...     {
        ...         "Elevation from [mLAT]": [0.0],
        ...         "Elevation to [mLAT]": [-10.0],
        ...         "Diameter from [m]": [6.0],
        ...         "Diameter to [m]": [6.0],
        ...         "Wall thickness [mm]": [10.0],
        ...         "Volume [m3]": [5.0],
        ...         "Mass [t]": [10.0],
        ...         "rho [t/m]": [1.0],
        ...     }
        ... )
        >>> helper = SimpleNamespace(
        ...     transition_piece=tp,
        ...     monopile=mp,
        ...     pile_head=5.0,
        ...     substructure=None,
        ...     tp_skirt=None,
        ...     _init_spec_part=False,
        ... )
        >>> helper.can_adjust_properties = OWT.can_adjust_properties
        >>> helper.can_modification = lambda df, altitude, position="bottom": OWT.can_modification(
        ...     helper,
        ...     df,
        ...     altitude,
        ...     position=position,
        ... )
        >>> OWT.assembly_tp_mp(helper)
        >>> helper.substructure is not None
        True
        >>> helper.tp_skirt is not None
        True
        """
        self._init_spec_part = True
        if (self.transition_piece is not None) and (self.monopile is not None):
            mp_head = self.pile_head
            tp = self.transition_piece
            df = deepcopy(tp[tp["Elevation from [mLAT]"] > mp_head])
            if df.loc[df.index[0], "Elevation to [mLAT]"] != mp_head:
                # Not bolted connection (i.e. Rentel) preprocessing needed
                tp1 = self.can_modification(df, mp_head, position="bottom")
                self.substructure = pd.concat([tp1, deepcopy(self.monopile)])
            else:
                # Bolted connection, nothing to do
                self.substructure = pd.concat([df, deepcopy(self.monopile)])
            df = deepcopy(tp[tp["Elevation to [mLAT]"] < mp_head])
            self.tp_skirt = self.can_modification(df, mp_head, position="top")
        else:
            raise TypeError("TP or MP items need to be processed before!")

    def assembly_full_structure(self) -> None:
        """
        Process the full structure of the OWT.

        Processes the full structure of the OWT: tower + tp combination
        with monopile.

        Raises
        ------
        TypeError
            If tower or substructure needs to be processed before.

        Examples
        --------
        >>> import pandas as pd
        >>> from types import SimpleNamespace
        >>> helper = SimpleNamespace(
        ...     substructure=pd.DataFrame({"Height [m]": [1.0]}),
        ...     tower=pd.DataFrame({"Height [m]": [2.0]}),
        ...     _init_spec_full=False,
        ... )
        >>> OWT.assembly_full_structure(helper)
        >>> float(helper.full_structure["Height [m]"].sum())
        3.0
        >>> helper._init_spec_full
        True
        >>> helper = SimpleNamespace(
        ...     substructure=None,
        ...     tower=None,
        ...     _init_spec_full=False,
        ... )
        >>> OWT.assembly_full_structure(helper)
        Traceback (most recent call last):
            ...
        TypeError: Substructure needs to be processed before!
        >>> helper = SimpleNamespace(
        ...     substructure=pd.DataFrame({"Height [m]": [1.0]}),
        ...     tower=None,
        ...     _init_spec_full=False,
        ... )
        >>> OWT.assembly_full_structure(helper)
        Traceback (most recent call last):
            ...
        TypeError: Tower needs to be processed before!
        """
        self._init_spec_full = True
        if self.substructure is not None:
            if self.tower is not None:
                self.full_structure = pd.concat([self.tower, self.substructure])
            else:
                raise TypeError("Tower needs to be processed before!")
        else:
            raise TypeError("Substructure needs to be processed before!")

    def extend_dfs(self) -> None:
        """
        Extend the dataframes with the subassembly columns.

        Examples
        --------
        >>> import pandas as pd
        >>> from types import SimpleNamespace
        >>> helper = SimpleNamespace(
        ...     pile_toe=None,
        ...     rna=None,
        ...     tower=pd.DataFrame({"Height [m]": [1.0]}),
        ...     transition_piece=None,
        ...     monopile=None,
        ...     tw_lumped_mass=None,
        ...     tp_lumped_mass=None,
        ...     mp_lumped_mass=None,
        ...     tp_distributed_mass=None,
        ...     mp_distributed_mass=None,
        ...     grout=None,
        ...     sub_assemblies={},
        ...     substructure=None,
        ...     tp_skirt=None,
        ...     full_structure=None,
        ...     _init_spec_part=False,
        ...     _init_spec_full=False,
        ... )
        >>> OWT.extend_dfs(helper)
        >>> helper.tower["Subassembly"].iloc[0]
        'TW'
        >>> helper.tp_skirt is None
        True
        """
        for attr in ATTR_PROC:
            df = getattr(self, attr)
            if df is not None:
                if "tower" in attr or "tw_" in attr or "rna" in attr:
                    df["Subassembly"] = "TW"
                    setattr(self, attr, df)
                elif "tp_" in attr or "transition" in attr or "grout" in attr:
                    df["Subassembly"] = "TP"
                    setattr(self, attr, df)
                elif "mp_" in attr or "monopile" in attr:
                    df["Subassembly"] = "MP"
                    setattr(self, attr, df)
        if "TP" in self.sub_assemblies and "MP" in self.sub_assemblies:
            self.assembly_tp_mp()
        else:
            self._init_spec_part = True
            self.tp_skirt = None
        if "TW" in self.sub_assemblies:
            self._init_spec_full = True
            if self.substructure is not None:
                self.assembly_full_structure()
            else:
                self.full_structure = None
        else:
            self.full_structure = None
            self._init_spec_full = True

    @typing.no_type_check
    def transform_monopile_geometry(
        self,
        cutoff_point: np.floating = np.nan,
    ) -> pd.DataFrame:
        """
        Return a dataframe with monopile geometry.

        Returns a dataframe with the monopile geometry with the mudline
        as reference.

        Parameters
        ----------
        cutoff_point : np.floating, optional
            Depth from the mudline to cut the monopile geometry.

        Returns
        -------
        pd.DataFrame
            Dataframe with the monopile geometry.

        Raises
        ------
        ValueError
            If monopile subassembly data not found.
        """
        toe_depth_lat = self.sub_assemblies["MP"].position.z
        penetration = -((1e-3 * toe_depth_lat) - self.water_depth)
        pile = pd.DataFrame()
        if self.mp_sub_assemblies is not None:
            df = self.mp_sub_assemblies.copy()
        else:
            raise ValueError("Monopile subassembly data not found.")
        df.reset_index(inplace=True)
        for i, row in df.iterrows():
            if i != 0:
                pile.loc[i, "Elevation from [m]"] = penetration - 1e-3 * df["z"].iloc[i - 1]
                pile.loc[i, "Elevation to [m]"] = penetration - 1e-3 * row["z"]
                pile.loc[i, "Pile material"] = self.sub_assemblies["MP"].bb[0].material.title
                pile.loc[i, "Pile material submerged unit weight [kN/m3]"] = (
                    1e-2 * self.sub_assemblies["MP"].bb[0].material.density - 10
                )
                pile.loc[i, "Wall thickness [mm]"] = row["wall_thickness"]
                bot_od = row["OD"].split("/")[0] if "/" in row["OD"] else row["OD"]
                top_od = row["OD"].split("/")[1] if "/" in row["OD"] else row["OD"]
                pile.loc[i, "Diameter [m]"] = 1e-3 * 0.5 * (float(bot_od) + float(top_od))
                pile.loc[i, "Youngs modulus [GPa]"] = self.sub_assemblies["MP"].bb[0].material.young_modulus
                pile.loc[i, "Poissons ratio [-]"] = self.sub_assemblies["MP"].bb[0].material.poisson_ratio
        if not np.isnan(cutoff_point):
            pile = pile.loc[pile["Elevation to [m]"] > cutoff_point].reset_index(drop=True)
            pile.loc[0, "Elevation from [m]"] = cutoff_point
        return pile

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

    def __getattribute__(self, name: str) -> object:
        if name in ATTR_PROC and not self._init_proc:
            warnings.warn(
                f"Attribute '{name}' accessed before processing. \
                    Run process_structure() first if you want to process values.",
                stacklevel=2,
            )
        elif name in ATTR_SPEC and not self._init_spec_part:
            warnings.warn(
                f"Attribute '{name}' accessed before processing. \
                    Run assembly_tp_mp() first if you want to process values.",
                stacklevel=2,
            )
        elif name in ATTR_SPEC and not self._init_spec_full:
            warnings.warn(
                f"Attribute '{name}' accessed before processing. \
                    Run assembly_full_structure() first if you want to process values.",
                stacklevel=2,
            )
        return object.__getattribute__(self, name)


class OWTs:
    """Class to process the geometry data of multiple OWTs.

    :param owts: List of OWT objects.
    :param api: API object used to call get_* methods.
    :param materials: Pandas dataframe with the materials data.
    :param sub_assemblies: Dictionary of dictionaries of the subassemblies for each turbine.
    :param tower_base: Dictionary of the elevation of the OWT tower base in mLAT for each turbine.
    :param pile_head: Dictionary of the elevation of the pile head in mLAT for each turbine.
    :param water_depth: Dictionary of the water depth in mLAT for each turbine.
    :param tw_sub_assemblies: Dataframe of the tower subassemblies data from each turbine.
    :param tp_sub_assemblies: Dataframe of the transition piece subassemblies data from each turbine.
    :param mp_sub_assemblies: Dataframe of the monopile subassemblies data from each turbine.
    :param pile_toe: Dataframe of the elevation of the pile toe in mLAT from each turbine.
    :param rna: Dataframe of the RNA data from each turbine.
    :param tower: Dataframe of the tower data from each turbine.
    :param transition_piece: Dataframe of the transition piece data from each turbine.
    :param monopile: Dataframe of the monopile data from each turbine.
    :param tw_lumped_mass: Dataframe of the lumped masses data of the tower from each turbine.
    :param tp_lumped_mass: Dataframe of the lumped masses data of the transition piece from each turbine.
    :param mp_lumped_mass: Dataframe of the lumped masses data of the monopile from each turbine.
    :param tp_distributed_mass: Dataframe of the distributed masses data of the transition piece from each turbine.
    :param mp_distributed_mass: Dataframe of the distributed masses data of the monopile from each turbine.
    :param grout: Dataframe of the grout data from each turbine.
    :param full_structure: Dataframe of the full structure data from each turbine.
    :param tp_skirt: Dataframe of the transition piece skirt data from each turbine.
    :param substructure: Dataframe of the substructure data from each turbine.
    :param all_turbines: Dataframe of the general geometry data from each turbine.
    :param all_tubular_structures: Dataframe of the tubular structures data from each turbine.
    :param all_distributed_mass: Dataframe of the distributed masses data from each turbine.
    :param all_lumped_mass: Dataframe of the lumped masses data from each turbine.
    """

    def __init__(
        self,
        turbines: list[str],
        owts: list[OWT],
    ) -> None:
        """
        Create an instance of the OWTs class with required parameters.

        Parameters
        ----------
        turbines : list of str
            List of turbine titles.
        owts : list of OWT
            List of OWT objects.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> stub = SimpleNamespace(
        ...     api="api",
        ...     materials="materials",
        ...     sub_assemblies={},
        ...     tower_base=0.0,
        ...     pile_head=0.0,
        ...     water_depth=0.0,
        ...     tw_sub_assemblies=None,
        ...     tp_sub_assemblies=None,
        ...     mp_sub_assemblies=None,
        ... )
        >>> owts = OWTs(["T01"], [stub])
        >>> owts.api
        'api'
        """
        self.owts = dict(zip(turbines, owts))
        self.api = self.owts[turbines[0]].api
        self.materials = self.owts[turbines[0]].materials
        for attr in [
            "sub_assemblies",
            "tower_base",
            "pile_head",
            "water_depth",
        ]:
            dict_ = {k: getattr(owt, attr) for k, owt in zip(turbines, self.owts.values())}
            setattr(self, attr, dict_)
        for attr in [
            "tw_sub_assemblies",
            "tp_sub_assemblies",
            "mp_sub_assemblies",
        ]:
            sa_turb_list = [getattr(owt, attr) for owt in self.owts.values() if getattr(owt, attr) is not None]
            df = None if sa_turb_list == [] else pd.concat(sa_turb_list)
            setattr(self, attr, df)
        for attr in ATTR_PROC:
            setattr(self, attr, [])
        for attr in ATTR_SPEC:
            setattr(self, attr, [])
        for attr in ATTR_FULL:
            setattr(self, attr, [])
        self._init = False

    def _concat_list(self, attr_list: list[str]) -> None:
        """
        Concatenate lists of dataframes for attributes.

        Parameters
        ----------
        attr_list : list of str
            List of attributes to concatenate.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> stub = SimpleNamespace(
        ...     api="api",
        ...     materials="materials",
        ...     sub_assemblies={},
        ...     tower_base=0.0,
        ...     pile_head=0.0,
        ...     water_depth=0.0,
        ...     tw_sub_assemblies=None,
        ...     tp_sub_assemblies=None,
        ...     mp_sub_assemblies=None,
        ... )
        >>> owts = OWTs(["T01"], [stub])
        >>> owts.tower = [pd.DataFrame({"a": [1]}), pd.DataFrame({"a": [2]})]
        >>> owts._concat_list(["tower"])
        >>> owts.tower.shape[0]
        2
        """
        for attr in attr_list:
            attr_val = getattr(self, attr)
            df = None if attr_val is None or attr_val == [] or all(v is None for v in attr_val) else pd.concat(attr_val)
            setattr(self, attr, df)

    def _assembly_turbine(self) -> None:
        """
        Assemble general geometry data of all specified turbines.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> monopile = pd.DataFrame(
        ...     {"Height [m]": [10.0], "Mass [t]": [1.0]}
        ... )
        >>> mp_dist = pd.DataFrame({"Mass [t]": [0.1]})
        >>> mp_lump = pd.DataFrame({"Mass [t]": [0.2]})
        >>> transition_piece = pd.DataFrame(
        ...     {"Height [m]": [5.0], "Mass [t]": [0.5]}
        ... )
        >>> tp_dist = pd.DataFrame({"Mass [t]": [0.1]})
        >>> tp_lump = pd.DataFrame({"Mass [t]": [0.2]})
        >>> grout = pd.DataFrame({"Mass [t]": [0.1]})
        >>> tower = pd.DataFrame({"Height [m]": [20.0], "Mass [t]": [2.0]})
        >>> tw_lump = pd.DataFrame({"Mass [t]": [0.3]})
        >>> rna = pd.DataFrame({"Mass [t]": [0.4]})
        >>> stub = SimpleNamespace(
        ...     api="api",
        ...     materials="materials",
        ...     sub_assemblies={},
        ...     tower_base=0.0,
        ...     pile_head=0.0,
        ...     water_depth=0.0,
        ...     tw_sub_assemblies=None,
        ...     tp_sub_assemblies=None,
        ...     mp_sub_assemblies=None,
        ...     monopile=monopile,
        ...     mp_distributed_mass=mp_dist,
        ...     mp_lumped_mass=mp_lump,
        ...     transition_piece=transition_piece,
        ...     tp_distributed_mass=tp_dist,
        ...     tp_lumped_mass=tp_lump,
        ...     grout=grout,
        ...     tower=tower,
        ...     tw_lumped_mass=tw_lump,
        ...     rna=rna,
        ... )
        >>> owts = OWTs(["T01"], [stub])
        >>> owts.water_depth = {"T01": 30.0}
        >>> owts.pile_toe = {"T01": -60.0}
        >>> owts.pile_head = {"T01": 5.0}
        >>> owts.tower_base = {"T01": 10.0}
        >>> owts._assembly_turbine()
        >>> "Turbine name" in owts.all_turbines.columns
        True
        """
        cols = [
            "Turbine name",
            "Water depth [m]",
            "Monopile toe [m]",
            "Monopile head [m]",
            "Tower base [m]",
            "Monopile height [m]",
            "Monopile mass [t]",
            "Transition piece height [m]",
            "Transition piece mass [t]",
            "Tower height [m]",
            "Tower mass [t]",
            "RNA mass [t]",
        ]
        df_list = []
        for attr in ATTR_PROC:
            df = getattr(self, attr)
            # if df is None:
            #     raise ValueError(f"Attribute '{attr}' is None.")
        pile_toe_map = cast(dict[str, Union[np.float64, float, None]], self.pile_toe)
        for turb in self.owts:
            df_list.append(
                [
                    turb,
                    self.water_depth[turb],
                    pile_toe_map[turb],
                    self.pile_head[turb],
                    self.tower_base[turb],
                    (self.owts[turb].monopile["Height [m]"].sum() if self.owts[turb].monopile is not None else None),
                    (
                        (
                            self.owts[turb].monopile["Mass [t]"].sum()
                            + self.owts[turb].mp_distributed_mass["Mass [t]"].sum()
                            + self.owts[turb].mp_lumped_mass["Mass [t]"].sum()
                        )
                        if self.owts[turb].monopile is not None
                        else None
                    ),
                    (
                        self.owts[turb].transition_piece["Height [m]"].sum()
                        if self.owts[turb].transition_piece is not None
                        else None
                    ),
                    (
                        (
                            self.owts[turb].transition_piece["Mass [t]"].sum()
                            + self.owts[turb].tp_distributed_mass["Mass [t]"].sum()
                            + self.owts[turb].tp_lumped_mass["Mass [t]"].sum()
                            + self.owts[turb].grout["Mass [t]"].sum()
                        )
                        if self.owts[turb].transition_piece is not None
                        else None
                    ),
                    (self.owts[turb].tower["Height [m]"].sum() if self.owts[turb].tower is not None else None),
                    (
                        (self.owts[turb].tower["Mass [t]"].sum() + self.owts[turb].tw_lumped_mass["Mass [t]"].sum())
                        if self.owts[turb].tower is not None
                        else None
                    ),
                    (self.owts[turb].rna["Mass [t]"].sum() if self.owts[turb].rna is not None else None),
                ]
            )
        df = pd.DataFrame(df_list, columns=cols)
        self.all_turbines = df.round(2)

    def process_structures(self) -> None:
        """
        Set dataframes with required properties to model the tower.

        Sets dataframes containing the required properties to model the
        tower geometry, including the RNA system.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> from unittest import mock
        >>> stub = SimpleNamespace(
        ...     api="api",
        ...     materials="materials",
        ...     sub_assemblies={"TW": 1, "TP": 1, "MP": 1},
        ...     tower_base=0.0,
        ...     pile_head=0.0,
        ...     water_depth=0.0,
        ...     tw_sub_assemblies=None,
        ...     tp_sub_assemblies=None,
        ...     mp_sub_assemblies=None,
        ...     process_structure=lambda *args, **kwargs: None,
        ...     extend_dfs=lambda *args, **kwargs: None,
        ...     pile_toe=0.0,
        ...     rna=None,
        ...     tower=None,
        ...     transition_piece=None,
        ...     monopile=None,
        ...     tw_lumped_mass=None,
        ...     tp_lumped_mass=None,
        ...     mp_lumped_mass=None,
        ...     tp_distributed_mass=None,
        ...     mp_distributed_mass=None,
        ...     grout=None,
        ...     full_structure=None,
        ...     tp_skirt=None,
        ...     substructure=None,
        ...     all_tubular_structures=None,
        ...     all_distributed_mass=None,
        ...     all_lumped_mass=None,
        ...     all_turbines=None,
        ... )
        >>> owts = OWTs(["T01"], [stub])
        >>> with mock.patch.object(OWTs, "_concat_list", lambda self, attrs: None), mock.patch.object(
        ...     OWTs, "_assembly_turbine", lambda self: None
        ... ):
        ...     owts.process_structures()
        >>> owts._init
        True
        """
        attr_list = ATTR_PROC + ATTR_SPEC + ATTR_FULL
        attr_list.remove("all_turbines")
        if self._init:
            return
        self._init = True
        for owt in self.owts.values():
            if len(owt.sub_assemblies) != 3:
                for sa in owt.sub_assemblies.keys():  # noqa: SIM118
                    owt.process_structure(option=sa)
            else:
                owt.process_structure()
            owt.extend_dfs()
            for attr in attr_list:
                if attr == "pile_toe":
                    pile_toe_list = cast(list[Union[np.float64, float, None]], self.pile_toe)
                    pile_toe_list.append(getattr(owt, attr))
                    self.pile_toe = pile_toe_list
                elif attr == "all_tubular_structures":
                    self.all_tubular_structures.extend([owt.tower, owt.transition_piece, owt.monopile])
                elif attr == "all_distributed_mass":
                    self.all_distributed_mass.extend(
                        [
                            owt.tp_distributed_mass,
                            owt.grout,
                            owt.mp_distributed_mass,
                        ]
                    )
                elif attr == "all_lumped_mass":
                    if isinstance(owt.rna, pd.DataFrame):
                        cols = [
                            "X [m]",
                            "Y [m]",
                            "Z [mLAT]",
                            "Mass [t]",
                            "Description",
                            "Subassembly",
                        ]
                        rna_ = owt.rna[cols]
                    else:
                        rna_ = owt.rna
                    self.all_lumped_mass.extend(
                        [
                            rna_,
                            owt.tw_lumped_mass,
                            owt.tp_lumped_mass,
                            owt.mp_lumped_mass,
                        ]
                    )
                else:
                    attr_val = getattr(self, attr)
                    owt_attr_val = getattr(owt, attr)
                    attr_val.append(owt_attr_val)
        attr_list.remove("pile_toe")
        self.pile_toe = dict(zip(self.owts.keys(), self.pile_toe))
        self._concat_list(attr_list)
        self._assembly_turbine()

    def select_owt(self, turbine: Union[str, int]) -> OWT:
        """
        Select OWT object from the OWTs object.

        Parameters
        ----------
        turbine : str or int
            Title of the turbine or its index in the original list of
            turbine titles (from get method).

        Returns
        -------
        OWT
            OWT object.

        Raises
        ------
        ValueError
            If turbine must be specified as single turbine title or
            its index from the get method input turbine list.

        Examples
        --------
        >>> from types import SimpleNamespace
        >>> stub = SimpleNamespace(
        ...     api="api",
        ...     materials="materials",
        ...     sub_assemblies={},
        ...     tower_base=0.0,
        ...     pile_head=0.0,
        ...     water_depth=0.0,
        ...     tw_sub_assemblies=None,
        ...     tp_sub_assemblies=None,
        ...     mp_sub_assemblies=None,
        ... )
        >>> owts = OWTs(["T01"], [stub])
        >>> owts.select_owt("T01") is stub
        True
        """
        if isinstance(turbine, int):
            return self.owts[list(self.owts.keys())[turbine]]
        elif isinstance(turbine, str):
            return self.owts[turbine]
        else:
            raise ValueError(
                "You must specify a single turbine title or \
                its index from the the get method input turbine list."
            )

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

    def __getattribute__(self, name):
        if name in ATTR_PROC + ATTR_SPEC + ATTR_FULL and not self._init:
            warnings.warn(
                f"Attribute '{name}' accessed before processing. \
                    Run process_structures() first if you want to process values.",
                stacklevel=2,
            )
        return object.__getattribute__(self, name)
