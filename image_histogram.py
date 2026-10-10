"""Расчёт гистограмм цветовых каналов случайного изображения."""

from pathlib import Path

import cv2
import numpy as np
import pandas as pd

from class_filter import filter_by_class
from config import DIMENSIONS_CSV, REPORTS_DIR


def calculate_random_image_histogram(
    dataframe: pd.DataFrame,
    class_label: str | int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Возвращает R-, G- и B-гистограммы случайного изображения класса."""
    class_dataframe = filter_by_class(dataframe, class_label)
    if class_dataframe.empty:
        raise ValueError(
            f"В DataFrame нет изображений класса {class_label!r}."
        )

    rng = np.random.default_rng()
    for row_index in rng.permutation(len(class_dataframe)):
        image_path = Path(
            str(class_dataframe.iloc[int(row_index)]["absolute_path"])
        )
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is None:
            continue

        histograms = tuple(
            cv2.calcHist([image], [channel], None, [256], [0, 256]).flatten()
            for channel in range(3)
        )
        return histograms[0], histograms[1], histograms[2]

    raise ValueError(
        f"Не удалось прочитать ни одно изображение класса {class_label!r}."
    )


def save_histogram_arrays(
    histograms: tuple[np.ndarray, np.ndarray, np.ndarray],
    class_label: str,
    output_dir: Path = REPORTS_DIR,
) -> Path:
    """Сохраняет три массива гистограмм в NPZ для следующего пункта."""
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{class_label}_histograms.npz"
    np.savez(
        output_path,
        blue=histograms[0],
        green=histograms[1],
        red=histograms[2],
    )
    return output_path


def main() -> None:
    """Считает гистограммы классов cat и dog и сохраняет массивы."""
    if not DIMENSIONS_CSV.is_file():
        raise FileNotFoundError(
            f"Сначала выполните пункт 4: не найден {DIMENSIONS_CSV}"
        )
    dataframe = pd.read_csv(DIMENSIONS_CSV)
    for class_name in ("cat", "dog"):
        histograms = calculate_random_image_histogram(dataframe, class_name)
        output_path = save_histogram_arrays(histograms, class_name)
        print(f"Гистограммы класса {class_name} сохранены: {output_path}")


if __name__ == "__main__":
    main()
