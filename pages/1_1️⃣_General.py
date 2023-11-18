import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import extra_streamlit_components as stx
import os
import tempfile

# Page configuration
st.set_page_config(page_title="General", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

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

# Page title. Dont use st.title()
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> General </span>", unsafe_allow_html=True)

# Create some tabs by using stx
tab_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="✍️ General Basemap", description=None),
    stx.TabBarItemData(id="tab2", title="✍️ Well Information", description=None),
    stx.TabBarItemData(id="tab3", title="✍️ Help", description=None),
    stx.TabBarItemData(id="tab4", title="✍️ About", description=None)])

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

# Define a configuration to format columns when use st.dataframe
column_config1 = {}
 
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
            
        # Convert geoPandasDataFrame to Pandas DataFrame and create some data
        vnBlocks_df = pd.DataFrame(vnBlocks_gdf.drop(columns="geometry"), copy=True)
        list_of_blocks = vnBlocks_df["BLOCK_NAME"].unique().tolist()
        file_name1 = uploaded_files[0].name
        vnBlocks_loaded = True                

        # Store data into SS
        st.session_state.file_name1 = file_name1
        st.session_state.vnBlocks_gdf = vnBlocks_gdf
        st.session_state.vnBlocks_df = vnBlocks_df
        st.session_state.list_of_blocks = list_of_blocks
        st.session_state.vnBlocks_loaded = vnBlocks_loaded 

        st.write("📣 :rainbow[Block shapefiles loaded, cached and stored in Session State!]")

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
            vnwells_df = pd.DataFrame(vnWells_gdf.drop(columns="geometry"), copy=True)
            file_name2 = uploaded_files[0].name
            vnWells_loaded = True
              
        # Store data into SS
        st.session_state.file_name2 = file_name2
        st.session_state.vnWells_gdf = vnWells_gdf 
        st.session_state.vnWells_df = vnwells_df 
        st.session_state.vnWells_loaded = vnWells_loaded 
        st.write("📣 :rainbow[Well shapefiles loaded, cached and stored in Session State!]")
        
# Main working functions for each tab
def tab1_func():

    # Display working data files
    st.write(f"📣 :rainbow[The working files: {st.session_state.file_name1} and  {st.session_state.file_name2}]") 
    
    # Initialize a current selected block in SS
    if "current_block_tab1" not in st.session_state:
        st.session_state.current_block_tab1 = st.session_state.list_of_blocks[0]
    
    # User input of block
    selected_block = st.sidebar.selectbox("Select a block 🔎", st.session_state.list_of_blocks, 
                                          index=st.session_state.list_of_blocks.index(st.session_state.current_block_tab1), key = "tab1_block")
    
    # Assign the selected block to the current_block and store in SS
    st.session_state.current_block_tab1 = selected_block
    
    list_of_wells = st.session_state.vnWells_df[st.session_state.vnWells_df["BLOCK_NAME"]==selected_block]   
    
    # User input of wells
    if "current_wells_tab1" not in st.session_state:
        st.session_state.current_wells_tab1 = []   # Assign a null list
        
    selected_wells = st.sidebar.multiselect("Select wells 🔎", list_of_wells, st.session_state.current_wells_tab1, key = "tab1_wells")
    st.session_state.current_wells_tab1 = selected_wells  # Update the SS
        
    # Step1: Create a Basemap (OpenStreetMap and All vnBlocks) - Using JSON method
    m = folium.Map(location=[10.278, 108.197], ZOOM_START=3)
    folium.GeoJson(st.session_state.vnBlocks_gdf, style_function=basemap_style).add_to(m)   # Show all blocks

    # Step2: Create a feature group to add to the Basemap
    feature_group = folium.FeatureGroup(name="Blocks_wells")
    
    # Step3a: Create features for bloks (GeoJson objects)
    for _, row in st.session_state.vnBlocks_gdf.iterrows():
        if row["BLOCK_NAME"] == selected_block:  
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
    for _, row in st.session_state.vnWells_gdf.iterrows():
        well_count = 0
        if row["WELL_NAME"] in selected_wells:          
            # Create circle symbol for well
            selected_well_geojson = folium.CircleMarker(location=[row.geometry.y, row.geometry.x], 
                                                          color="yellow", fill=True, fill_opacity=1, radius=3, popup=None)
            feature_group.add_child(selected_well_geojson)
            
            # Create well name feature
            selected_well_labels = folium.Marker(location=[row.geometry.y, row.geometry.x], icon=well_label_style(row["WELL_NAME"]))
            feature_group.add_child(selected_well_labels)
            
            # Create the popup feature - this also show up the default folium marker (How to turn markers off???)          
            popup_df_temp = st.session_state.vnWells_df[st.session_state.vnWells_df["WELL_NAME"] == row["WELL_NAME"]]
            popup_df = popup_df_temp[popup_fields]
            html = popup_df.to_html(classes="table table-striped table-hover table-condensed table-responsive")
            popup = folium.Popup(html)
            popup_feature = folium.Marker(location=[row.geometry.y, row.geometry.x], icon_size=(5, 5), popup=popup)
            feature_group.add_child(popup_feature)
            
            # Check if all matched wells added then break the loop
            well_count = well_count + 1
            if well_count == len(selected_wells):              
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
    
    # Check if the data loaded from tab1
    if "list_of_blocks" in st.session_state:
        number_of_blocks = len(st.session_state.list_of_blocks)
        
        # Initialize a current selected block in SS
        if "current_block_tab2" not in st.session_state:
            st.session_state.current_block_tab2 = st.session_state.list_of_blocks[0]
        
        # User input of block
        selected_block = st.sidebar.selectbox(f"📣 Found {number_of_blocks} blocks in total - Select a block 🔎", 
                                      st.session_state.list_of_blocks, 
                                      index=st.session_state.list_of_blocks.index(st.session_state.current_block_tab2),
                                      key = "tab2_block")
        
        # Assign the selected block to the current_block and store in SS
        st.session_state.current_block_tab2 = selected_block
        
        wells_in_block = st.session_state.vnWells_df[st.session_state.vnWells_df["BLOCK_NAME"] == selected_block]
        number_of_wells = wells_in_block.shape[0]
          
        # Initialize a current selected wells in SS
        if "current_wells_tab2" not in st.session_state:
            st.session_state.current_wells_tab2 = []   # Assign a null list
            
        # User input of wells
        selected_wells = st.sidebar.multiselect(f"📣 {number_of_wells} wells found within the block - Select wells 🔎", 
                                              wells_in_block["WELL_NAME"], st.session_state.current_wells_tab2, key = "tab2_wells")
        # Assign the selected block to the current_block and store in SS
        st.session_state.current_wells_tab2 = selected_wells  # Update the SS
        
        # Filter out the whole df for just selected wells only
        selected_well_df = st.session_state.vnWells_df[st.session_state.vnWells_df["WELL_NAME"].isin(selected_wells)]
        
        # Show the well information
        st.dataframe(selected_well_df, hide_index= True, use_container_width=True)

