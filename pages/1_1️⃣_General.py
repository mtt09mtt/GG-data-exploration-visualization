import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import extra_streamlit_components as stx
import st_tk_file_folder_dialog as sttk  # This library made by mtt!

# Page configuration
st.set_page_config(page_title="General", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')
st.title("General")

# Read CSS file to apply the style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
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
    
# Create some tabs by using stx
tab_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="✍️ General Basemap", description=None),
    stx.TabBarItemData(id="tab2", title="✍️ Well Information", description=None),
    stx.TabBarItemData(id="tab3", title="✍️ Others", description=None)])

# Loading, caching and storing data into SS
@st.cache_data
def load_block_data(file_in):  
        short_file_name1 = file_in.split("/")[-1]
        vnBlocks_gdf = gpd.read_file(file_in) 
        vnblocks_df = pd.DataFrame(vnBlocks_gdf.drop(columns="geometry"), copy=True)
        list_of_blocks = vnblocks_df["BLOCK_NAME"].unique().tolist()
        vnBlocks_loaded = True                   
        # Store data into SS
        st.session_state["short_file_name1"] = short_file_name1
        st.session_state["vnBlocks_gdf"] = vnBlocks_gdf
        st.session_state["vnBlocks_df"] = vnblocks_df
        st.session_state["list_of_blocks"] = list_of_blocks
        st.session_state["vnBlocks_loaded"] = vnBlocks_loaded 

@st.cache_data
def load_well_data(file_in):  
        short_file_name2 = file_in.split("/")[-1]
        vnWells_gdf = gpd.read_file(file_in)   
        vnwells_df = pd.DataFrame(vnWells_gdf.drop(columns="geometry"), copy=True)
        vnWells_loaded = True
        # Store data into SS
        st.session_state["short_file_name2"] = short_file_name2
        st.session_state["vnWells_gdf"] = vnWells_gdf 
        st.session_state["vnWells_df"] = vnwells_df 
        st.session_state["vnWells_loaded"] = vnWells_loaded 

                           
# Main working functions for each tab
def tab1_func():
    
    # Display data files
    st.write(f"📣 :rainbow[The working files: {st.session_state.short_file_name1} and  {st.session_state.short_file_name2}]") 
    
    # Create a select box widget for selecting a block
    col1, col2 = st.columns(2)
    selected_block = col1.selectbox("Select a block 🔎", st.session_state["list_of_blocks"])
    list_of_wells = st.session_state["vnWells_df"] [st.session_state["vnWells_df"] ["BLOCK_NAME"]==selected_block]
    selected_wells = col2.multiselect("Select a well 🔎", list_of_wells)
        
    # Step1: Create a Basemap (OpenStreetMap and All vnBlocks) - Using JSON method
    m = folium.Map(location=[10.278, 108.197], ZOOM_START=3)
    folium.GeoJson(st.session_state["vnBlocks_gdf"], style_function=basemap_style).add_to(m)   # Show all blocks
    # folium.GeoJson(st.session_state["wells_gpd"], style_function=None).add_to(m)  # Show all wells (Take time)

    # Step2: Create a feature group to add to the Basemap
    feature_group = folium.FeatureGroup(name="Blocks_wells")
    
    # Step3a: Create features for bloks (GeoJson objects)
    for _, row in st.session_state["vnBlocks_gdf"].iterrows():
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
    for _, row in st.session_state["vnWells_gdf"].iterrows():
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
            popup_df_temp = st.session_state["vnWells_df"][st.session_state["vnWells_df"]["WELL_NAME"] == row["WELL_NAME"]]
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
    
        
def tab2_func():
    # Display full well information
    st.write(f"📣 :rainbow[The working files: {st.session_state.short_file_name1} and  {st.session_state.short_file_name2}]") 
    col1, col2 = st.columns(2)
    number_of_blocks = len(st.session_state["list_of_blocks"])
    selected_block = col1.selectbox(f"📣 Found {number_of_blocks} blocks in total - Select a block", 
                                  st.session_state["list_of_blocks"])
    wells_in_block = st.session_state["vnWells_df"][st.session_state["vnWells_df"]["BLOCK_NAME"] == selected_block]
    number_of_wells = wells_in_block.shape[0]
    selected_well = col2.selectbox(f"📣 {number_of_wells} wells found within the block - Select a well", 
                                          wells_in_block["WELL_NAME"])
    selected_well_df = st.session_state["vnWells_df"][st.session_state["vnWells_df"]["WELL_NAME"] == selected_well]
    st.dataframe(selected_well_df, use_container_width=True)

def tab3_func():
    pass
       
def main_entry():   
    
    if tab_id == "tab1":
        text_message = ''':rainbow[Please select the block shapefile to begin] :hibiscus:'''
        # Create a button holder in order to delete the button after file loaded successfully
        button_holder = st.sidebar.empty()    
        # Create a placeholder for the widgets - it is eazy to delete by empty method
        # placeholder = st.container()
        # Define the file types to open
        filetypes = [("ESRI shapefile", "*.shp *.SHP")]  
        try:
            if "vnBlocks_loaded" not in st.session_state:
                block_full_path_fileName = sttk.file_picker(button_label="Please select a block shapefile", 
                                                            button_holder=button_holder, filetypes=filetypes)
                load_block_data(block_full_path_fileName)
                text_message = ''':rainbow[Please select the well shapefile to begin] :hibiscus:'''
                
            if "vnWells_loaded" not in st.session_state:
                well_full_path_fileName = sttk.file_picker(button_label="Please select a well shapefile", 
                                                           button_holder=button_holder, filetypes=filetypes)
                load_well_data(well_full_path_fileName)
        except:
            st.markdown(text_message)
        
        if "vnBlocks_loaded" in st.session_state and "vnWells_loaded" in st.session_state:
            try:
                tab1_func()
            except:
                st.write(f"📣 :red[Could not parse data of the block/well shapefile(s)!]")
        
    elif tab_id == "tab2":
        try:
            tab2_func()
        except:
            st.write(f"📣 :red[Could not parse data of the block/well shapefile(s)!]")

    elif tab_id == "tab3":
        st.write(f"Welcome to {tab_id}")

    else:
        pass
        #placeholder = st.empty()

    
if __name__ == "__main__":
    main_entry()
      