"""Формирование исходной CSV-аннотации датасета."""

from pathlib import Path

import pandas as pd

from config import (
    ANNOTATION_CSV,
    ANNOTATIONS_DIR,
    CLASS_TO_LABEL,
    IMAGE_EXTENSIONS,
    SOURCE_DATASET_DIR,
)


def find_image_files(dataset_dir: Path) -> list[Path]:
    """Возвращает отсортированный список файлов изображений в датасете."""
    if not dataset_dir.is_dir():
        raise FileNotFoundError(
            f"Не найдена папка исходного датасета: {dataset_dir}"
        )
    return sorted(
        path
        for path in dataset_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def get_class_name(image_path: Path, dataset_dir: Path) -> str:
    """Определяет название класса по первой подпапке датасета."""
    relative_path = image_path.resolve().relative_to(dataset_dir.resolve())
    if len(relative_path.parts) < 2:
        raise ValueError(
            f"Изображение должно находиться в подпапке класса: {image_path}"
        )
    return relative_path.parts[0]


def create_annotation_dataframe(
    dataset_dir: Path = SOURCE_DATASET_DIR,
) -> pd.DataFrame:
    """Создаёт DataFrame из названия класса и абсолютного пути к файлу."""
    rows: list[dict[str, str]] = []
    for image_path in find_image_files(dataset_dir):
        rows.append(
            {
                "class_name": get_class_name(image_path, dataset_dir),
                "absolute_path": str(image_path.resolve()),
            }
        )
    dataframe = pd.DataFrame(
        rows,
        columns=["class_name", "absolute_path"],
    )
    if dataframe.empty:
        raise ValueError(f"В папке {dataset_dir} не найдены изображения.")
    unknown_classes = sorted(
        set(dataframe["class_name"]) - set(CLASS_TO_LABEL)
    )
    if unknown_classes:
        raise ValueError(
            "В датасете найдены классы, не указанные в CLASS_TO_LABEL: "
            f"{unknown_classes}"
        )
    return dataframe


def save_annotation(
    dataframe: pd.DataFrame,
    output_path: Path = ANNOTATION_CSV,
) -> None:
    """Сохраняет двухколоночную аннотацию в CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    """Создаёт и сохраняет CSV-аннотацию исходных изображений."""
    ANNOTATIONS_DIR.mkdir(parents=True, exist_ok=True)
    dataframe = create_annotation_dataframe()
    save_annotation(dataframe)
    print(f"Создана аннотация: {ANNOTATION_CSV}")
    print(f"Количество изображений: {len(dataframe)}")
    print(dataframe.head())


if __name__ == "__main__":
    main()
