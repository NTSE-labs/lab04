"""Добавление числовой метки для каждого класса."""

from pathlib import Path

import pandas as pd

from config import CLASS_TO_LABEL, LABELED_CSV, NORMALIZED_CSV
from dataset_annotation import create_annotation_dataframe
from column_names import normalize_column_names


def add_numeric_class_labels(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Добавляет колонку class_label: cat=0, dog=1."""
    result = dataframe.copy()
    result["class_label"] = result["class_name"].map(CLASS_TO_LABEL)
    if result["class_label"].isna().any():
        unknown = sorted(
            result.loc[result["class_label"].isna(), "class_name"]
            .astype(str)
            .unique()
        )
        raise ValueError(f"Не найдены числовые метки для классов: {unknown}")
    result["class_label"] = result["class_label"].astype("int64")
    return result


def save_labeled_dataframe(
    dataframe: pd.DataFrame,
    output_path: Path = LABELED_CSV,
) -> None:
    """Сохраняет DataFrame с числовыми метками классов в CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    """Добавляет числовые метки к аннотации и сохраняет промежуточный CSV."""
    if NORMALIZED_CSV.is_file():
        dataframe = pd.read_csv(NORMALIZED_CSV)
    else:
        dataframe = normalize_column_names(create_annotation_dataframe())
    labeled = add_numeric_class_labels(dataframe)
    save_labeled_dataframe(labeled)
    print(f"Сохранён файл: {LABELED_CSV}")
    print(labeled[["class_name", "class_label"]].drop_duplicates())


if __name__ == "__main__":
    main()
