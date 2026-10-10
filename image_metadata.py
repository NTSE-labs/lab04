"""Получение высоты, ширины и числа каналов изображений."""

from pathlib import Path

import cv2
import pandas as pd

from config import DIMENSIONS_CSV, LABELED_CSV


def get_image_properties(image_path: Path) -> tuple[int, int, int]:
    """Возвращает высоту, ширину и количество каналов изображения."""
    image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"OpenCV не смог прочитать изображение: {image_path}")
    height, width = image.shape[:2]
    channels = 1 if image.ndim == 2 else image.shape[2]
    return int(height), int(width), int(channels)


def add_image_dimensions(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Добавляет в DataFrame колонки height, width и channels."""
    result = dataframe.copy()
    heights: list[int] = []
    widths: list[int] = []
    channels_list: list[int] = []
    for raw_path in result["absolute_path"]:
        height, width, channels = get_image_properties(Path(str(raw_path)))
        heights.append(height)
        widths.append(width)
        channels_list.append(channels)
    result["height"] = heights
    result["width"] = widths
    result["channels"] = channels_list
    return result


def save_dimensions_dataframe(
    dataframe: pd.DataFrame,
    output_path: Path = DIMENSIONS_CSV,
) -> None:
    """Сохраняет DataFrame с характеристиками изображений в CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    """Добавляет размеры изображений к DataFrame с числовыми метками."""
    if not LABELED_CSV.is_file():
        from class_labels import main as create_labels

        create_labels()
    dataframe = pd.read_csv(LABELED_CSV)
    result = add_image_dimensions(dataframe)
    save_dimensions_dataframe(result)
    print(f"Сохранён файл: {DIMENSIONS_CSV}")
    print(result.head())


if __name__ == "__main__":
    main()
