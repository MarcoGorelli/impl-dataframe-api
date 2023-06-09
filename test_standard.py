# todo: test that errors are appropriately raised when calls violate standard
from __future__ import annotations

from typing import Any, Callable

import pytest
import pandas as pd
import polars as pl
import dataframe_api_compat.pandas_standard
import dataframe_api_compat.polars_standard


def convert_to_standard_compliant_dataframe(df: pd.DataFrame | pl.DataFrame) -> Any:
    # todo: type return
    if isinstance(df, pd.DataFrame):
        return (
            dataframe_api_compat.pandas_standard.convert_to_standard_compliant_dataframe(
                df
            )
        )
    elif isinstance(df, pl.DataFrame):
        return (
            dataframe_api_compat.polars_standard.convert_to_standard_compliant_dataframe(
                df
            )
        )
    else:
        raise AssertionError(f"Got unexpected type: {type(df)}")


def convert_dataframe_to_pandas_numpy(df: pd.DataFrame) -> pd.DataFrame:
    conversions = {
        "boolean": "bool",
        "Int64": "int64",
        "Float64": "float64",
    }
    for nullable, numpy in conversions.items():
        df = df.astype({key: numpy for key in df.columns[df.dtypes == nullable]})
    return df


def convert_series_to_pandas_numpy(ser: pd.Series) -> pd.Series:  # type: ignore[type-arg]
    conversions = {
        "boolean": "bool",
        "Int64": "int64",
        "Int32": "int32",
        "Float64": "float64",
        "Float32": "float32",
    }
    for nullable, numpy in conversions.items():
        if ser.dtype == nullable:
            ser = ser.astype(numpy)  # type: ignore[call-overload]
    return ser


def pytest_generate_tests(metafunc: Any) -> None:
    if "library" in metafunc.fixturenames:
        metafunc.parametrize("library", ["pandas-numpy", "pandas-nullable", "polars"])


