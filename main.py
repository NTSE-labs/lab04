"""Точка входа для последовательного запуска всех пунктов лабораторной №4."""

import pandas as pd

from class_filter import filter_by_class
from class_labels import add_numeric_class_labels, save_labeled_dataframe
from column_names import normalize_column_names, save_normalized_dataframe
from config import (
    ANALYSIS_CSV,
    ANNOTATION_CSV,
    ANNOTATIONS_DIR,
    DIMENSIONS_CSV,
    FILTERED_CLASS_CSV,
    FILTERED_DIMENSIONS_CSV,
    LABELED_CSV,
    NORMALIZED_CSV,
    PIXEL_STATS_CSV,
    PLOTS_DIR,
    REPORTS_DIR,
    SOURCE_DATASET_DIR,
)
from data_statistics import (
    is_dataset_balanced,
    plot_class_distribution,
    save_statistics,
)
from dataset_annotation import create_annotation_dataframe, save_annotation
from dimension_filter import filter_by_class_and_dimensions
from image_histogram import (
    calculate_random_image_histogram,
    save_histogram_arrays,
)
from image_metadata import add_image_dimensions, save_dimensions_dataframe
from pixel_statistics import (
    add_pixel_count,
    group_pixel_statistics,
    plot_sample_images,
)
from plot_histograms import plot_color_histograms


def main() -> None:
    """Выполняет пункты 1–10 и сохраняет таблицы, отчёты и графики."""
    if not SOURCE_DATASET_DIR.is_dir():
        raise FileNotFoundError(
            "Не найдена папка lab01/dataset. Ожидаемый путь: "
            f"{SOURCE_DATASET_DIR}"
        )

    for directory in (ANNOTATIONS_DIR, REPORTS_DIR, PLOTS_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    print("Создание исходной аннотации.")
    dataframe = create_annotation_dataframe()
    save_annotation(dataframe, ANNOTATION_CSV)
    print(f"Сохранено изображений: {len(dataframe)}")

    print("Проверка и нормализация названий колонок.")
    dataframe = normalize_column_names(dataframe)
    save_normalized_dataframe(dataframe, NORMALIZED_CSV)

    print("Добавление числовых меток классов.")
    dataframe = add_numeric_class_labels(dataframe)
    save_labeled_dataframe(dataframe, LABELED_CSV)

    print("Получение размеров изображений.")
    dataframe = add_image_dimensions(dataframe)
    save_dimensions_dataframe(dataframe, DIMENSIONS_CSV)
    dataframe = pd.read_csv(DIMENSIONS_CSV)

    print("Описательная статистика и баланс классов.")
    describe_table, counts_table = save_statistics(dataframe)
    print(describe_table)
    print(counts_table)
    print(f"Набор сбалансирован: {is_dataset_balanced(dataframe)}")
    plot_class_distribution(dataframe, PLOTS_DIR / "class_distribution.png")

    print("Фильтрация по классу.")
    filtered_class = filter_by_class(dataframe, "cat")
    filtered_class.to_csv(
        FILTERED_CLASS_CSV,
        index=False,
        encoding="utf-8-sig",
    )
    print(f"Изображений cat: {len(filtered_class)}")

    print("Фильтрация по классу и размерам.")
    filtered_dimensions = filter_by_class_and_dimensions(
        dataframe,
        class_label="cat",
        max_width=800,
        max_height=600,
    )
    filtered_dimensions.to_csv(
        FILTERED_DIMENSIONS_CSV,
        index=False,
        encoding="utf-8-sig",
    )
    print(f"Изображений cat до 800×600: {len(filtered_dimensions)}")

    print("Статистика количества пикселей и примеры изображений.")
    pixel_dataframe = add_pixel_count(dataframe)
    pixel_dataframe.to_csv(ANALYSIS_CSV, index=False, encoding="utf-8-sig")
    pixel_stats = group_pixel_statistics(pixel_dataframe)
    PIXEL_STATS_CSV.parent.mkdir(parents=True, exist_ok=True)
    pixel_stats.to_csv(PIXEL_STATS_CSV, encoding="utf-8-sig")
    print(pixel_stats)
    plot_sample_images(
        pixel_dataframe,
        sample_size=5,
        output_path=PLOTS_DIR / "sample_images.png",
    )

    print("Вычисление гистограмм случайных изображений.")
    for class_name in ("cat", "dog"):
        histograms = calculate_random_image_histogram(
            pixel_dataframe,
            class_name,
        )
        save_histogram_arrays(histograms, class_name)

    print("Сохранение графиков гистограмм.")
    from plot_histograms import load_histogram_arrays

    for class_name in ("cat", "dog"):
        plot_color_histograms(
            load_histogram_arrays(class_name),
            class_name,
            PLOTS_DIR / f"{class_name}_histograms.png",
        )

    print("\nРабота завершена.")
    print(f"Аннотация: {ANNOTATION_CSV}")
    print(f"Таблица с размерами: {DIMENSIONS_CSV}")
    print(f"Таблица пикселей: {ANALYSIS_CSV}")
    print(f"Отчёты: {REPORTS_DIR}")
    print(f"Графики: {PLOTS_DIR}")


if __name__ == "__main__":
    main()
