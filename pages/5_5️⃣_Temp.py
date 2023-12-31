import streamlit as st
# import streamlit.components.v1 as sct # No need to install components

# Magic statement to preserve widget input values across pages
st.session_state.update(st.session_state)

# Alias the Session State
ss = st.session_state

# Page configuration
st.set_page_config(page_title="General", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

# Add local image logo into the centre-top of the sidebar and use CSS to custom the logo position
if "image_logo" in ss:
    image_logo = ss.image_logo # Get logo from SS that loaded and cached and stored in the Main Page
    logo_image_css = """ <style> [data-testid="stSidebar"] {
        background-image: url("data:image/png;base64,%s");
        background-repeat: no-repeat;
        background-size: 100px;
        background-position: center top;} </style> """ % image_logo
    st.markdown(logo_image_css, unsafe_allow_html=True)


# Injecting custom CSS to reduce top space for the title, adjust padding-top value to move the title up - Method 2
st.markdown("<style>div.block-container{padding-top:0.5rem;}</style>", unsafe_allow_html=True)
    
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