def integer_series_1(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1, 2, 3]}, dtype="int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1, 2, 3]}, dtype="Int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [1, 2, 3]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def integer_series_3(library: str) -> object:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1, 2, 4]}, dtype="int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1, 2, 4]}, dtype="Int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [1, 2, 4]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def integer_series_5(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1, 1, 4]}, dtype="int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1, 1, 4]}, dtype="Int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [1, 1, 4]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def integer_series_6(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1, 3, 2]}, dtype="int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1, 3, 2]}, dtype="Int64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [1, 3, 2]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def float_series_1(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [2.0, 3.0]}, dtype="float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [2.0, 3.0]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [2.0, 3.0]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def float_series_2(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [2.0, 1.0]}, dtype="float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [2.0, 1.0]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [2.0, 1.0]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def float_series_3(library: str) -> object:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [float("nan"), 2.0]}, dtype="float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [0.0, 2.0]}, dtype="Float64")
        other = pd.DataFrame({"a": [0.0, 1.0]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df / other).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [float("nan"), 2.0]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def float_series_4(library: str) -> object:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1.0, float("nan")]}, dtype="float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1.0, 0.0]}, dtype="Float64")
        other = pd.DataFrame({"a": [1.0, 0.0]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df / other).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [1.0, float("nan")]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def bool_series_1(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [True, False, True]}, dtype="bool")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [True, False, True]}, dtype="boolean")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [True, False, True]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def bool_series_2(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [True, False, False]}, dtype="bool")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [True, False, False]}, dtype="boolean")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [True, False, False]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def integer_dataframe_1(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype="int64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}, dtype="Int64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def integer_dataframe_2(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1, 2, 4], "b": [4, 2, 6]}, dtype="int64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1, 2, 4], "b": [4, 2, 6]}, dtype="Int64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"a": [1, 2, 4], "b": [4, 2, 6]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def integer_dataframe_3(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame(
            {"a": [1, 2, 3, 4, 5, 6, 7], "b": [7, 6, 5, 4, 3, 2, 1]}, dtype="int64"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame(
            {"a": [1, 2, 3, 4, 5, 6, 7], "b": [7, 6, 5, 4, 3, 2, 1]}, dtype="Int64"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"a": [1, 2, 3, 4, 5, 6, 7], "b": [7, 6, 5, 4, 3, 2, 1]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def integer_dataframe_4(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame(
            {"key": [1, 1, 2, 2], "b": [1, 2, 3, 4], "c": [4, 5, 6, 7]}, dtype="int64"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame(
            {"key": [1, 1, 2, 2], "b": [1, 2, 3, 4], "c": [4, 5, 6, 7]}, dtype="Int64"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"key": [1, 1, 2, 2], "b": [1, 2, 3, 4], "c": [4, 5, 6, 7]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def integer_dataframe_5(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1, 1], "b": [4, 3]}, dtype="int64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1, 1], "b": [4, 3]}, dtype="Int64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"a": [1, 1], "b": [4, 3]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def nan_dataframe_1(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [1.0, 2.0, float("nan")]}, dtype="float64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1.0, 2.0, 0.0]}, dtype="Float64")
        other = pd.DataFrame({"a": [1.0, 1.0, 0.0]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df / other)
    if library == "polars":
        df = pl.DataFrame({"a": [1.0, 2.0, float("nan")]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def nan_dataframe_2(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [0.0, 1.0, float("nan")]}, dtype="float64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [0.0, 1.0, 0.0]}, dtype="Float64")
        other = pd.DataFrame({"a": [1.0, 1.0, 0.0]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df / other)
    if library == "polars":
        df = pl.DataFrame({"a": [0.0, 1.0, float("nan")]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def null_dataframe_1(library: str, request: pytest.FixtureRequest) -> Any:
    df: Any
    if library == "pandas-numpy":
        mark = pytest.mark.xfail()
        request.node.add_marker(mark)
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1.0, 2.0, pd.NA]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"a": [1.0, 2.0, None]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def nan_series_1(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame({"a": [0.0, 1.0, float("nan")]}, dtype="float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [0.0, 1.0, 0.0]}, dtype="Float64")
        other = pd.DataFrame({"a": [1.0, 1.0, 0.0]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df / other).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [0.0, 1.0, float("nan")]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def null_series_1(library: str, request: pytest.FixtureRequest) -> Any:
    df: Any
    if library == "pandas-numpy":
        mark = pytest.mark.xfail()
        request.node.add_marker(mark)
    if library == "pandas-nullable":
        df = pd.DataFrame({"a": [1.0, 2.0, pd.NA]}, dtype="Float64")
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    if library == "polars":
        df = pl.DataFrame({"a": [1.0, 2.0, None]})
        return convert_to_standard_compliant_dataframe(df).get_column_by_name("a")
    raise AssertionError(f"Got unexpected library: {library}")


def bool_dataframe_1(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame(
            {"a": [True, True, False], "b": [True, True, True]}, dtype="bool"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame(
            {"a": [True, True, False], "b": [True, True, True]}, dtype="boolean"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"a": [True, True, False], "b": [True, True, True]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def bool_dataframe_2(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame(
            {
                "key": [1, 1, 2, 2],
                "b": [False, True, True, True],
                "c": [True, False, False, False],
            }
        ).astype({"key": "int64", "b": "bool", "c": "bool"})
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame(
            {
                "key": [1, 1, 2, 2],
                "b": [False, True, True, True],
                "c": [True, False, False, False],
            }
        ).astype({"key": "Int64", "b": "boolean", "c": "boolean"})
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame(
            {
                "key": [1, 1, 2, 2],
                "b": [False, True, True, True],
                "c": [True, False, False, False],
            }
        )
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


def bool_dataframe_3(library: str) -> Any:
    df: Any
    if library == "pandas-numpy":
        df = pd.DataFrame(
            {"a": [False, False], "b": [False, True], "c": [True, True]}, dtype="bool"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "pandas-nullable":
        df = pd.DataFrame(
            {"a": [False, False], "b": [False, True], "c": [True, True]}, dtype="boolean"
        )
        return convert_to_standard_compliant_dataframe(df)
    if library == "polars":
        df = pl.DataFrame({"a": [False, False], "b": [False, True], "c": [True, True]})
        return convert_to_standard_compliant_dataframe(df)
    raise AssertionError(f"Got unexpected library: {library}")


@pytest.mark.parametrize(
    ("reduction", "expected_data"),
    [
        ("any", {"a": [True], "b": [True]}),
        ("all", {"a": [False], "b": [True]}),
    ],
)
def test_reductions(
    library: str, reduction: str, expected_data: dict[str, object]
) -> None:
    df = bool_dataframe_1(library)
    result = getattr(df, reduction)()
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    expected = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result_pd, expected)


@pytest.mark.parametrize(
    ("comparison", "expected_data"),
    [
        ("__eq__", {"a": [True, True, False], "b": [True, False, True]}),
        ("__ne__", {"a": [False, False, True], "b": [False, True, False]}),
        ("__ge__", {"a": [True, True, False], "b": [True, True, True]}),
        ("__gt__", {"a": [False, False, False], "b": [False, True, False]}),
        ("__le__", {"a": [True, True, True], "b": [True, False, True]}),
        ("__lt__", {"a": [False, False, True], "b": [False, False, False]}),
        ("__add__", {"a": [2, 4, 7], "b": [8, 7, 12]}),
        ("__sub__", {"a": [0, 0, -1], "b": [0, 3, 0]}),
        ("__mul__", {"a": [1, 4, 12], "b": [16, 10, 36]}),
        ("__truediv__", {"a": [1, 1, 0.75], "b": [1, 2.5, 1]}),
        ("__floordiv__", {"a": [1, 1, 0], "b": [1, 2, 1]}),
        ("__pow__", {"a": [1, 4, 81], "b": [256, 25, 46656]}),
        ("__mod__", {"a": [0, 0, 3], "b": [0, 1, 0]}),
    ],
)
def test_comparisons(
    library: str, comparison: str, expected_data: dict[str, object]
) -> None:
    df = integer_dataframe_1(library)
    other = integer_dataframe_2(library)
    result = getattr(df, comparison)(other).dataframe
    if library == "polars" and comparison == "__pow__":
        # Is this right? Might need fixing upstream.
        result = result.select(pl.col("*").cast(pl.Int64))
    result_pd = pd.api.interchange.from_dataframe(result)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result_pd, expected)


@pytest.mark.parametrize(
    ("comparison", "expected_data"),
    [
        ("__eq__", {"a": [False, True, False], "b": [False, False, False]}),
        ("__ne__", {"a": [True, False, True], "b": [True, True, True]}),
        ("__ge__", {"a": [False, True, True], "b": [True, True, True]}),
        ("__gt__", {"a": [False, False, True], "b": [True, True, True]}),
        ("__le__", {"a": [True, True, False], "b": [False, False, False]}),
        ("__lt__", {"a": [True, False, False], "b": [False, False, False]}),
        ("__add__", {"a": [3, 4, 5], "b": [6, 7, 8]}),
        ("__sub__", {"a": [-1, 0, 1], "b": [2, 3, 4]}),
        ("__mul__", {"a": [2, 4, 6], "b": [8, 10, 12]}),
        ("__truediv__", {"a": [0.5, 1, 1.5], "b": [2, 2.5, 3]}),
        ("__floordiv__", {"a": [0, 1, 1], "b": [2, 2, 3]}),
        ("__pow__", {"a": [1, 4, 9], "b": [16, 25, 36]}),
        ("__mod__", {"a": [1, 0, 1], "b": [0, 1, 0]}),
    ],
)
def test_comparisons_with_scalar(
    library: str, comparison: str, expected_data: dict[str, object]
) -> None:
    df = integer_dataframe_1(library)
    other = 2
    result = getattr(df, comparison)(other).dataframe
    if library == "polars" and comparison == "__pow__":
        # Is this right? Might need fixing upstream.
        result = result.select(pl.col("*").cast(pl.Int64))
    result_pd = pd.api.interchange.from_dataframe(result)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result_pd, expected)


@pytest.mark.parametrize(
    ("comparison", "expected_data"),
    [
        ("__eq__", [True, True, False]),
        ("__ne__", [False, False, True]),
        ("__ge__", [True, True, False]),
        ("__gt__", [False, False, False]),
        ("__le__", [True, True, True]),
        ("__lt__", [False, False, True]),
        ("__add__", [2, 4, 7]),
        ("__sub__", [0, 0, -1]),
        ("__mul__", [1, 4, 12]),
        ("__truediv__", [1, 1, 0.75]),
        ("__floordiv__", [1, 1, 0]),
        ("__pow__", [1, 4, 81]),
        ("__mod__", [0, 0, 3]),
    ],
)
def test_column_comparisons(
    library: str, comparison: str, expected_data: list[object]
) -> None:
    ser: Any
    ser = integer_series_1(library)
    other = integer_series_3(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": getattr(ser, comparison)(other)})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    expected = pd.Series(expected_data, name="result")
    if library == "polars" and comparison == "__pow__":
        # todo: fix
        result_pd = result_pd.astype("int64")
    result_pd = convert_series_to_pandas_numpy(result_pd)
    pd.testing.assert_series_equal(result_pd, expected)


@pytest.mark.parametrize(
    ("comparison", "expected_data"),
    [
        ("__eq__", [False, False, True]),
        ("__ne__", [True, True, False]),
        ("__ge__", [False, False, True]),
        ("__gt__", [False, False, False]),
        ("__le__", [True, True, True]),
        ("__lt__", [True, True, False]),
        ("__add__", [4, 5, 6]),
        ("__sub__", [-2, -1, 0]),
        ("__mul__", [3, 6, 9]),
        ("__truediv__", [1 / 3, 2 / 3, 1]),
        ("__floordiv__", [0, 0, 1]),
        ("__pow__", [1, 8, 27]),
        ("__mod__", [1, 2, 0]),
    ],
)
def test_column_comparisons_scalar(
    library: str, comparison: str, expected_data: list[object]
) -> None:
    ser: Any
    ser = integer_series_1(library)
    other = 3
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": getattr(ser, comparison)(other)})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    expected = pd.Series(expected_data, name="result")
    if library == "polars" and comparison == "__pow__":
        # todo: fix
        result_pd = result_pd.astype("int64")
    result_pd = convert_series_to_pandas_numpy(result_pd)
    pd.testing.assert_series_equal(result_pd, expected)


def test_divmod(library: str) -> None:
    df = integer_dataframe_1(library)
    other = integer_dataframe_2(library)
    result_quotient, result_remainder = df.__divmod__(other)
    result_quotient_pd = pd.api.interchange.from_dataframe(result_quotient.dataframe)
    result_remainder_pd = pd.api.interchange.from_dataframe(result_remainder.dataframe)
    expected_quotient = pd.DataFrame({"a": [1, 1, 0], "b": [1, 2, 1]})
    expected_remainder = pd.DataFrame({"a": [0, 0, 3], "b": [0, 1, 0]})
    result_quotient_pd = convert_dataframe_to_pandas_numpy(result_quotient_pd)
    result_remainder_pd = convert_dataframe_to_pandas_numpy(result_remainder_pd)
    pd.testing.assert_frame_equal(result_quotient_pd, expected_quotient)
    pd.testing.assert_frame_equal(result_remainder_pd, expected_remainder)


def test_divmod_with_scalar(library: str) -> None:
    df = integer_dataframe_1(library)
    other = 2
    result_quotient, result_remainder = df.__divmod__(other)
    result_quotient_pd = pd.api.interchange.from_dataframe(result_quotient.dataframe)
    result_remainder_pd = pd.api.interchange.from_dataframe(result_remainder.dataframe)
    expected_quotient = pd.DataFrame({"a": [0, 1, 1], "b": [2, 2, 3]})
    expected_remainder = pd.DataFrame({"a": [1, 0, 1], "b": [0, 1, 0]})
    result_quotient_pd = convert_dataframe_to_pandas_numpy(result_quotient_pd)
    result_remainder_pd = convert_dataframe_to_pandas_numpy(result_remainder_pd)
    pd.testing.assert_frame_equal(result_quotient_pd, expected_quotient)
    pd.testing.assert_frame_equal(result_remainder_pd, expected_remainder)


def test_column_divmod(library: str) -> None:
    ser = integer_series_1(library)
    other = integer_series_3(library)
    namespace = ser.__column_namespace__()
    result_quotient, result_remainder = ser.__divmod__(other)
    result_quotient_pd = pd.api.interchange.from_dataframe(
        namespace.dataframe_from_dict({"result": result_quotient}).dataframe
    )["result"]
    result_remainder_pd = pd.api.interchange.from_dataframe(
        namespace.dataframe_from_dict({"result": result_remainder}).dataframe
    )["result"]
    expected_quotient = pd.Series([1, 1, 0], name="result")
    expected_remainder = pd.Series([0, 0, 3], name="result")
    result_quotient_pd = convert_series_to_pandas_numpy(result_quotient_pd)
    result_remainder_pd = convert_series_to_pandas_numpy(result_remainder_pd)
    pd.testing.assert_series_equal(result_quotient_pd, expected_quotient)
    pd.testing.assert_series_equal(result_remainder_pd, expected_remainder)


def test_column_divmod_with_scalar(library: str) -> None:
    ser = integer_series_1(library)
    other = 2
    namespace = ser.__column_namespace__()
    result_quotient, result_remainder = ser.__divmod__(other)
    result_quotient_pd = pd.api.interchange.from_dataframe(
        namespace.dataframe_from_dict({"result": result_quotient}).dataframe
    )["result"]
    result_remainder_pd = pd.api.interchange.from_dataframe(
        namespace.dataframe_from_dict({"result": result_remainder}).dataframe
    )["result"]
    expected_quotient = pd.Series([0, 1, 1], name="result")
    expected_remainder = pd.Series([1, 0, 1], name="result")
    result_quotient_pd = convert_series_to_pandas_numpy(result_quotient_pd)
    result_remainder_pd = convert_series_to_pandas_numpy(result_remainder_pd)
    pd.testing.assert_series_equal(result_quotient_pd, expected_quotient)
    pd.testing.assert_series_equal(result_remainder_pd, expected_remainder)


def test_get_column_by_name(library: str) -> None:
    df = integer_dataframe_1(library)
    result = df.get_column_by_name("a")
    namespace = df.__dataframe_namespace__()
    result = namespace.dataframe_from_dict({"result": result})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([1, 2, 3], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_get_column_by_name_invalid(library: str) -> None:
    df = integer_dataframe_1(library)
    with pytest.raises(ValueError):
        df.get_column_by_name([True, False])


def test_get_columns_by_name(library: str) -> None:
    df = integer_dataframe_1(library)
    result = df.get_columns_by_name(["b"]).dataframe
    result_pd = pd.api.interchange.from_dataframe(result)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"b": [4, 5, 6]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_get_columns_by_name_invalid(library: str) -> None:
    df = integer_dataframe_1(library)
    with pytest.raises(TypeError, match=r"Expected sequence of str, got <class \'str\'>"):
        df.get_columns_by_name("b")


def test_get_rows(library: str) -> None:
    df = integer_dataframe_1(library)
    namespace = df.__dataframe_namespace__()
    indices = namespace.column_from_sequence([0, 2, 1], dtype=namespace.Int64())
    result = df.get_rows(indices).dataframe
    result_pd = pd.api.interchange.from_dataframe(result)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"a": [1, 3, 2], "b": [4, 6, 5]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_column_get_rows(library: str) -> None:
    ser = integer_series_1(library)
    namespace = ser.__column_namespace__()
    indices = namespace.column_from_sequence([0, 2, 1], dtype=namespace.Int64())
    result = namespace.dataframe_from_dict({"result": ser.get_rows(indices)})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([1, 3, 2], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


@pytest.mark.parametrize(
    ("start", "stop", "step", "expected"),
    [
        (2, 7, 2, pd.DataFrame({"a": [3, 5, 7], "b": [5, 3, 1]})),
        (None, 7, 2, pd.DataFrame({"a": [1, 3, 5, 7], "b": [7, 5, 3, 1]})),
        (2, None, 2, pd.DataFrame({"a": [3, 5, 7], "b": [5, 3, 1]})),
        (2, None, None, pd.DataFrame({"a": [3, 4, 5, 6, 7], "b": [5, 4, 3, 2, 1]})),
    ],
)
def test_slice_rows(
    library: str,
    start: int | None,
    stop: int | None,
    step: int | None,
    expected: pd.DataFrame,
) -> None:
    df = integer_dataframe_3(library)
    result = df.slice_rows(start, stop, step)
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    pd.testing.assert_frame_equal(result_pd, expected)


def test_get_rows_by_mask(library: str) -> None:
    df = integer_dataframe_1(library)
    namespace = df.__dataframe_namespace__()
    mask = namespace.column_from_sequence([True, False, True], dtype=namespace.Bool())
    result = df.get_rows_by_mask(mask)
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"a": [1, 3], "b": [4, 6]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_insert(library: str) -> None:
    df = integer_dataframe_1(library)
    namespace = df.__dataframe_namespace__()
    new_col = namespace.column_from_sequence([7, 8, 9], dtype=namespace.Int64())
    result = df.insert(1, "c", new_col)
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"a": [1, 2, 3], "c": [7, 8, 9], "b": [4, 5, 6]})
    pd.testing.assert_frame_equal(result_pd, expected)
    # check original df didn't change
    df_pd = pd.api.interchange.from_dataframe(df.dataframe)
    df_pd = convert_dataframe_to_pandas_numpy(df_pd)
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    pd.testing.assert_frame_equal(df_pd, expected)


def test_drop_column(library: str) -> None:
    df = integer_dataframe_1(library)
    result = df.drop_column("a")
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"b": [4, 5, 6]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_drop_column_invalid(library: str) -> None:
    df = integer_dataframe_1(library)
    with pytest.raises(TypeError, match="Expected str, got: <class 'list'>"):
        df.drop_column(["a"])


def test_rename_columns(library: str) -> None:
    df = integer_dataframe_1(library)
    result = df.rename_columns({"a": "c", "b": "e"})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"c": [1, 2, 3], "e": [4, 5, 6]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_rename_columns_invalid(library: str) -> None:
    df = integer_dataframe_1(library)
    with pytest.raises(
        TypeError, match="Expected Mapping, got: <class 'function'>"
    ):  # pragma: no cover
        # why is this not covered? bug in coverage?
        df.rename_columns(lambda x: x.upper())


def test_get_column_names(library: str) -> None:
    df = integer_dataframe_1(library)
    result = df.get_column_names()
    assert [name for name in result] == ["a", "b"]


@pytest.mark.parametrize(
    ("aggregation", "expected_b", "expected_c"),
    [
        ("min", [1, 3], [4, 6]),
        ("max", [2, 4], [5, 7]),
        ("sum", [3, 7], [9, 13]),
        ("prod", [2, 12], [20, 42]),
        ("median", [1.5, 3.5], [4.5, 6.5]),
        ("mean", [1.5, 3.5], [4.5, 6.5]),
        (
            "std",
            [0.7071067811865476, 0.7071067811865476],
            [0.7071067811865476, 0.7071067811865476],
        ),
        ("var", [0.5, 0.5], [0.5, 0.5]),
    ],
)
def test_groupby_numeric(
    library: str, aggregation: str, expected_b: list[float], expected_c: list[float]
) -> None:
    df = integer_dataframe_4(library)
    result = getattr(df.groupby(["key"]), aggregation)()
    sorted_indices = result.sorted_indices(["key"])
    result = result.get_rows(sorted_indices)
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"key": [1, 2], "b": expected_b, "c": expected_c})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_groupby_size(library: str) -> None:
    df = integer_dataframe_4(library)
    result = df.groupby(["key"]).size()
    # got to sort
    idx = result.sorted_indices(["key"])
    result = result.get_rows(idx)
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    expected = pd.DataFrame({"key": [1, 2], "size": [2, 2]})
    # TODO polars returns uint32. what do we standardise to?
    result_pd["size"] = result_pd["size"].astype("int64")
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    pd.testing.assert_frame_equal(result_pd, expected)


def test_groupby_invalid_any_all(library: str) -> None:
    df = integer_dataframe_4(library)
    with pytest.raises(Exception):
        df.groupby(["key"]).any()
    with pytest.raises(Exception):
        df.groupby(["key"]).all()


@pytest.mark.parametrize(
    ("aggregation", "expected_b", "expected_c"),
    [
        ("any", [True, True], [True, False]),
        ("all", [False, True], [False, False]),
    ],
)
def test_groupby_boolean(
    library: str, aggregation: str, expected_b: list[bool], expected_c: list[bool]
) -> None:
    df = bool_dataframe_2(library)
    result = getattr(df.groupby(["key"]), aggregation)()
    # need to sort
    idx = result.sorted_indices(["key"])
    result = result.get_rows(idx)
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"key": [1, 2], "b": expected_b, "c": expected_c})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_any(library: str) -> None:
    df = bool_dataframe_3(library)
    result = df.any()
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    expected = pd.DataFrame({"a": [False], "b": [True], "c": [True]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_all(library: str) -> None:
    df = bool_dataframe_3(library)
    result = df.all()
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    expected = pd.DataFrame({"a": [False], "b": [False], "c": [True]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_column_any(library: str) -> None:
    ser = bool_series_1(library)
    result = ser.any()
    assert result


def test_column_all(library: str) -> None:
    ser = bool_series_1(library)
    result = ser.all()
    assert not result


def test_dataframe_is_nan(library: str) -> None:
    df = nan_dataframe_1(library)
    result = df.is_nan()
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    expected = pd.DataFrame({"a": [False, False, True]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_column_is_nan(library: str) -> None:
    ser = nan_series_1(library)
    result = ser.is_nan()
    namespace = ser.__column_namespace__()
    result_df = namespace.dataframe_from_dict({"result": result})
    result_pd = pd.api.interchange.from_dataframe(result_df.dataframe)["result"]
    expected = pd.Series([False, False, True], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_is_null_1(library: str) -> None:
    df = nan_dataframe_2(library)
    result = df.is_null().dataframe
    result_pd = pd.api.interchange.from_dataframe(result)
    expected = pd.DataFrame({"a": [False, False, False]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_is_null_2(library: str, request: pytest.FixtureRequest) -> None:
    df = null_dataframe_1(library, request)
    result = df.is_null().dataframe
    result_pd = pd.api.interchange.from_dataframe(result)
    expected = pd.DataFrame({"a": [False, False, True]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_shape(library: str) -> None:
    df = integer_dataframe_1(library)
    assert df.shape() == (3, 2)


def test_column_is_null_1(library: str) -> None:
    ser = nan_series_1(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser.is_null()})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    expected = pd.Series([False, False, False], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_column_is_null_2(library: str, request: pytest.FixtureRequest) -> None:
    ser = null_series_1(library, request)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser.is_null()})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    expected = pd.Series([False, False, True], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_concat(library: str) -> None:
    df1 = integer_dataframe_1(library)
    df2 = integer_dataframe_2(library)
    namespace = df1.__dataframe_namespace__()
    result = namespace.concat([df1, df2])
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"a": [1, 2, 3, 1, 2, 4], "b": [4, 5, 6, 4, 2, 6]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_concat_mismatch(library: str) -> None:
    df1 = integer_dataframe_1(library)
    df2 = integer_dataframe_4(library)
    namespace = df1.__dataframe_namespace__()
    # todo check the error
    with pytest.raises((ValueError, pl.exceptions.ShapeError)):
        namespace.concat([df1, df2]).dataframe


@pytest.mark.parametrize(
    ("ser_factory", "other_factory", "expected_values"),
    [
        (float_series_1, float_series_4, [False, False]),
        (float_series_2, float_series_4, [False, True]),
        (float_series_3, float_series_4, [True, False]),
    ],
)
def test_is_in(
    library: str,
    ser_factory: Callable[[str], Any],
    other_factory: Callable[[str], Any],
    expected_values: list[bool],
) -> None:
    other = other_factory(library)
    ser = ser_factory(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser.is_in(other)})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series(expected_values, name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_is_in_raises(library: str) -> None:
    ser = float_series_1(library)
    other = integer_series_1(library)
    with pytest.raises(ValueError):
        ser.is_in(other)


def test_column_len(library: str) -> None:
    result = len(integer_series_1(library))
    assert result == 3


def test_get_value(library: str) -> None:
    result = integer_series_1(library).get_value(0)
    assert result == 1


def test_unique_indices(library: str) -> None:
    ser = integer_series_5(library)
    namespace = ser.__column_namespace__()
    ser = ser.get_rows(ser.unique_indices())
    ser = ser.get_rows(ser.sorted_indices())
    result = namespace.dataframe_from_dict({"result": ser})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([1, 4], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_mean(library: str) -> None:
    result = integer_series_5(library).mean()
    assert result == 2.0


def test_std(library: str) -> None:
    result = integer_series_5(library).std()
    assert abs(result - 1.7320508075688772) < 1e-8


def test_sorted_indices(library: str) -> None:
    df = integer_dataframe_5(library)
    namespace = df.__dataframe_namespace__()
    result = namespace.dataframe_from_dict({"result": df.sorted_indices(keys=["a", "b"])})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    # TODO should we standardise on the return type?
    result_pd = result_pd.astype("int64")
    expected = pd.Series([1, 0], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_column_sorted_indices(library: str) -> None:
    ser = integer_series_6(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser.sorted_indices()})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    # TODO standardise return type?
    result_pd = result_pd.astype("int64")
    expected = pd.Series([0, 2, 1], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_invert(library: str) -> None:
    df = bool_dataframe_1(library)
    result = ~df
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = convert_dataframe_to_pandas_numpy(result_pd)
    expected = pd.DataFrame({"a": [False, False, True], "b": [False, False, False]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_column_invert(library: str) -> None:
    ser = bool_series_1(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ~ser})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([False, True, False], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_column_and(library: str) -> None:
    ser = bool_series_1(library)
    other = bool_series_2(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser & other})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([True, False, False], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_column_or(library: str) -> None:
    ser = bool_series_1(library)
    other = bool_series_2(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser | other})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([True, False, True], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_column_and_with_scalar(library: str) -> None:
    ser = bool_series_1(library)
    other = True
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser & other})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([True, False, True], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_column_or_with_scalar(library: str) -> None:
    ser = bool_series_1(library)
    other = True
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser | other})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([True, True, True], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_column_max(library: str) -> None:
    result = integer_series_1(library).max()
    assert result == 3


def test_repeated_columns() -> None:
    df = pd.DataFrame({"a": [1, 2]}, index=["b", "b"]).T
    with pytest.raises(
        ValueError, match=r"Expected unique column names, got b 2 time\(s\)"
    ):
        convert_to_standard_compliant_dataframe(df)


def test_non_str_columns() -> None:
    df = pd.DataFrame({0: [1, 2]})
    with pytest.raises(
        TypeError,
        match=r"Expected column names to be of type str, got 0 of type <class 'int'>",
    ):
        convert_to_standard_compliant_dataframe(df)


def test_comparison_invalid(library: str) -> None:
    df = integer_dataframe_1(library).get_columns_by_name(["a"])
    other = integer_dataframe_1(library).get_columns_by_name(["b"])
    with pytest.raises(
        (ValueError, pl.exceptions.DuplicateError),
    ):
        df > other


def test_groupby_invalid(library: str) -> None:
    df = integer_dataframe_1(library).get_columns_by_name(["a"])
    with pytest.raises((KeyError, TypeError)):
        df.groupby(0)
    with pytest.raises((KeyError, TypeError)):
        df.groupby("0")
    with pytest.raises((KeyError, TypeError)):
        df.groupby(["b"])


def test_any_rowwise(library: str) -> None:
    df = bool_dataframe_1(library)
    namespace = df.__dataframe_namespace__()
    result = namespace.dataframe_from_dict({"result": df.any_rowwise()})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    expected = pd.Series([True, True, True], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_all_rowwise(library: str) -> None:
    df = bool_dataframe_1(library)
    namespace = df.__dataframe_namespace__()
    result = namespace.dataframe_from_dict({"result": df.all_rowwise()})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    expected = pd.Series([True, True, False], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


def test_fill_nan(library: str) -> None:
    df = nan_dataframe_1(library)
    result = df.fill_nan(-1)
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    result_pd = result_pd.astype("float64")
    expected = pd.DataFrame({"a": [1.0, 2.0, -1.0]})
    pd.testing.assert_frame_equal(result_pd, expected)


def test_column_fill_nan(library: str) -> None:
    # todo: test with nullable pandas
    ser = nan_series_1(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict({"result": ser.fill_nan(-1.0)})
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    expected = pd.Series([0.0, 1.0, -1.0], name="result")
    pd.testing.assert_series_equal(result_pd, expected)


@pytest.mark.parametrize(
    ("reduction", "expected"),
    [
        ("min", pd.DataFrame({"a": [1], "b": [4]})),
        ("max", pd.DataFrame({"a": [3], "b": [6]})),
        ("sum", pd.DataFrame({"a": [6], "b": [15]})),
        ("prod", pd.DataFrame({"a": [6], "b": [120]})),
        ("median", pd.DataFrame({"a": [2.0], "b": [5.0]})),
        ("mean", pd.DataFrame({"a": [2.0], "b": [5.0]})),
        ("std", pd.DataFrame({"a": [1.0], "b": [1.0]})),
        ("var", pd.DataFrame({"a": [1.0], "b": [1.0]})),
    ],
)
def test_dataframe_reductions(
    library: str, reduction: str, expected: pd.DataFrame
) -> None:
    df = integer_dataframe_1(library)
    result = getattr(df, reduction)()
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)
    pd.testing.assert_frame_equal(result_pd, expected)


@pytest.mark.parametrize(
    ("reduction", "expected"),
    [
        ("min", 1),
        ("max", 3),
        ("sum", 6),
        ("prod", 6),
        ("median", 2.0),
        ("mean", 2.0),
        ("std", 1.0),
        ("var", 1.0),
    ],
)
def test_column_reductions(library: str, reduction: str, expected: float) -> None:
    ser = integer_series_1(library)
    result = getattr(ser, reduction)()
    assert result == expected


def test_column_column() -> None:
    result = (
        convert_to_standard_compliant_dataframe(pl.DataFrame({"a": [1, 2, 3]}))
        .get_column_by_name("a")
        .column
    )
    pd.testing.assert_series_equal(result.to_pandas(), pd.Series([1, 2, 3], name="a"))
    result = (
        convert_to_standard_compliant_dataframe(pd.DataFrame({"a": [1, 2, 3]}))
        .get_column_by_name("a")
        .column
    )
    pd.testing.assert_series_equal(result, pd.Series([1, 2, 3], name="a"))


@pytest.mark.parametrize(
    ("values", "dtype", "expected"),
    [
        ([1, 2, 3], "Int64", pd.Series([1, 2, 3], dtype="int64", name="result")),
        ([1, 2, 3], "Int32", pd.Series([1, 2, 3], dtype="int32", name="result")),
        (
            [1.0, 2.0, 3.0],
            "Float64",
            pd.Series([1, 2, 3], dtype="float64", name="result"),
        ),
        (
            [1.0, 2.0, 3.0],
            "Float32",
            pd.Series([1, 2, 3], dtype="float32", name="result"),
        ),
        (
            [True, False, True],
            "Bool",
            pd.Series([True, False, True], dtype=bool, name="result"),
        ),
    ],
)
def test_column_from_sequence(
    library: str, values: list[Any], dtype: str, expected: pd.Series
) -> None:
    ser = integer_series_1(library)
    namespace = ser.__column_namespace__()
    result = namespace.dataframe_from_dict(
        {"result": namespace.column_from_sequence(values, getattr(namespace, dtype)())}
    )
    result_pd = pd.api.interchange.from_dataframe(result.dataframe)["result"]
    result_pd = convert_series_to_pandas_numpy(result_pd)
    pd.testing.assert_series_equal(result_pd, expected)
