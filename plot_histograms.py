"""Отрисовка гистограмм цветовых каналов через Matplotlib."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from config import PLOTS_DIR, REPORTS_DIR


def plot_color_histograms(
    histograms: tuple[np.ndarray, np.ndarray, np.ndarray],
    class_label: str | int,
    output_path: Path | None = None,
) -> None:
    """Рисует B-, G- и R-гистограммы с заголовком и подписями осей."""
    channel_names = ("Синий (B)", "Зелёный (G)", "Красный (R)")
    figure, axis = plt.subplots(figsize=(9, 5))
    for histogram, channel_name in zip(histograms, channel_names):
        axis.plot(np.arange(256), histogram, label=channel_name)
    axis.set_title(f"Гистограммы цветовых каналов — класс {class_label}")
    axis.set_xlabel("Значение интенсивности пикселя (0–255)")
    axis.set_ylabel("Количество пикселей")
    axis.set_xlim(0, 255)
    axis.legend()
    axis.grid(alpha=0.2)
    figure.tight_layout()
    if output_path is None:
        plt.show()
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(figure)


def load_histogram_arrays(
    class_label: str,
    reports_dir: Path = REPORTS_DIR,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Загружает ранее сохранённые три массива гистограмм для класса."""
    input_path = reports_dir / f"{class_label}_histograms.npz"
    if not input_path.is_file():
        raise FileNotFoundError(
            f"Не найдены массивы гистограмм: {input_path}. "
            "Сначала выполните пункт 9."
        )
    with np.load(input_path) as data:
        return data["blue"], data["green"], data["red"]


def main() -> None:
    """Строит и сохраняет графики гистограмм для обоих классов."""
    for class_name in ("cat", "dog"):
        histograms = load_histogram_arrays(class_name)
        output_path = PLOTS_DIR / f"{class_name}_histograms.png"
        plot_color_histograms(histograms, class_name, output_path)
        print(f"Сохранён график: {output_path}")


if __name__ == "__main__":
    main()
