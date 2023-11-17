import streamlit as st
import plotly.express as px
import lasio
from io import StringIO
import pandas as pd
import extra_streamlit_components as stx

st.set_page_config(page_title="Well Logs", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

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
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> Well Logs </span>", unsafe_allow_html=True)
    
# Create some tabs by using stx
tab_id = stx.tab_bar(data=[
    stx.TabBarItemData(id="tab1", title="✍️ Curve Cross Plot", description=None),
    stx.TabBarItemData(id="tab2", title="✍️ Well Information", description=None),
    stx.TabBarItemData(id="tab3", title="✍️ Help", description=None),
    stx.TabBarItemData(id="tab4", title="✍️ About", description=None)])
    
@st.cache_data # Load data, cache and store into Session State(SS)
def load_data(uploaded_file):

    # Check if files are uploaded
    if uploaded_file:
        # Read the uploaded file as a string
        las_str = uploaded_file.getvalue().decode(('Windows-1252'))
        # Create a StringIO object from the string
        las_file = StringIO(las_str)
        las = lasio.read(las_file)
        # Convert las to df
        well_data_df = las.df()               
            
    # Have to use try-exception for each header section due to header of las file is very offen get error during parsing      
    try:       
        # Then we need convert index to column data
        well_data_df.reset_index(inplace=True)     # -> This is a dataframe of all well log data values
        # Store dataframe into SS
        st.session_state.df_for_plot = well_data_df       
    except:
        pass
    
    try:        
        # Convert each header section to a dataframe
        well_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                  for item in las.well]
        well_header_df = pd.DataFrame(well_header).astype(str)   # -> This is a dataframe of all well information
        # Store dataframe into SS
        st.session_state.well_header_df = well_header_df
        # Dig out well name from well header section
        well_name = well_header_df.loc[well_header_df["Name"]=="WELL", "Value"].values[0]
        # Store well name into SS
        st.session_state.well_name = well_name
    except:
        pass
    
    try:
        #Convert well curve section to a dataframe
        curves_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Description': item.descr, 
                          'Original name': item.original_mnemonic, 'Number of points': item.data.shape[0]}
                  for item in las.curves]
        curves_header_df = pd.DataFrame(curves_header).astype(str)   # -> This is a dataframe of all curve information
        # Store dataframe into SS
        st.session_state.curves_header_df = curves_header_df
    except:
        pass
    
    try:
        # Convert well params section to a dataframe
        parameter_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                  for item in las.params]
        parameter_header_df = pd.DataFrame(parameter_header).astype(str)   # -> This is a dataframe of all parameter information
        # Store dataframe into SS
        st.session_state.parameter_header_df = parameter_header_df
    except:
        pass
    
    try:
        # Convert well other section to a dataframe
        other_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                  for item in las.other]
        other_header_df = pd.DataFrame(other_header).astype(str)   # -> This is a dataframe of all other information
        # Store dataframe into SS
        st.session_state.other_header_df = other_header_df
    except:
        pass
    
