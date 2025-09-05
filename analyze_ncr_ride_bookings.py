# Импорт необходимых библиотек
import pandas as pd

# Шаг 1: Загрузка и первичный осмотр данных

# 1. Загрузите датасет ncr_ride_bookings.csv в DataFrame df
try:
    df = pd.read_csv('ncr_ride_bookings.csv')
    print("✅ Датасет успешно загружен.")
except FileNotFoundError:
    print("❌ Ошибка: Файл 'ncr_ride_bookings.csv' не найден!")
    print("Проверьте, что файл находится в той же папке, где запускается скрипт.")
    exit()

# === Добавляем: преобразуем Date и Time в booking_datetime ===
# Проверяем наличие необходимых столбцов
if 'Date' not in df.columns or 'Time' not in df.columns:
    print("❌ Ошибка: В файле отсутствуют столбцы 'Date' или 'Time'.")
    exit()

# Объединяем Date и Time в один datetime-столбец
df['booking_datetime'] = pd.to_datetime(
    df['Date'] + ' ' + df['Time'],
    format='%Y-%m-%d %H:%M',      # Уточните формат, если нужно (например, '%d/%m/%Y' или другой)
    errors='coerce'               # При ошибках ставим NaT
)

# Если формат не угадан — можно убрать format и оставить auto-detection
if df['booking_datetime'].isnull().all():
    # Пробуем автоматическое определение, если формат не подошёл
    df['booking_datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], errors='coerce')
    print("⚠️  Не удалось распознать формат даты. Используется автоматическое определение.")

# Проверим, сколько удалось распарсить
valid_dates = df['booking_datetime'].notna().sum()
print(f"📅 Успешно преобразовано {valid_dates} дат из {len(df)}.")

# 2. Выведите первые 5 строк датасета
print("\n" + "="*60)
print("1. Первые 5 строк датасета:")
print(df.head())

# 3. Выведите общую информацию о датасете
print("\n" + "="*60)
print("2. Общая информация о датасете:")
df.info()

# 4. Выведите статистическое описание числовых столбцов
print("\n" + "="*60)
print("3. Статистическое описание числовых столбцов:")
print(df.describe())

# 5. Определите количество строк и столбцов
print("\n" + "="*60)
print("4. Количество строк и столбцов:")
print(f"Строк: {df.shape[0]}, Столбцов: {df.shape[1]}")

# Шаг 3: Выборка и фильтрация данных
print("\n" + "="*60)
print("Шаг 3: Выборка и фильтрация данных")

# 1. Выбор столбцов: Booking ID, booking_datetime, Booking Status, Vehicle Type, Payment Method
print("1. Выбор столбцов: Booking ID, booking_datetime, Booking Status, Vehicle Type, Payment Method")

required_columns = [
    'Booking ID',
    'booking_datetime',
    'Booking Status',
    'Vehicle Type',
    'Payment Method'
]

# Проверяем, все ли нужные столбцы теперь доступны
missing_cols = [col for col in required_columns if col not in df.columns]
if missing_cols:
    print(f"❌ Ошибка: Отсутствуют столбцы: {missing_cols}")
else:
    df_selected = df[required_columns]
    print("Первые 5 строк после выборки:")
    print(df_selected.head())

# 2. Отфильтруйте бронирования со статусом "Cancelled by Driver"
print("\n" + "="*60)
print("2. Бронирования, отменённые водителем ('Cancelled by Driver'):")

if 'Booking Status' not in df.columns:
    print("❌ Ошибка: Столбец 'Booking Status' не найден.")
else:
    cancelled_by_driver = df[df['Booking Status'] == 'Cancelled by Driver']
    if cancelled_by_driver.empty:
        print("Нет записей с таким статусом.")
    else:
        print(f"Найдено {len(cancelled_by_driver)} отменённых водителем бронирований.")
        print(cancelled_by_driver[['Booking ID', 'Booking Status']].head())

# 3. Отфильтруйте бронирования с Vehicle Type = "Auto" и Booking Value > 500
print("\n" + "="*60)
print("3. Бронирования на 'Auto' с стоимостью > 500:")

if 'Vehicle Type' not in df.columns or 'Booking Value' not in df.columns:
    print("❌ Ошибка: Не хватает столбцов 'Vehicle Type' или 'Booking Value'.")
else:
    # Преобразуем Booking Value в числовой тип
    df['Booking Value'] = pd.to_numeric(df['Booking Value'], errors='coerce')
    auto_high_value = df[(df['Vehicle Type'] == 'Auto') & (df['Booking Value'] > 500)]
    if auto_high_value.empty:
        print("Нет таких бронирований.")
    else:
        print(f"Найдено {len(auto_high_value)} бронирований.")
        print(auto_high_value[['Booking ID', 'Vehicle Type', 'Booking Value']].head())

# 4. Отфильтруйте бронирования за март 2024 года
print("\n" + "="*60)
print("4. Бронирования в марте 2024 года (с 2024-03-01 по 2024-03-31):")

if 'booking_datetime' not in df.columns or df['booking_datetime'].isnull().all():
    print("❌ Ошибка: Столбец 'booking_datetime' пуст или не создан.")
else:
    start_date = '2024-03-01'
    end_date = '2024-03-31'
    march_2024 = df[
        (df['booking_datetime'] >= start_date) &
        (df['booking_datetime'] <= end_date)
    ]
    if march_2024.empty:
        print("Нет бронирований за этот период.")
    else:
        print(f"Найдено {len(march_2024)} бронирований в марте 2024.")
        print(march_2024[['Booking ID', 'booking_datetime', 'Booking Status']].head())