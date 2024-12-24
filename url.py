import streamlit as st
import pandas as pd

# Функция для загрузки данных из ссылки
def load_data_from_url(url):
    # Чтение файла Excel из URL в DataFrame
    df = pd.read_excel(url)
    return df

# Заголовок приложения
st.title("Загрузка данных из ссылки")

# Ввод ссылки
url = st.text_input("Введите ссылку на файл Excel")

if url:
    try:
        # Загружаем данные из ссылки
        df = load_data_from_url(url)

        # Отображение DataFrame
        st.write("Содержимое файла:")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Произошла ошибка при загрузке данных: {e}")
