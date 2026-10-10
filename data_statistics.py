"""Описательные статистики и оценка баланса классов."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import (
    CLASS_COUNTS_CSV,
    CLASS_TO_LABEL,
    DESCRIBE_CSV,
    DIMENSIONS_CSV,
    PLOTS_DIR,
)


def get_descriptive_statistics(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Вычисляет describe() для ширины, высоты, каналов и числовой метки."""
    columns = ["width", "height", "channels", "class_label"]
    missing = set(columns) - set(dataframe.columns)
    if missing:
        raise ValueError(
            f"Для статистики отсутствуют колонки: {sorted(missing)}"
        )
    return dataframe[columns].describe()


def get_class_counts(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Возвращает число изображений и процент для каждого класса."""
    counts = dataframe["class_name"].value_counts()
    rows = [
        {
            "class_name": class_name,
            "class_label": numeric_label,
            "count": int(counts.get(class_name, 0)),
        }
        for class_name, numeric_label in CLASS_TO_LABEL.items()
    ]
    result = pd.DataFrame(rows)
    total = int(result["count"].sum())
    result["share_percent"] = result["count"] / total * 100 if total else 0.0
    return result


def is_dataset_balanced(dataframe: pd.DataFrame) -> bool:
    """Возвращает True, если количество файлов одинаково во всех классах."""
    counts = get_class_counts(dataframe)["count"]
    return bool(counts.nunique() == 1)


def save_statistics(
    dataframe: pd.DataFrame,
    describe_path: Path = DESCRIBE_CSV,
    counts_path: Path = CLASS_COUNTS_CSV,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Сохраняет describe() и таблицу количества изображений по классам."""
    describe_table = get_descriptive_statistics(dataframe)
    counts_table = get_class_counts(dataframe)
    describe_path.parent.mkdir(parents=True, exist_ok=True)
    counts_path.parent.mkdir(parents=True, exist_ok=True)
    describe_table.to_csv(describe_path, encoding="utf-8-sig")
    counts_table.to_csv(counts_path, index=False, encoding="utf-8-sig")
    return describe_table, counts_table


def plot_class_distribution(
    dataframe: pd.DataFrame,
    output_path: Path | None = None,
) -> None:
    """Строит столбчатую диаграмму количества изображений каждого класса."""
    counts = get_class_counts(dataframe)
    figure, axis = plt.subplots(figsize=(7, 4))
    bars = axis.bar(counts["class_name"], counts["count"])
    axis.set_title("Распределение изображений по классам")
    axis.set_xlabel("Класс изображения")
    axis.set_ylabel("Количество изображений")
    axis.bar_label(bars, padding=3)
    figure.tight_layout()
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(figure)
    else:
        plt.show()


def main() -> None:
    """Показывает описательную статистику и баланс классов."""
    if not DIMENSIONS_CSV.is_file():
        raise FileNotFoundError(
            f"Сначала выполните пункт 4: не найден {DIMENSIONS_CSV}"
        )
    dataframe = pd.read_csv(DIMENSIONS_CSV)
    describe_table, counts_table = save_statistics(dataframe)
    print(describe_table)
    print(counts_table)
    print(f"Набор сбалансирован: {is_dataset_balanced(dataframe)}")
    plot_class_distribution(dataframe, PLOTS_DIR / "class_distribution.png")


if __name__ == "__main__":
    main()
