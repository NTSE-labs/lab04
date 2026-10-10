# Лабораторная работа №4 — исследовательский анализ и визуализация данных

## Выбор датасета

Используется датасет из лабы 1:

```text
../lab01/dataset/
├── cat/
└── dog/
```

## Установка и запуск в Windows PowerShell

Открой папку `lab04` в IDE:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Запустить main:

```powershell
python main.py
```

Запустить notebook:

```powershell
jupyter notebook
```
Или открыть notebook.ipynb и запускать все по порядку сверху вниз

## Результат

1. `dataset_annotation.py` формирует DataFrame и CSV с колонками `class_name`, `absolute_path`.
2. Имена колонок уже соответствуют английскому `snake_case`.
3. `image_metadata.py` добавляет `class_label`: `cat=0`, `dog=1`.
4. Там же добавляются `height`, `width`, `channels`.
5. `data_statistics.py` использует `DataFrame.describe()`, создаёт таблицу подсчёта изображений по классам и график баланса.
6. `data_filters.py`: `filter_by_class(dataframe, class_label)`.
7. `data_filters.py`: `filter_by_class_and_dimensions(dataframe, class_label, max_width, max_height)`.
8. `pixel_count = width * height`; группировка по классам вычисляет max/min/mean, `plot_sample_images()` показывает 3–5 изображений.
9. `image_visualization.py`: `calculate_random_image_histogram()` случайно выбирает доступное изображение класса и возвращает три массива гистограмм B, G, R.
10. `plot_color_histograms()` строит график с подписями осей и каналов.
