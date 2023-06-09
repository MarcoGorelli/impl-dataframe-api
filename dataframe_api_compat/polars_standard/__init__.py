from __future__ import annotations
from dataframe_api_compat.polars_standard.polars_standard import (
    PolarsDataFrame,
    PolarsColumn,
)

import polars as pl
from typing import Any, Sequence


class Int64:
    ...


class Int32:
    ...


class Float64:
    ...


class Float32:
    ...


class Bool:
    ...


DTYPE_MAP = {
    pl.Int64: Int64(),
    pl.Int32: Int32(),
    pl.Float64: Float64(),
    pl.Float32: Float32(),
    pl.Boolean: Bool(),
}


def _map_standard_to_polars_dtypes(dtype: Any) -> pl.DataType:
    if isinstance(dtype, Int64):
        return pl.Int64()
    if isinstance(dtype, Int32):
        return pl.Int32()
    if isinstance(dtype, Float64):
        return pl.Float64()
    if isinstance(dtype, Float32):
        return pl.Float32()
    if isinstance(dtype, Bool):
        return pl.Boolean()
    raise AssertionError(f"Unknown dtype: {dtype}")


def concat(dataframes: Sequence[PolarsDataFrame]) -> PolarsDataFrame:
    dfs = []
    for _df in dataframes:
        dfs.append(_df.dataframe)
    return PolarsDataFrame(pl.concat(dfs))


def dataframe_from_dict(data: dict[str, PolarsColumn[Any]]) -> PolarsDataFrame:
    return PolarsDataFrame(
        pl.DataFrame({label: column.column for label, column in data.items()})
    )


def column_from_sequence(sequence: Sequence[Any], dtype: Any) -> PolarsColumn[Any]:
    return PolarsColumn(pl.Series(sequence, dtype=_map_standard_to_polars_dtypes(dtype)))


def convert_to_standard_compliant_dataframe(df: pl.DataFrame) -> PolarsDataFrame:
    return PolarsDataFrame(df)
