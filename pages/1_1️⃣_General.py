import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import tempfile

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

# Injecting custom CSS to reduce top space of the title, adjust padding-top value to move the title up - Method 2
st.markdown("<style>div.block-container{padding-top:0.5rem;}</style>", unsafe_allow_html=True)

# Page title. Dont use st.title()
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> General </span>", unsafe_allow_html=True)

# Create some tabs
tab1, tab2, tab3, tab4 = st.tabs(["✍️ General Basemap", "✍️ Well Information", "✍️ Help", "✍️ About"])

# Create a button holder in order to delete the button after file loaded successfully
files_uploader_holder = st.sidebar.empty()  

# Key information of well for the Popup
popup_fields = ["TD_M", "STATUS", "RESULT", "NOTES", "COMPLETED"]

# Define style of basemap
def basemap_style(feature):
    # return {"fillColor": None, "color": "black", "weight": 1, "dashArray": "5, 5",}
    return {"fillColor": None, "color": "grey", "weight": 0.5,}

# Define style of the selected block label 
def selected_block_style(feature):
    return {"fillColor": "yellow", "color": "grey", "weight": 0.5,}

# Define icon for wells 
def well_label_style(feature):
    # Note: transform is to setup position of the well name to the well icon
    mt_icon = folium.DivIcon(html = f"""<div style="font-family: Arial; color: blue; font-size=9px; transform: translate(-250%, 50%);
                                          white-space:nowrap;">{feature}</div>""")
    return mt_icon
 
