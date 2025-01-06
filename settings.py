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
        ._container_gzau3_1   {display: none;}
        ._profileContainer_gzau3_53   {display: none;}
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
