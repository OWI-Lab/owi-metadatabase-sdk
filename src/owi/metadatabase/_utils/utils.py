"""Utility functions for the owimetadatabase_preprocessor package."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any, overload

import numpy as np
import pandas as pd


def custom_formatwarning(message, category, filename, lineno, line=None):
    """
    Return customized warning.

    Parameters
    ----------
    message : str
        Warning message.
    category : type
        Warning category.
    filename : str
        Filename where warning occurred.
    lineno : int
        Line number where warning occurred.
    line : str, optional
        Line text where warning occurred.

    Returns
    -------
    str
        Formatted warning string.

    Examples
    --------
    >>> print(custom_formatwarning("warn", UserWarning, "file.py", 10), end="")
    UserWarning: warn
    """
    return f"{category.__name__}: {message}\n"


def dict_generator(
    dict_: dict[str, Any],
    keys_: Sequence[str] | None = None,
    method_: str = "exclude",
) -> dict[str, Any]:
    """
    Generate a dictionary with the specified keys.

    Parameters
    ----------
    dict_ : dict
        Dictionary to be filtered.
    keys_ : Sequence of str, optional
        List of keys to be included or excluded.
    method_ : str, optional
        Method to be used for filtering. Options are "exclude" and
        "include", default is "exclude".

    Returns
    -------
    dict
        Filtered dictionary.

    Raises
    ------
    ValueError
        If method is not recognized.

    Examples
    --------
    >>> dict_generator({"a": 1, "b": 2}, keys_=["a"])
    {'b': 2}
    >>> dict_generator({"a": 1, "b": 2}, keys_=["a"], method_="include")
    {'a': 1}
    >>> dict_generator({"a": 1}, method_="unknown")  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Method not recognized!
    """
    if keys_ is None:
        keys_ = []
    if method_ == "exclude":
        return {k: dict_[k] for k in dict_ if k not in keys_}
    elif method_ == "include":
        return {k: dict_[k] for k in dict_ if k in keys_}
    else:
        raise ValueError("Method not recognized!")


def compare_if_simple_close(a: Any, b: Any, tol: float = 1e-9) -> tuple[bool, None | str]:
    """
    Compare two values and return a boolean and a message.

    Parameters
    ----------
    a : Any
        First value to be compared.
    b : Any
        Second value to be compared.
    tol : float, optional
        Tolerance for the comparison, default is 1e-9.

    Returns
    -------
    tuple
        Tuple with a result of comparison and a message if different.

    Examples
    --------
    >>> compare_if_simple_close(1.0, 1.0)
    (True, None)
    >>> compare_if_simple_close(1.0, 2.0)
    (False, 'Values of 1.0 and 2.0 are different.')
    >>> compare_if_simple_close(np.nan, np.nan)
    (True, None)
    """
    if isinstance(a, (float, np.floating)) and isinstance(b, (float, np.floating)):
        if np.isnan(a) and np.isnan(b):
            return True, None
        assertion = math.isclose(a, b, rel_tol=tol)
        messsage = None if assertion else f"Values of {a} and {b} are different."
        return assertion, messsage
    assertion = a == b
    messsage = None if assertion else f"Values of {a} and {b} are different."
    return assertion, messsage


def check_df_eq(df1: pd.DataFrame, df2: pd.DataFrame, tol: float = 1e-9) -> bool:
    """
    Check if two dataframes are equal.

    Parameters
    ----------
    df1 : pd.DataFrame
        First dataframe to be compared.
    df2 : pd.DataFrame
        Second dataframe to be compared.
    tol : float, optional
        Tolerance for the comparison, default is 1e-9.

    Returns
    -------
    bool
        Boolean indicating if the dataframes are equal.

    Examples
    --------
    >>> df1 = pd.DataFrame({"a": [1.0, 2.0], "b": ["x", "y"]})
    >>> df2 = pd.DataFrame({"a": [1.0, 2.0], "b": ["x", "y"]})
    >>> check_df_eq(df1, df2)
    True
    >>> check_df_eq(pd.DataFrame(), pd.DataFrame())
    True
    """
    if df1.empty and df2.empty:
        return True
    elif (df1.empty and not df2.empty) or (not df1.empty and df2.empty):
        return False
    if df1.shape != df2.shape:
        return False
    num_cols_eq = np.allclose(
        df1.select_dtypes(include="number"),
        df2.select_dtypes(include="number"),
        rtol=tol,
        atol=tol,
        equal_nan=True,
    )
    str_cols_eq = df1.select_dtypes(include="object").equals(df2.select_dtypes(include="object"))
    return num_cols_eq and str_cols_eq


def deepcompare(a: Any, b: Any, tol: float = 1e-5) -> tuple[bool, None | str]:
    """
    Compare two complicated objects recursively.

    Compares two complicated (potentially nested) objects recursively
    and returns a result and a message.

    Parameters
    ----------
    a : Any
        First object to be compared.
    b : Any
        Second object to be compared.
    tol : float, optional
        Tolerance for the comparison, default is 1e-5.

    Returns
    -------
    tuple
        Tuple with a result of comparison and a message if different.

    Examples
    --------
    >>> deepcompare({"a": 1.0}, {"a": 1.0})[0]
    True
    >>> deepcompare([1, 2], [1, 3])[0]
    False
    >>> deepcompare(np.nan, np.nan)[0]
    True
    """
    if type(a) != type(b):  # noqa: E721
        if hasattr(a, "__dict__") and isinstance(b, dict):
            return deepcompare(a.__dict__, b, tol)
        elif hasattr(b, "__dict__") and isinstance(a, dict):
            return deepcompare(a, b.__dict__, tol)
        elif isinstance(a, (float, np.floating)) and isinstance(b, (float, np.floating)):
            return deepcompare(np.float64(a), np.float64(b), tol)
        return (
            False,
            f"Types of {a} and {b} are different: {type(a).__name__} and {type(b).__name__}.",
        )
    elif isinstance(a, dict):
        if a.keys() != b.keys():
            return (
                False,
                f"Dictionary keys {a.keys()} and {b.keys()} are different.",
            )
        compare = [deepcompare(a[key], b[key], tol)[0] for key in a]
        assertion = all(compare)
        if assertion:
            message = None
        else:
            keys = [key for key, val in zip(a.keys(), compare) if val is False]
            message = f"Dictionary values are different for {a} and {b}, for keys: {keys}."
        return assertion, message
    elif isinstance(a, (list, tuple)):
        if len(a) != len(b):
            return (
                False,
                f"Lists/tuples {a} and {b} are of different length: {len(a)} and {len(b)}.",
            )
        compare = [deepcompare(i, j, tol)[0] for i, j in zip(a, b)]
        assertion = all(compare)
        if assertion:
            message = None
        else:
            inds = [ind for ind, val in zip(range(len(compare)), compare) if val is False]
            message = f"Lists/tuples are different for {a} and {b}, for indices: {inds}."
        return assertion, message
    elif hasattr(a, "__dict__") and not isinstance(a, pd.DataFrame):
        return deepcompare(a.__dict__, b.__dict__, tol)
    elif isinstance(a, pd.DataFrame):
        assertion = check_df_eq(a, b, tol)
        message = None if assertion else f"Dataframes {a} and {b} are different for {a.compare(b)}."
        return assertion, message
    else:
        return compare_if_simple_close(a, b, tol)


def fix_nan(obj: Any) -> Any:
    """
    Replace "nan" strings with None.

    Parameters
    ----------
    obj : Any
        Object to be fixed.

    Returns
    -------
    Any
        Fixed object.

    Examples
    --------
    >>> fixed = fix_nan({"a": "NaN", "b": ["nan", "ok"]})
    >>> bool(np.isnan(fixed["a"]))
    True
    >>> bool(np.isnan(fixed["b"][0]))
    True
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = fix_nan(v)
    elif isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = fix_nan(obj[i])
    elif isinstance(obj, str) and obj.lower() == "nan":
        # obj = None
        obj = np.nan
    return obj


