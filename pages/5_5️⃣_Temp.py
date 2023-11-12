import streamlit as st

# Config the page
st.set_page_config(page_title="General", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

# Add local image logo into the centre-top of the sidebar and use CSS to custom the logo position
image_logo = st.session_state["image_logo"] # Get logo from SS that loaded and cached and stored in the Main Page
logo_image_css = """ <style> [data-testid="stSidebar"] {
    background-image: url("data:image/png;base64,%s");
    background-repeat: no-repeat;
    background-size: 100px;
    background-position: 100px 5px;} </style> """ % image_logo
st.markdown(logo_image_css, unsafe_allow_html=True)


# Injecting custom CSS to reduce top space for the title, adjust padding-top value to move the title up
custom_css = """ <style> .block-container.st-emotion-cache-z5fcl4.ea3mdgi4 {padding-top: 30px;} </style> """
st.markdown(custom_css, unsafe_allow_html=True)
    
# Page title. Dont use st.title()
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> Temporary </span>", unsafe_allow_html=True)

# Add copyright into the sidebar
st.sidebar.markdown(''' Created with ❤️ by My Thang ''') 

def main_entry():
    pass
    
  
if __name__ == "__main__":
    main_entry()
      
'''
1) Explore well log data by stremlit-pandas and pygwalker packages
2) Explore well information from well shapefile by streamlit-pandas package
3) Heatmap matrix of the curves in a well. Need clean up the abnormal values
4) HTML 5 and CSS and MARKDOWN


'''