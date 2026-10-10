"""Фильтрация DataFrame по классу и максимальным размерам."""

from pathlib import Path

import pandas as pd

from class_filter import filter_by_class
from config import DIMENSIONS_CSV, FILTERED_DIMENSIONS_CSV

DEFAULT_CLASS_LABEL = "cat"
DEFAULT_MAX_WIDTH = 800
DEFAULT_MAX_HEIGHT = 600


def filter_by_class_and_dimensions(
    dataframe: pd.DataFrame,
    class_label: str | int,
    max_width: int,
    max_height: int,
) -> pd.DataFrame:
    """Оставляет класс с width<=max_width и height<=max_height."""
    required_columns = {"width", "height"}
    missing = required_columns - set(dataframe.columns)
    if missing:
        raise ValueError(
            f"Для фильтрации по размерам не хватает колонок: {sorted(missing)}"
        )
    class_dataframe = filter_by_class(dataframe, class_label)
    mask = (
        (class_dataframe["width"] <= max_width)
        & (class_dataframe["height"] <= max_height)
    )
    return class_dataframe.loc[mask].copy()


def main() -> None:
    """Фильтрует кошек по размерам и сохраняет результат в CSV."""
    if not DIMENSIONS_CSV.is_file():
        raise FileNotFoundError(
            f"Сначала выполните пункт 4: не найден {DIMENSIONS_CSV}"
        )
    dataframe = pd.read_csv(DIMENSIONS_CSV)
    filtered = filter_by_class_and_dimensions(
        dataframe,
        DEFAULT_CLASS_LABEL,
        DEFAULT_MAX_WIDTH,
        DEFAULT_MAX_HEIGHT,
    )
    FILTERED_DIMENSIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    filtered.to_csv(
        FILTERED_DIMENSIONS_CSV,
        index=False,
        encoding="utf-8-sig",
    )
    print(f"Отфильтровано изображений: {len(filtered)}")
    print(FILTERED_DIMENSIONS_CSV)


if __name__ == "__main__":
    main()