def tab3_func():
    pass
       
def main_entry(): 
    
    text_message = ''':rainbow[Please select and load block and well shapefiles - Select the first task above to begin]:hibiscus:'''
        
    # Use a match case statement to execute the tab
    if tab_id == "tab1":
        # Create a button holder in order to delete the button after file loaded successfully
        files_uploader_holder = st.sidebar.empty()    
                
        # Load the data files at the first time of app running ONLY
        try:
            if "vnBlocks_loaded" not in st.session_state:
                # Create a multiple file uploader widget
                uploaded_block_files = files_uploader_holder.file_uploader("Press Ctrl to select all block shapefiles", 
                                                                    type=["shp", "dbf", "prj", "shx"], accept_multiple_files=True)        
                load_block_data(uploaded_block_files)
                            
            if "vnBlocks_loaded" in st.session_state and "vnWells_loaded" not in st.session_state:
                # Create a multiple file uploader widget
                uploaded_well_files = files_uploader_holder.file_uploader("Press Ctrl to select all well shapefiles", 
                                                                    type=["shp", "dbf", "prj", "shx"], accept_multiple_files=True)                  
                load_well_data(uploaded_well_files)
        except Exception as e:
            # Populate a message of loading data problem
            st.write(e)
        
        # Check if data loaded and stored in the session state(SS) then execute the function
        if "vnBlocks_loaded" in st.session_state and "vnWells_loaded" in st.session_state:
            try:
                tab1_func()
                text_message = ''':rainbow[Please select a desired TAB above for more information]:hibiscus:'''
            except Exception as e:
                st.write(e)            
    elif tab_id == "tab2":
        try:
            tab2_func()
            text_message = ''':rainbow[Please select a desired TAB above for more information]:hibiscus:'''
        except Exception as e:
            st.write(f"Welcome to {tab_id}")
            st.write(e) 

    elif tab_id == "tab3":
        st.write("Welcome to the TAB - Under construction")

    elif tab_id == "tab4":
        st.write("Welcome to the TAB - Under construction")
                
    st.markdown(text_message)
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''')

    
if __name__ == "__main__":
    main_entry()
      