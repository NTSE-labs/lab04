"""Проверка и нормализация названий колонок DataFrame."""

from pathlib import Path
import re

import pandas as pd

from config import ANNOTATION_CSV, NORMALIZED_CSV
from dataset_annotation import create_annotation_dataframe


def normalize_column_name(column_name: str) -> str:
    """Приводит название колонки к snake_case."""
    normalized = column_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized)
    return normalized.strip("_")


def normalize_column_names(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Возвращает копию DataFrame с нормализованными названиями колонок."""
    result = dataframe.copy()
    result.columns = [
        normalize_column_name(str(name)) for name in result.columns
    ]
    if len(set(result.columns)) != len(result.columns):
        raise ValueError(
            "После нормализации имена колонок стали неуникальными."
        )
    return result


def save_normalized_dataframe(
    dataframe: pd.DataFrame,
    output_path: Path = NORMALIZED_CSV,
) -> None:
    """Сохраняет DataFrame с нормализованными названиями колонок."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    """Нормализует названия колонок исходной аннотации и сохраняет CSV."""
    dataframe = create_annotation_dataframe()
    normalized = normalize_column_names(dataframe)
    save_normalized_dataframe(normalized)
    print(f"Исходная аннотация: {ANNOTATION_CSV}")
    print(f"Нормализованная аннотация: {NORMALIZED_CSV}")
    print(f"Колонки: {list(normalized.columns)}")


if __name__ == "__main__":
    main()