def cross_plot(in_df, well_name):
    # Display well name
    st.write(f"📣 :rainbow[The working files: {well_name}]") 
   
    # Define a color palette
    color_template = ["orange", "red","green", "blue", "purple"]
    
    # All input widgets for the plot
    with st.sidebar.expander(":arrow_down: Setup the X Axis"):
        x_axis_val = st.selectbox('Value', options=in_df.columns, key = "x1")   # Get column name for the X axis
        x_scale_type = st.selectbox("Scale type", options=["Linear", "Logarithmic"], key = "x2")
        x_invert = st.selectbox("Inverted", options=["No", "Yes"], key = "x3")
        
    with st.sidebar.expander(":arrow_down: Setup the Y Axis"):
        y_axis_val = st.selectbox('Value', options=in_df.columns, key = "y1")   # Get column name for the X axis
        y_scale_type = st.selectbox("Scale type", options=["Linear", "Logarithmic"], key = "y2")
        y_invert = st.selectbox("Inverted", options=["No", "Yes"], key = "y3")
    
    # Check if axises inverted
    if x_invert == "Yes":
        autorangeX ="reversed"
    else:
        autorangeX = None
    
    if y_invert == "Yes":
        autorangeY ="reversed"
    else:
        autorangeY = None
        
    # Check scale types of X and Y axises
    if x_scale_type == "Logarithmic":
        log_x = True
    else:
        log_x = False
    if y_scale_type == "Logarithmic":
        log_y = True
    else:
        log_y = False    
        
    # Get max, min of curve values    
    x_max = in_df[x_axis_val].max()
    x_min = in_df[x_axis_val].min()
    y_max = in_df[y_axis_val].max()
    y_min = in_df[y_axis_val].min()
    
    # Select ranges by sliders for curve of color    
    color_by = st.sidebar.selectbox("Color the data by", options=in_df.columns, key = "color_by") # Returned a string
    color_curve_df = in_df[color_by]
    color_max = color_curve_df.max() # Get max value of curve for input to color slider
    color_min = color_curve_df.min() # Get min value of curve for input to color slider   
    
    # Select ranges by sliders for curves of X and Y
    x_range = st.sidebar.slider(f"{x_axis_val} range", value = [x_min, x_max], key = "slider2")
    y_range = st.sidebar.slider(f"{y_axis_val} range", value = [y_min, y_max], key = "slider3")
    user_input_color = st.sidebar.slider(f"{color_by} range", value = [color_min, color_max], key = "slider4")
        
    # Plot        
    plot = px.scatter(in_df, x=x_axis_val, y=y_axis_val, color=color_by, color_continuous_scale=color_template,
                      log_x=log_x, log_y=log_y, range_color=[color_min, color_max])
    
    # Slyling and Updating the plots
    plot.update_xaxes(showline=True, showgrid= True, linewidth=1, linecolor='white', mirror=True)
    plot.update_yaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    plot.update_xaxes(range = x_range, autorange = autorangeX)
    plot.update_yaxes(range = y_range, autorange = autorangeY)
    plot.update_layout(coloraxis = dict(cmin=user_input_color[0], cmax=user_input_color[1]))
    plot.update_layout(height = 700)
    st.plotly_chart(plot, use_container_width=True)    
    
# This function is simply put the header sections in to the streamlit expanders
def well_infor(well_name, well_header_df, curves_header_df, parameter_header_df, other_header_df):

    # Check if the data loaded from tab1
    if "well_name" in st.session_state:    

        st.write(f"📣 :rainbow[The working files: {well_name}]") 
    
        with st.expander("Well information 	:arrow_down:"):
            st.dataframe(well_header_df, width=960, height=350)
    
        with st.expander("Curve information :arrow_down:"):
            st.dataframe(curves_header_df, width=960, height=350)
     
        with st.expander("Parameter information	:arrow_down:"):
            st.dataframe(parameter_header_df, width=960, height=350)
    
        with st.expander("Other information	:arrow_down:"):
            st.dataframe(other_header_df, width=960, height=350)

            
def main_entry(): 
    
    text_message = ''':rainbow[Please select and load a LAS data file - Select the first task above to begin]:hibiscus:'''
    
    if tab_id == "tab1":
        # Check if the session state(SS) is not existing -> Upload the file then store it to SS
        try:
            if "df_for_plot" not in st.session_state:  
                
                # Create a file uploader widget
                uploaded_file = st.sidebar.file_uploader("Please select a LAS file", type=["las", "LAS"], accept_multiple_files=False)           
                # Call load_data  
                load_data(uploaded_file)
                
            if "df_for_plot" in st.session_state:                     
                # Call out the data from the SS
                df1 = st.session_state.df_for_plot
                well_name = st.session_state.well_name 
                cross_plot(df1, well_name) 
                text_message = ''':rainbow[Please select a desired TAB above for more information]:hibiscus:'''
        except Exception as e:
            st.write(e) 
            
    elif tab_id == "tab2":
        try:
            well_name = st.session_state.well_name
            df2 = st.session_state.well_header_df
            df3 = st.session_state.curves_header_df
            df4 = st.session_state.parameter_header_df
            df5 = st.session_state.other_header_df
            well_infor(well_name, df2, df3, df4, df5)
            text_message = ''':rainbow[Please select a desired TAB above for more information]:hibiscus:'''
        except Exception as e:
            st.write(e)

    elif tab_id == "tab3":
        st.write(f"Welcome to {tab_id}")
        
    elif tab_id == "tab4":
        st.write(f"Welcome to {tab_id}")
    
    st.markdown(text_message)
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''') 
    
if __name__ == "__main__":
    main_entry()

   