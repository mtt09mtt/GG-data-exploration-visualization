import streamlit as st

# Config the page
st.set_page_config(page_title="General", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

# Read CSS file to apply the style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    

def main_entry():
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''') 

    
    
if __name__ == "__main__":
    main_entry()
      
'''
1) Explore well log data by stremlit-pandas and pygwalker packages
2) Explore well information from well shapefile by streamlit-pandas package
3) HTML 5 and CSS and MARKDOWN

'''