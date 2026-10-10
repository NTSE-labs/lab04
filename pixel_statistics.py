"""Статистика количества пикселей и визуализация примеров."""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import pandas as pd

from config import DIMENSIONS_CSV, PIXEL_STATS_CSV, ANALYSIS_CSV, PLOTS_DIR


def add_pixel_count(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Добавляет число пикселей как произведение ширины на высоту."""
    result = dataframe.copy()
    result["pixel_count"] = result["width"] * result["height"]
    return result


def group_pixel_statistics(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Считает минимум, максимум и среднее число пикселей по классам."""
    pixel_dataframe = add_pixel_count(dataframe)
    return (
        pixel_dataframe.groupby("class_name")["pixel_count"]
        .agg(["min", "max", "mean"])
        .rename(
            columns={
                "min": "minimum_pixels",
                "max": "maximum_pixels",
                "mean": "average_pixels",
            }
        )
    )


def plot_sample_images(
    dataframe: pd.DataFrame,
    sample_size: int = 5,
    random_state: int = 42,
    output_path: Path | None = None,
) -> None:
    """Показывает от 1 до 5 случайных изображений с классом и размером."""
    if sample_size < 1 or sample_size > 5:
        raise ValueError("Для лабораторной укажите sample_size от 1 до 5.")
    sample = dataframe.sample(
        n=min(sample_size, len(dataframe)),
        random_state=random_state,
    )
    if sample.empty:
        raise ValueError("Нельзя показать изображения из пустого DataFrame.")
    columns = min(3, len(sample))
    rows = (len(sample) + columns - 1) // columns
    figure, axes = plt.subplots(
        rows,
        columns,
        figsize=(4 * columns, 3.7 * rows),
        squeeze=False,
    )
    for axis, (_, record) in zip(axes.flat, sample.iterrows()):
        image_path = Path(str(record["absolute_path"]))
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            axis.set_title(f"Не удалось открыть\n{image_path.name}")
            axis.axis("off")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        axis.imshow(image)
        axis.set_title(
            f"{record['class_name']} | {image_path.name}\n"
            f"{record['width']}×{record['height']}"
        )
        axis.axis("off")
    for axis in axes.flat[len(sample):]:
        axis.axis("off")
    figure.suptitle("Примеры изображений датасета", fontsize=14)
    figure.tight_layout()
    if output_path is None:
        plt.show()
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(figure)


def main() -> None:
    """Сохраняет статистику числа пикселей и сетку примеров изображений."""
    if not DIMENSIONS_CSV.is_file():
        raise FileNotFoundError(
            f"Сначала выполните пункт 4: не найден {DIMENSIONS_CSV}"
        )
    dataframe = pd.read_csv(DIMENSIONS_CSV)
    result = add_pixel_count(dataframe)
    result.to_csv(ANALYSIS_CSV, index=False, encoding="utf-8-sig")
    statistics = group_pixel_statistics(result)
    PIXEL_STATS_CSV.parent.mkdir(parents=True, exist_ok=True)
    statistics.to_csv(PIXEL_STATS_CSV, encoding="utf-8-sig")
    print(statistics)
    plot_sample_images(
        result,
        sample_size=5,
        output_path=PLOTS_DIR / "sample_images.png",
    )


if __name__ == "__main__":
    main()
