import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Создание искусственного набора данных
data = {
    'CustomerID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'LastPurchaseDate': pd.to_datetime(['2023-10-01', '2023-09-15', '2023-08-20', '2023-10-05',
                                         '2023-07-30', '2023-09-10', '2023-06-25', '2023-10-02',
                                         '2023-05-15', '2023-09-20']),
    'Frequency': [5, 3, 2, 8, 1, 4, 2, 6, 1, 7],
    'Monetary': [500, 300, 200, 800, 100, 400, 250, 600, 150, 700]
}

df = pd.DataFrame(data)

# Установка даты анализа
analysis_date = pd.to_datetime('2023-10-10')

# Расчет RFM
rfm = df.copy()
rfm['Recency'] = (analysis_date - rfm['LastPurchaseDate']).dt.days
rfm = rfm[['CustomerID', 'Recency', 'Frequency', 'Monetary']]

# Вывод RFM
print("RFM DataFrame:")
print(rfm)

# Сегментация клиентов
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])  # Чем меньше, тем лучше
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 4, labels=[1, 2, 3, 4])  # Чем больше, тем лучше
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])  # Чем больше, тем лучше

# Общий RFM Score
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Вывод сегментации
print("\nRFM Segmentation:")
print(rfm)

# Визуализация
plt.figure(figsize=(12, 6))

# График частоты клиентов по RFM Score
sns.countplot(x='RFM_Score', data=rfm, palette='viridis')
plt.title('Частота клиентов по RFM Score')
plt.xlabel('RFM Score')
plt.ylabel('Количество клиентов')
plt.xticks(rotation=45)
plt.show()

# График средних значений по RFM
rfm[['Recency', 'Frequency', 'Monetary']].mean().plot(kind='bar', figsize=(10, 5))
plt.title('Средние значения RFM')
plt.ylabel('Среднее значение')
plt.xticks(rotation=0)
plt.show()