def fix_outline(data: Any) -> Any:
    """
    Fix the outline attribute in the data.

    Parameters
    ----------
    data : Any
        Data to be fixed.

    Returns
    -------
    Any
        Fixed data.

    Raises
    ------
    ValueError
        If data type is not supported.

    Examples
    --------
    >>> fix_outline({"outline": [[0, 1], [2, 3]]})
    {'outline': ([0, 1], [2, 3])}
    """
    if isinstance(data, list):
        for i in range(len(data)):
            if "outline" in data[i] and data[i]["outline"] is not None:
                data[i]["outline"] = tuple(data[i]["outline"])
    elif isinstance(data, dict):
        if "outline" in data and data["outline"] is not None:
            data["outline"] = tuple(data["outline"])
    else:
        raise ValueError("Not supported data type.")
    return data


@overload
def hex_to_dec(value: str) -> list[float]: ...
@overload
def hex_to_dec(value: list[str]) -> list[list[float]]: ...
@overload
def hex_to_dec(value: tuple[str, ...]) -> list[list[float]]: ...
def hex_to_dec(value: str | Sequence[str]) -> list[float] | list[list[float]]:
    """
    Convert hex color(s) to normalized [r, g, b, a] floats.

    Accepts 6-digit (#rrggbb) or 8-digit (#rrggbbaa) hex strings, with
    or without leading '#'.
    - If `value` is a string: returns [r, g, b, a]
    - If `value` is a list of strings: returns [[r, g, b, a], ...]

    Parameters
    ----------
    value : str or Sequence of str
        Hex color string or list of hex color strings.

    Returns
    -------
    list of float or list of list of float
        Normalized RGBA list or list of such lists.

    Raises
    ------
    ValueError
        If the hex string length is not 6 or 8, or if the input type
        is not supported.

    Examples
    --------
    >>> hex_to_dec("#ff0000")
    [1.0, 0.0, 0.0, 1.0]
    >>> hex_to_dec(["#000000", "ffffff"])
    [[0.0, 0.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0]]
    """

    def _hex_to_dec(s: str) -> list[float]:
        s = s.lstrip("#") if s.startswith("#") else s
        if len(s) not in (6, 8):
            raise ValueError("Length of the color string must be 6 or 8 (excluding #)")
        r = int(s[0:2], 16) / 255.0
        g = int(s[2:4], 16) / 255.0
        b = int(s[4:6], 16) / 255.0
        a = int(s[6:8], 16) / 255.0 if len(s) == 8 else 1.0
        return [r, g, b, a]

    if isinstance(value, str):
        return _hex_to_dec(value)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_hex_to_dec(v) for v in value]
    raise ValueError("Value must be a string or a list of strings.")
