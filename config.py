"""Настройки путей и классов лабораторной работы №4."""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
LAB01_DIR = PROJECT_DIR.parent / "lab01"
SOURCE_DATASET_DIR = LAB01_DIR / "dataset"

ANNOTATIONS_DIR = PROJECT_DIR / "annotations"
OUTPUT_DIR = PROJECT_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
PLOTS_DIR = OUTPUT_DIR / "plots"

ANNOTATION_CSV = ANNOTATIONS_DIR / "dataset_annotation.csv"
NORMALIZED_CSV = ANNOTATIONS_DIR / "normalized_columns.csv"
LABELED_CSV = ANNOTATIONS_DIR / "class_labeled.csv"
DIMENSIONS_CSV = ANNOTATIONS_DIR / "image_dimensions.csv"
ANALYSIS_CSV = ANNOTATIONS_DIR / "pixel_analysis.csv"
FILTERED_CLASS_CSV = ANNOTATIONS_DIR / "filtered_by_class.csv"
FILTERED_DIMENSIONS_CSV = ANNOTATIONS_DIR / "filtered_by_dimensions.csv"
DESCRIBE_CSV = REPORTS_DIR / "descriptive_statistics.csv"
CLASS_COUNTS_CSV = REPORTS_DIR / "class_counts.csv"
PIXEL_STATS_CSV = REPORTS_DIR / "pixel_statistics.csv"

CLASS_TO_LABEL: dict[str, int] = {"cat": 0, "dog": 1}
IMAGE_EXTENSIONS: frozenset[str] = frozenset(
    {".jpg", ".jpeg"}
)


def main() -> None:
    """Показывает настройки путей проекта."""
    print(f"Проект lab04: {PROJECT_DIR}")
    print(f"Источник изображений: {SOURCE_DATASET_DIR}")
    print(f"Источник существует: {SOURCE_DATASET_DIR.is_dir()}")


if __name__ == "__main__":
    main()
