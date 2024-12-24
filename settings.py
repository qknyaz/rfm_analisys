import streamlit as st


def settings():
    st.set_page_config(
        page_title="RFM анализ",
        # layout="wide",
    )

    st.markdown(
        """
        <style>
        .stAppHeader  {display: none;}
        .stMainBlockContainer {padding-top: 1rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # html_code = """
    # <script>
    #   var element = document.getElementsByClassName("stAppHeader");
    #     elements[0].remove();
    # </script>
    # """
    # st.markdown(html_code, unsafe_allow_html=True)
