import streamlit as st
import pandas as pd
from welltop_plot_class import MtPlot # This class can be imported from mtlib.py module as well
import extra_streamlit_components as stx

st.set_page_config(page_title="DSTs and TOPs", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

# Add local image logo into the centre-top of the sidebar and use CSS to custom the logo position
image_logo = st.session_state.image_logo # Get logo from SS that loaded and cached and stored in the Main Page
logo_image_css = """ <style> [data-testid="stSidebar"] {
    background-image: url("data:image/png;base64,%s");
    background-repeat: no-repeat;
    background-size: 100px;
    background-position: center top;} </style> """ % image_logo
st.markdown(logo_image_css, unsafe_allow_html=True)

# Injecting custom CSS to reduce top space for the title, adjust padding-top value to move the title up - Method 2
st.markdown("<style>div.block-container{padding-top:0.5rem;}</style>", unsafe_allow_html=True)

# Page title. Dont use st.title()
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> Well DSTs and Tops </span>", unsafe_allow_html=True)
    
# Create some tabs by using stx
tab_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="✍️ Plot well Tops and DSTs", description=None),
    stx.TabBarItemData(id="tab2", title="✍️ Data file example", description=None),
    stx.TabBarItemData(id="tab3", title="✍️ Help", description=None),
    stx.TabBarItemData(id="tab4", title="✍️ About", description=None)])

@st.cache_data # Load data, cache and store into Session State(SS)
def load_data(uploaded_file):
    if uploaded_file:
        
        # Read only sheets named "well_top" and "well_dst"
        df_well_top = pd.read_excel(uploaded_file, sheet_name="well_top")
        df_well_dst = pd.read_excel(uploaded_file, sheet_name="well_dst")
        
        # Sort the dataframes
        df_well_top = df_well_top.sort_values(["well_name", "surface_md_m"], ascending = [True, True])
        df_well_dst = df_well_dst.sort_values(["well_name", "dst_number"], ascending = [True, True])
        
        # Get unique blocks and wells
        unique_well_top = df_well_top["well_name"].unique().tolist()
        unique_well_dst = df_well_dst["well_name"].unique().tolist()
        file_loaded = True
        
        # Store data into SS
        st.session_state.df_well_top = df_well_top
        st.session_state.df_well_dst = df_well_dst
        st.session_state.unique_well_top = unique_well_top
        st.session_state.unique_well_dst = unique_well_dst
        st.session_state.file_loaded = file_loaded
   
# Main body
def main_stuff():     
    
    # Initialize current_well_has_top and current_well_has_dst in SS
    if "current_well_has_top" not in st.session_state:
        st.session_state.current_well_has_top = st.session_state.unique_well_top[0]
    if "current_well_has_dst" not in st.session_state:
        st.session_state.current_well_has_dst = st.session_state.unique_well_dst[0]
      
    # Input from user or get the items from SS
    selected_well_has_top = st.sidebar.selectbox("Well with tops 🔎", st.session_state.unique_well_top,
                                                 index=st.session_state.unique_well_top.index(st.session_state.current_well_has_top))
    st.session_state.current_well_has_top = selected_well_has_top
    
    
    selected_well_has_dst = st.sidebar.selectbox("Well with DSTs 🔎", st.session_state.unique_well_dst,
                                                 index=st.session_state.unique_well_dst.index(st.session_state.current_well_has_dst))
    st.session_state.current_well_has_dst = selected_well_has_dst
    
    # Create 2 columns below above row in the Main page
    col1, col2 = st.columns(2)
    
    # Place widgets in col1
    with col1:
        
        # Setup range of the depth
        depth_range1 = st.slider("👉 Select depth range for Tops", value = [500.0, 5500.0])
        
        # Create a dataframe for plotting tops
        show_df1 = st.session_state.df_well_top[st.session_state.df_well_top["well_name"] == st.session_state.current_well_has_top]
        show_df1 = show_df1.sort_values(by="surface_md_m", ascending=True)
                
        # Call well_top function from MtPlot class in mtlib.py module
        my_fig = MtPlot.well_top(show_df1, depth_range1[0], depth_range1[1], 1, 3)
                        
        # Show the matplotlib plot on col2
        st.pyplot(my_fig)
        
        # Show the data as a table
        df1a = show_df1.iloc[:, 1:]
        df1a = df1a.reset_index(drop=True)
        #st.write(df1a) # This code also worked
        st.dataframe(df1a, width=640, height=350)
        
    # Place widgets in col2
    with col2:
        
        # Setup range of the depth
        depth_range2 = st.slider("👉 Select depth range for DSTs", value = [500.0, 5500.0])
        
        # Create a dataframe for plotting dsts
        show_df2 = st.session_state.df_well_dst[st.session_state.df_well_dst["well_name"] == st.session_state.current_well_has_dst]
                
        # Call well_top function from MtPlot class in mtlib.py module
        my_fig = MtPlot.well_dst(show_df2, depth_range2[0], depth_range2[1], 3, 4, 2)
               
        # Show the matplotlib plot on col2
        st.pyplot(my_fig)
        
        # Show the data as a table
        df2a = show_df2.iloc[:, 2:]
        #st.write(df2a)
        st.dataframe(df2a, width=640, height=350)
        
def main_entry():
    text_message = ''':rainbow[Please select and load an Excel data file - 
    The file must has two sheets named "well_top" and "well_dst". Select the first task above to begin]:hibiscus:'''
    
    # Use match case statement to execute the tab   
    match tab_id:
        case "tab1":
            try:
                if "file_loaded" not in st.session_state:
                    # Create a file uploader widget
                    uploaded_file = st.sidebar.file_uploader("Please select a Exel data file", type=["xls", "xlsx"], accept_multiple_files=False)           
                    # load_excel data file
                    load_data(uploaded_file)
                if "file_loaded" in st.session_state:
                    main_stuff()
                    text_message = ''':rainbow[Please select a desired TAB for more information]:hibiscus:'''
            except Exception as e:
                st.write(e)

        case "tab2":
            st.write("Welcome to the Data file example TAB")
            text_message = ''':rainbow[Please select a desired TAB above for more information]:hibiscus:'''
        case "tab3":
            st.write("Welcome to the Help TAB")
            text_message = ''':rainbow[Please select a desired TAB above for more information]:hibiscus:'''
        case "tab4":
            st.write("Welcome to the About TAB")
            text_message = ''':rainbow[Please select a desired TAB above for more information]:hibiscus:'''
    
    st.markdown(text_message)
        
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''')
        
    
if __name__ == "__main__":
    main_entry()