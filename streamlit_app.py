import streamlit as st
import pandas as pd
from func_data import hist, boxplot, circular_diagram, scatter, convert_df
from txt_const import drop_columns
import matplotlib.pyplot as plt
from settings import settings
import seaborn as sns

settings()


# Заголовок приложения
st.markdown("### RFM анализ ваших клиентов.")
st.warning(
    """Файл должен состоять из колонок:
    **Покупатель** (Информация о лице или компании), 
    **Дата** (Даты покупок в формате "дд.мм.гггг"), 
    **Сумма** (покупка на данную дату)""",
    icon="⚠️",
)

# Загрузка файла
uploaded_file = st.file_uploader("Выберите файл Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Чтение файла Excel в DataFrame
    df = pd.read_excel(uploaded_file)

    # определение переменных для колонок покупатель, дата, сумма
    c_buyer, c_date, c_money = df.columns
    df[c_date] = pd.to_datetime(df[c_date], errors="coerce")

    st.markdown("### Результат анализа")

    # Группируем данные по столбцу 'Покупатель -> Сумма' и вычисляем сумму значений
    agg_results = (
        df.groupby(c_buyer)[c_money].agg(["count", "sum", "max"]).reset_index()
    )

    # Группируем данные по столбцу 'Покупатель -> Дата' и вычисляем сумму значений
    agg_result_d = df.groupby(c_buyer)[c_date].max().reset_index()
    agg_results["Последняя покупка"] = agg_result_d[c_date].dt.date

    # Слияние двух дата <-> фреймов
    merged_df = pd.merge(agg_results, agg_result_d, on=c_buyer)

    # создание колонки F (частота)
    c = "count"
    merged_df["F (частота)"] = merged_df[c].apply(
        lambda x: (
            1
            if x < merged_df[c].mean() * 2 / 3
            else (3 if x > merged_df[c].mean() * 4 / 3 else 2)
        )
    )
    # Создание колонки R (давность) с категорией
    merged_df["R (давность)"] = merged_df["Дата"].apply(
        lambda x: (
            1
            if x < (df[c_date].max() - df[c_date].min()) / 3 + df[c_date].min()
            else (
                3
                if x > (df[c_date].max() - (df[c_date].max() - df[c_date].min()) / 3)
                else 2
            )
        )
    )

    merged_df["M (чек)"] = merged_df["sum"].apply(
        lambda x: (
            1
            if x < merged_df["sum"].median() * 2 / 3
            else (3 if x > merged_df["sum"].median() * 4 / 3 else 2)
        )
    )

    # агрегация показателей в цифровой код
    merged_df["Код"] = (
        merged_df["F (частота)"] * 100
        + merged_df["R (давность)"] * 10
        + merged_df["M (чек)"] * 1
    )

    merged_df.rename(
        columns={
            "count": "Кол-во покупок",
            "sum": "Суммарно покупок",
        },
        inplace=True,
    )

    # --------------------------------------------------
    # Сегментация данных на потерянных, в риске потерь, активных
    # --------------------------------------------------
    outflow = merged_df[merged_df["Код"] < 222].reset_index().drop(columns=drop_columns)

    losing_client = (
        merged_df[(222 <= merged_df["Код"]) & (merged_df["Код"] < 322)]
        .reset_index()
        .drop(columns=drop_columns)
    )

    activ_client = (
        merged_df[merged_df["Код"] >= 322].reset_index().drop(columns=drop_columns)
    )
    # ===================================================

    # Создаем вкладки
    tabs = st.tabs(
        [
            ":red[Потерянные клиенты]",
            ":blue[Риск потери клиентов]",
            ":green[Активные клиенты]",
        ],
    )
    # Содержимое первой вкладки
    with tabs[0]:
        st.markdown(
            f"### :red[Потерянные клиенты - {outflow.shape[0]} шт.]",
            # help="это датафрейм",
        )
        st.dataframe(outflow)

        st.download_button(
            label="Скачать данные в формате Excel",
            data=convert_df(outflow),
            file_name="данные потерянных клиентов.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            # help="""Это кнопка""",
        )

        hist(df=outflow)

    # Содержимое второй вкладки
    with tabs[1]:
        st.markdown(f"### :blue[Риск потери клиентов - {losing_client.shape[0]} шт.]")
        st.dataframe(losing_client)
        st.download_button(
            label="Скачать данные в формате Excel",
            data=convert_df(losing_client),
            file_name="данные риск-потерянных клиентов.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        hist(df=losing_client)

    # Содержимое третьей вкладки
    with tabs[2]:
        st.markdown(f"### :green[Активные клиенты - {activ_client.shape[0]} шт.]")
        st.dataframe(activ_client)
        st.download_button(
            label="Скачать данные в формате Excel",
            data=convert_df(activ_client),
            file_name="данные активных клиентов.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        hist(df=activ_client)

    data_for_pie = {
        "Категория": [
            f"Потерянные {outflow['Суммарно покупок'].sum():,.0f} \u20BD",
            f"Риск {losing_client['Суммарно покупок'].sum():,.0f} \u20BD",
            f"Активные {activ_client['Суммарно покупок'].sum():,.0f} \u20BD",
        ],
        "Значения": [
            outflow.shape[0],
            losing_client.shape[0],
            activ_client.shape[0],
        ],
    }  # \u20BD - символ рубля

    pie_df = pd.DataFrame(data_for_pie)
    circular_diagram(pie_df)
