"""Фильтрация DataFrame по метке класса."""

from pathlib import Path

import pandas as pd

from config import DIMENSIONS_CSV, FILTERED_CLASS_CSV


def filter_by_class(
    dataframe: pd.DataFrame,
    class_label: str | int,
) -> pd.DataFrame:
    """Возвращает копию DataFrame только со строками указанного класса."""
    column = "class_name" if isinstance(class_label, str) else "class_label"
    if column not in dataframe.columns:
        raise ValueError(f"В DataFrame отсутствует колонка {column!r}.")
    return dataframe.loc[dataframe[column] == class_label].copy()


def main() -> None:
    """Демонстрирует фильтрацию по классу cat и сохраняет результат в CSV."""
    if not DIMENSIONS_CSV.is_file():
        raise FileNotFoundError(
            f"Сначала выполните пункт 4: не найден {DIMENSIONS_CSV}"
        )
    dataframe = pd.read_csv(DIMENSIONS_CSV)
    filtered = filter_by_class(dataframe, "cat")
    FILTERED_CLASS_CSV.parent.mkdir(parents=True, exist_ok=True)
    filtered.to_csv(FILTERED_CLASS_CSV, index=False, encoding="utf-8-sig")
    print(f"Сохранено строк класса cat: {len(filtered)}")
    print(FILTERED_CLASS_CSV)


if __name__ == "__main__":
    main()
