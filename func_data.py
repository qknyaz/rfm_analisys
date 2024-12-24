import io

from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np


def hist(df: DataFrame):
    # Настройка стиля графика
    sns.set(style="whitegrid")

    # Получение количества строк и столбцов
    rows, columns = df.shape
    # Определение количества бинов по правилу Стурджеса
    bins = int(1 + np.log2(rows))

    # Построение гистограммы
    plt.figure(figsize=(8, 6))
    sns.histplot(
        df["Суммарно покупок"],
        bins=bins,
        kde=True,
    )  # kde=True добавляет линию плотности

    plt.title("Гистограмма значений")
    plt.xlabel("Сумма")
    plt.ylabel("Количество клиентов")
    st.pyplot(plt)


def boxplot(df: DataFrame):
    sns.boxplot(x="Суммарно покупок", y="Покупатель", data=df)
    plt.title("Боксплот значений по категориям")
    plt.xlabel("Категория")
    plt.ylabel("Значения")

    # Отображение графика в Streamlit
    st.pyplot(plt)


def circular_diagram(df: DataFrame):
    # Построение круговой диаграммы
    plt.figure(figsize=(8, 8))
    plt.pie(
        df["Значения"],
        labels=df["Категория"],
        autopct="%1.1f%%",
        startangle=90,
        shadow=0,
        radius=0.7,
    )
    plt.title("Распределение клиентов по категориям")
    plt.axis("equal")  # Чтобы круговая диаграмма была кругом

    # Отображение графика в Streamlit
    st.pyplot(plt)


def circle_diagram_2(df: DataFrame):
    plt.gcf().set_size_inches(12, 12)
    sns.set_style("darkgrid")

    # Установка максимального значения

    max_val = max(df["Значения"]) * 1.01
    ax = plt.subplot(projection="polar")

    # Зададим внутренний график

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(1)
    ax.set_rlabel_position(0)
    ax.set_thetagrids([], labels=[])
    ax.set_rgrids(range(len(df)), labels=df["Категория"])

    st.pyplot(plt)


def scatter(df):
    sns.set(font_scale=1.3)
    sns.scatterplot(
        y="Кол-во покупок",
        x="Суммарно покупок",
        data=df,
    )
    plt.ylabel("Клиенты")
    plt.xlabel("Сумма")
    st.pyplot(plt)


@st.cache_data
def convert_df(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    return buffer.getvalue()
