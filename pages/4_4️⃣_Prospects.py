import streamlit as st

st.set_page_config(page_title="Prospect", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')
st.title("Prospects")

# Read CSS file to apply the style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.markdown(''' Created with ❤️ by My Thang ''')