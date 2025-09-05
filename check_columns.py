import pandas as pd

# Загружаем данные
df = pd.read_csv('ncr_ride_bookings.csv')

# Выводим все названия столбцов
print(df.columns.tolist())