# Loading, caching and storing data into SS
@st.cache_data
def load_block_data(uploaded_files):  
    
    # Check if files are uploaded
    if uploaded_files:
        # Create a temporary directory using tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            for uploaded_file in uploaded_files:
                # Write out each uploaded file to the temporary directory
                with open(os.path.join(tmp_dir, uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
            # Read the shapefile from the temporary directory using geopandas
            vnBlocks_gdf = gpd.read_file(os.path.join(tmp_dir, [file.name for file in uploaded_files if ".shp" in file.name][0]))
            file_name1 = uploaded_files[0].name
            vnBlocks_loaded = True  
            # st.write("📣 :rainbow[Block shapefiles loaded, cached and stored in Session State!]")
            return vnBlocks_gdf, file_name1, vnBlocks_loaded

@st.cache_data
def load_well_data(uploaded_files):  
           
    # Check if files are uploaded
    if uploaded_files:
        # Create a temporary directory using tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            for uploaded_file in uploaded_files:
                # Write out each uploaded file to the temporary directory
                with open(os.path.join(tmp_dir, uploaded_file.name), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
            # Read the shapefile from the temporary directory using geopandas
            vnWells_gdf = gpd.read_file(os.path.join(tmp_dir, [file.name for file in uploaded_files if ".shp" in file.name][0]))
            file_name2 = uploaded_files[0].name
            vnWells_loaded = True
            # st.write("📣 :rainbow[Well shapefiles loaded, cached and stored in Session State!]")
            return vnWells_gdf, file_name2, vnWells_loaded    
        
# Get user input from sidebar
def get_user_input():
       
    # User input of block
    selected_block = st.sidebar.selectbox(f"📣 Found {ss.number_of_blocks} Blocks in total - 👉 Please select a Block", 
                                          ss.list_of_blocks, key = "tab1_block")
    
    # List of wells in the selected block
    list_of_wells = ss.vnWells_df[ss.vnWells_df["BLOCK_NAME"]==selected_block] 
    number_of_wells = len(list_of_wells)
    
    # User input of wells        
    selected_wells = st.sidebar.multiselect(f"📣 Found {number_of_wells} Wells in the Block -👉 Please select a Well", 
                                            list_of_wells, key = "tab1_wells")
    
    # Store the input into SS
    ss.selected_block = selected_block
    ss.list_of_wells = list_of_wells
    ss.number_of_wells = number_of_wells
    ss.selected_wells = selected_wells
    

# Main working functions for each tab
def tab1_func():
     
    # Step1: Create a Basemap (OpenStreetMap and All vnBlocks) - Using JSON method
    m = folium.Map(location=[10.278, 108.197], ZOOM_START=3)
    folium.GeoJson(ss.vnBlocks_gdf, style_function=basemap_style).add_to(m)   # Show all blocks

    # Step2: Create a feature group to add to the Basemap
    feature_group = folium.FeatureGroup(name="Blocks_wells")
    
    # Step3a: Create features for bloks (GeoJson objects)
    for _, row in ss.vnBlocks_gdf.iterrows():
        if row["BLOCK_NAME"] == ss.selected_block:  
            selected_block_geojson  = folium.GeoJson(row['geometry'], style_function=selected_block_style)
            
            # Get center point of the block to zoom in at it's location
            center_point = row['geometry'].centroid
            center = [center_point.y, center_point.x]
            selected_block_label = folium.Marker(location=[center_point.y, center_point.x], icon=well_label_style(row["BLOCK_NAME"]))
            
            # Step4: Use add_child() method to add features(selected block and it's label) to the feature_group
            feature_group.add_child(selected_block_geojson)
            feature_group.add_child(selected_block_label)
            break
        
    # Step3b: Create features for wells: the symbol(folium name is marker), label(well nanme) and the popup information
    # Note that the standard styles just work well with the add_to(m) method rather than with the st_folium()
    for _, row in ss.vnWells_gdf.iterrows():
        well_count = 0
        if row["WELL_NAME"] in ss.selected_wells:          
            # Create circle symbol for well
            selected_well_geojson = folium.CircleMarker(location=[row.geometry.y, row.geometry.x], 
                                                          color="yellow", fill=True, fill_opacity=1, radius=3, popup=None)
            feature_group.add_child(selected_well_geojson)
            
            # Create well name feature
            selected_well_labels = folium.Marker(location=[row.geometry.y, row.geometry.x], icon=well_label_style(row["WELL_NAME"]))
            feature_group.add_child(selected_well_labels)
            
            # Create the popup feature - this also show up the default folium marker (How to turn markers off???)          
            popup_df_temp = ss.vnWells_df[ss.vnWells_df["WELL_NAME"] == row["WELL_NAME"]]
            popup_df = popup_df_temp[popup_fields]
            html = popup_df.to_html(classes="table table-striped table-hover table-condensed table-responsive")
            popup = folium.Popup(html)
            popup_feature = folium.Marker(location=[row.geometry.y, row.geometry.x], icon_size=(5, 5), popup=popup)
            feature_group.add_child(popup_feature)
            
            # Check if all matched wells added then break the loop
            well_count = well_count + 1
            if well_count == len(ss.selected_wells):              
                break
            
    # Finally, call st_folium() to show the Map. This method will not rerendering whole map. Just add more features
    st_folium(
        m,
        center=center,
        zoom=10,
        key="new",
        feature_group_to_add=feature_group,   # Update the map
        height=720,
        width=1500)
        
# This function shows full well information as a table (dataframe)
def tab2_func():
        
        # Check if data loaded
        if "vnBlocks_loaded" in ss and "vnWells_loaded" in ss:
        
            # Filter out the whole df for just selected wells only
            selected_well_df = ss.vnWells_df[ss.vnWells_df["WELL_NAME"].isin(ss.selected_wells)]
            
            # Show the well information
            st.dataframe(selected_well_df, hide_index= True, use_container_width=True)

def tab3_func():
    pass
       
def main_entry(): 
    
    text_message = '''📣 :rainbow[Please select and load Block and Well shapefiles to begin]:hibiscus:'''
       
    # Load the data files at the first time running ONLY
    try:
        # Check if block shapefiles is already loaded
        if "vnBlocks_loaded" not in ss:
            # Create a multiple file uploader widget
            uploaded_block_files = files_uploader_holder.file_uploader("👉 Press Ctrl to select all Block shapefiles", 
                                                                type=["shp", "dbf", "prj", "shx"], accept_multiple_files=True)        
            # Load data files
            vnBlocks_gdf, file_name1, vnBlocks_loaded = load_block_data(uploaded_block_files)
            
            # Convert geoPandasDataFrame to Pandas DataFrame and create some data
            vnBlocks_df = pd.DataFrame(vnBlocks_gdf.drop(columns="geometry"), copy=True)
            list_of_blocks = vnBlocks_df["BLOCK_NAME"].unique().tolist()
            number_of_blocks = len(list_of_blocks)
            
            # Store data into SS
            ss.vnBlocks_loaded = vnBlocks_loaded
            ss.file_name1 = file_name1
            ss.vnBlocks_gdf = vnBlocks_gdf
            ss.vnBlocks_df = vnBlocks_df
            ss.list_of_blocks = list_of_blocks
            ss.number_of_blocks = number_of_blocks
        
            # Check if well shapefiles is already loaded
        if "vnBlocks_loaded" in ss and "vnWells_loaded" not in ss:
            # Create a multiple file uploader widget
            uploaded_well_files = files_uploader_holder.file_uploader("👉 Press Ctrl to select all Well shapefiles", 
                                                                type=["shp", "dbf", "prj", "shx"], accept_multiple_files=True)                  
            # Load data files
            vnWells_gdf, file_name2, vnWells_loaded = load_well_data(uploaded_well_files)
            vnwells_df = pd.DataFrame(vnWells_gdf.drop(columns="geometry"), copy=True)
            
            # Store data into SS
            ss.vnWells_loaded = vnWells_loaded
            ss.file_name2 = file_name2
            ss.vnWells_gdf = vnWells_gdf 
            ss.vnWells_df = vnwells_df
            
        # Display working data files
        st.write(f"📣 :rainbow[The working files: {ss.file_name1} and  {ss.file_name2}]") 
                      
    except Exception as e:
        # Ignore the error of the first run, when user has not select the files to upload
        st.markdown(text_message)
        pass
        # Populate a message of loading data problem
        # st.write(e)
    
    # User input from the sidebar
    try:
        get_user_input()
    except Exception as e:
        # Ignore the error of the first run, when the data was not loaded
        pass
    
    with tab1:       
        # Check if data loaded and stored in the session state(SS) then execute the function
        if "vnBlocks_loaded" in ss and "vnWells_loaded" in ss:
            try:
                tab1_func()
            except Exception as e:
                # Show the error in tab1 if any
                st.write(e)            
    with tab2:
        try:
            tab2_func()
        except Exception as e:
            st.write(e) 

    with tab3:
        st.write("Welcome to the TAB - Under construction")

    with tab4:
        st.write("Welcome to the TAB - Under construction")
                
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''')

    
if __name__ == "__main__":
    main_entry()
      