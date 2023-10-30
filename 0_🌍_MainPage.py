import streamlit as st

# Puplic link to Camel logo: https://drive.google.com/uc?id=1_YA6DT8E2GP817VRpenvXCxSBBrhnl_C

def main():
    st.set_page_config(page_title="Home Page", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')
    st.title("Main Page")
    
    # Read CSS file to apply the style
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
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
    main()