import streamlit as st

st.set_page_config(page_title="Prospect", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

# Add local image logo into the centre-top of the sidebar and use CSS to custom the logo position
if "image_logo" in st.session_state:
    image_logo = st.session_state.image_logo # Get logo from SS that loaded and cached and stored in the Main Page
    logo_image_css = """ <style> [data-testid="stSidebar"] {
        background-image: url("data:image/png;base64,%s");
        background-repeat: no-repeat;
        background-size: 100px;
        background-position: center top;} </style> """ % image_logo
    st.markdown(logo_image_css, unsafe_allow_html=True)


# Injecting custom CSS to reduce top space for the title, adjust padding-top value to move the title up - Method 2
st.markdown("<style>div.block-container{padding-top:0.5rem;}</style>", unsafe_allow_html=True)

# Custom color using HTML tag and use markdown rather than st.title()
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> Prospect </span>", unsafe_allow_html=True)

st.write("The page is under construction")

# Add copyright into the sidebar
st.sidebar.markdown(''' Created with ❤️ by My Thang ''')

def main_entry():
    pass

if __name__ == "__main__":
    main_entry()