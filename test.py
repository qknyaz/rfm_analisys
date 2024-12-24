
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Функция для обработки файла Excel
def process_excel_file(uploaded_file):
    # Чтение файла Excel в DataFrame
    df = pd.read_excel(uploaded_file)
    return df

# Заголовок приложения
st.title("Загрузка файла Excel и построение графика")



# Загрузка файла
uploaded_file = st.file_uploader("Выберите файл Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Передаем загруженный файл в функцию для обработки
    df = process_excel_file(uploaded_file)

    # Отображение DataFrame
    st.write("Содержимое файла:")
    st.dataframe(df)

    # Проверка, есть ли в DataFrame числовые данные для построения графика
    if not df.empty:
        # Предположим, что у вас есть два столбца: 'x' и 'y'
        if '1' in df.columns and 'Дальность' in df.columns:
            # Построение графика
            plt.figure(figsize=(10, 5))
            plt.plot(df['1'], df['Дальность'], marker='o')
            plt.title('График зависимости y от x')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid()

            # Отображение графика в Streamlit
            st.pyplot(plt)
        else:
            st.warning("В DataFrame должны быть столбцы 'x' и 'y' для построения графика.")
