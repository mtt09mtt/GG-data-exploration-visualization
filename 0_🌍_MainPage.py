import streamlit as st
import base64

# Magic statement to preserve widget input values across pages
st.session_state.update(st.session_state)

# Alias the Session State
ss = st.session_state

# Prepare a local image for the logo. pgn_file (100px each side) must be in same folder with this source
@st.cache_data
def myLogo(pgn_file):
    # Convert a local pgn image logo file to a base64 string
    with open(pgn_file, 'rb') as f:
        data = f.read()
        logo_base64_text = base64.b64encode(data).decode()
    return logo_base64_text

def main_entry():
    
    # Set page config
    st.set_page_config(page_title="Home Page", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')
        
    # Add local image logo into the centre-top of the sidebar and use CSS to custom the logo position
    image_logo = myLogo(r"./images/Leopard_100px.png")
    
    # Store the logo into SS for other pages (modules)
    ss.image_logo = image_logo
    
    # Style the logo
    logo_image_css = """ <style> [data-testid="stSidebar"] {
        background-image: url("data:image/png;base64,%s");
        background-repeat: no-repeat;
        background-size: 100px;
        background-position: center top;} </style> """ % image_logo
    st.markdown(logo_image_css, unsafe_allow_html=True)
    
    # Injecting custom CSS to reduce top space for the title, adjust padding-top value to move the title up - Method 2
    st.markdown("<style>div.block-container{padding-top:0.5rem;}</style>", unsafe_allow_html=True)
    
    # Page title. Use markdown to format text rather than using st.title()
    st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> Main Page </span>", unsafe_allow_html=True)
       
    # Add copyright into the sidebar
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''') 
    
    # Text in the main page
    st.markdown(
        """
        ### :green[Welcome to the exploration area]
        *The all in one place for data review and for the highlighting of the exploration prospects*   
        #### Geneal Information
        :cherry_blossom: Overview of the Blocks and Wells   
        #### Well DSTs and Tops Summary
        :cherry_blossom: Summary of the tests and the formation tops
        #### Well Log Cross-Plot
        :cherry_blossom: Review the hostest drilled/drillable prospects
        #### Prospect Review 
        :cherry_blossom: The resources for the G&G activities
    """
    )    
    
if __name__ == "__main__":
    main_entry()
    