import numpy as np
import streamlit as st
import app1
import app2
PAGES = {
    "Dashbord": app1 ,
    "Chatbot": app2 ,
}
st.sidebar.title('Mental Health ')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()