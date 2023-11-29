import streamlit as st
import plotly.express as px
import lasio
from io import StringIO
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport

# Magic statement to preserve absolutely all widget input values across pages
# but it does not work with st.form. If disable this statement, only slider values are not preserved.
# so consider to on/off this statement
st.session_state.update(st.session_state)

# Alias the Session State
ss = st.session_state

# Page configuration
st.set_page_config(page_title="Well Logs", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

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
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> Well Logs </span>", unsafe_allow_html=True)

# Create some tabs
tab1, tab2, tab3, tab4 = st.tabs(["✍️ Exploration Data Analysis", "✍️ Well Information", "✍️ Curve Cross Plot", "✍️ About"])
    
@st.cache_data # Load data
def load_data(uploaded_file):

    # Check if files are uploaded
    if uploaded_file:
        # Read the uploaded file as a string
        las_str = uploaded_file.getvalue().decode(('Windows-1252'))
        # Create a StringIO object from the string
        las_file = StringIO(las_str)
        las = lasio.read(las_file, engine='normal')
        # Convert las to df
        well_data_df = las.df()                 
        
        # Have to use try-exception for each header section due to header of las file is very offen get error during parsing      
        try:       
            # Then we need convert index to column data
            well_data_df.reset_index(inplace=True)     # -> This is a dataframe of all well log data values     
        except:
            pass    
        try:        
            # Convert each header section to a dataframe
            well_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                      for item in las.well]
            well_header_df = pd.DataFrame(well_header).astype(str)   # -> This is a dataframe of all well information
            # Dig out well name 
            well_name = well_header_df.loc[well_header_df["Name"]=="WELL", "Value"].values[0]
            # If there is no well name in the header, let it to be the working file name
            if not well_name:
                well_name = uploaded_file.name
        except:
            pass
        
        try:
            #Convert well curve section to a dataframe
            curves_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Description': item.descr, 
                              'Original name': item.original_mnemonic, 'Number of points': item.data.shape[0]}
                      for item in las.curves]
            curves_header_df = pd.DataFrame(curves_header).astype(str)   # -> This is a dataframe of all curve information
        except:
            pass
        
        try:
            # Convert well params section to a dataframe
            parameter_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                      for item in las.params]
            parameter_header_df = pd.DataFrame(parameter_header).astype(str)   # -> This is a dataframe of all parameter information
        except:
            parameter_header_df = []
            pass
        
        try:
            # Convert well other section to a dataframe
            other_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                      for item in las.other]
            other_header_df = pd.DataFrame(other_header).astype(str)   # -> This is a dataframe of all other information
        except:
            other_header_df = []
            pass
        
        return well_data_df, well_header_df, well_name, curves_header_df, parameter_header_df, other_header_df
       
# Get user input from sidebar
def get_user_input():
    
    # Call back data from SS
    in_df = ss.df_for_plot
    
    # Setup X axis
    with st.sidebar.expander(":arrow_down: Setup the X Axis"):
        x_axis_val = st.selectbox('👉 Curve', options=in_df.columns, key = "x1")   # Get column name for the X axis
        x_scale_type = st.selectbox("👉 Scale type", options=["Linear", "Logarithmic"], key = "x2")
        x_invert = st.selectbox("👉 Inverted", options=["No", "Yes"], key = "x3")
    
    # Setup Y axis
    with st.sidebar.expander(":arrow_down: Setup the Y Axis"):
        y_axis_val = st.selectbox('👉 Curve', options=in_df.columns, key = "y1")   # Get column name for the Y axis
        y_scale_type = st.selectbox("👉 Scale type", options=["Linear", "Logarithmic"], key = "y2")
        y_invert = st.selectbox("👉 Inverted", options=["No", "Yes"], key = "y3")
        
    # Setup the third axis (Color bar) 
    color_by = st.sidebar.selectbox("👉 Color the data by", options=in_df.columns, key = "z") # Returned a string
    color_curve_df = in_df[color_by]
    color_max = color_curve_df.max() # Get max value of curve for input to color slider
    color_min = color_curve_df.min() # Get min value of curve for input to color slider   
    
    # Store the user input into SS
    ss.x_axis_val = x_axis_val
    ss.x_scale_type = x_scale_type
    ss.x_invert = x_invert
    ss.y_axis_val = y_axis_val
    ss.y_scale_type = y_scale_type
    ss.y_invert = y_invert
    
    ss.color_by = color_by
    ss.color_max = color_max
    ss.color_min = color_min
    
    # Get max, min of curve values    
    x_max = in_df[ss.x_axis_val].max()
    x_min = in_df[ss.x_axis_val].min()
    y_max = in_df[ss.y_axis_val].max()
    y_min = in_df[ss.y_axis_val].min()
    
    # Input ranges by sliders for curves of X, Y and Color
    x_range = st.sidebar.slider(f"👉 {ss.x_axis_val} range", value = [x_min, x_max], key = "slider1")
    y_range = st.sidebar.slider(f"👉 {ss.y_axis_val} range", value = [y_min, y_max], key = "slider2")
    user_input_color = st.sidebar.slider(f"👉 {color_by} range", value = [color_min, color_max], key = "slider3")
       
    # Store the user input into SS
    ss.x_range = x_range
    ss.y_range = y_range
    ss.user_input_color = user_input_color
    
# Using Streamlit Pandas Profiling for EDA of the Log curves
def tab1_func():
    
    # Create a place holder for a button and a message
    temp_place_holder = st.empty()
      
    if "profile" not in ss:
        
        # Create a button to control the running flow. The report is not auto-generating         
        generate_button = temp_place_holder.button("📣 Report generating is time consuming! 👉 Click to go!")
        
        # If user click the button 
        if generate_button:   
            # temp_place_holder.write("The report is generating, Please wait!")
            profile = ProfileReport(ss.df_for_plot)
            st_profile_report(profile)
            
            # Store the report into SS
            ss.profile = profile
            temp_place_holder.empty()
            
    else:
        # Get out the report from session state
        st_profile_report(ss.profile)

# This function is simply put the header sections in to the streamlit expanders
def tab2_func():
       
    with st.expander("👉 Well information 	:arrow_down:"):
        st.dataframe(ss.well_header_df, width=960, height=350)

    with st.expander("👉 Curve information :arrow_down:"):
        st.dataframe(ss.curves_header_df, width=960, height=350)
 
    with st.expander("👉 Parameter information	:arrow_down:"):
        st.dataframe(ss.parameter_header_df, width=960, height=350)

    with st.expander("👉 Other information	:arrow_down:"):
        st.dataframe(ss.other_header_df, width=960, height=350)

def tab3_func():
    
    # Call back data from SS
    in_df = ss.df_for_plot
   
    # Define a color palette
    color_template = ["orange", "red","green", "blue", "purple"]
    
    # Check if X and Y inverted
    if ss.x_invert == "Yes":
        autorangeX ="reversed"
    else:
        autorangeX = None
    
    if ss.y_invert == "Yes":
        autorangeY ="reversed"
    else:
        autorangeY = None
        
    # Check scale types of X and Y
    if ss.x_scale_type == "Logarithmic":
        log_x = True
    else:
        log_x = False
    if ss.y_scale_type == "Logarithmic":
        log_y = True
    else:
        log_y = False    
                
    # Plot        
    plot = px.scatter(in_df, x=ss.x_axis_val, y=ss.y_axis_val, color=ss.color_by, 
                      color_continuous_scale=color_template,
                      log_x=log_x, log_y=log_y, range_color=[ss.color_min, ss.color_max])
    
    # Slyling and Updating the plots
    plot.update_xaxes(showline=True, showgrid= True, linewidth=1, linecolor='white', mirror=True)
    plot.update_yaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    plot.update_xaxes(range = ss.x_range, autorange = autorangeX)
    plot.update_yaxes(range = ss.y_range, autorange = autorangeY)
    plot.update_layout(coloraxis = dict(cmin=ss.user_input_color[0], cmax=ss.user_input_color[1]))
    plot.update_layout(height = 700)
    st.plotly_chart(plot, use_container_width=True)    
                     
def main_entry(): 
    
    text_message = ''':rainbow[👉 Please select and load a LAS data file (Version 2.0 or older) to begin]:hibiscus:'''
    
    # Load the data files at the first time running ONLY
    try:
        # Check if the data is loaded
        if "df_for_plot" not in ss:
            # Create a file uploader widget
            uploaded_file = st.sidebar.file_uploader("👉 Please select a LAS file", type=["las", "LAS"], accept_multiple_files=False)           
            # Call load_data function 
            well_data_df, well_header_df, well_name, curves_header_df, parameter_header_df, other_header_df = load_data(uploaded_file)
            # Store data into SS
            ss.df_for_plot = well_data_df
            ss.well_header_df = well_header_df
            ss.well_name = well_name
            ss.curves_header_df = curves_header_df
            ss.parameter_header_df = parameter_header_df
            ss.other_header_df = other_header_df
            
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
        # st.write(e)
        pass
    
    with tab1:
        try:   
            # Check if the data is loaded
            if "df_for_plot" in ss:
                st.write(f"📣 :rainbow[The working Well: {ss.well_name}]")
                tab1_func() 
        except Exception as e:
            pass
            # st.write(e) 
            
    with tab2:
        try:
            # Check if the data is loaded
            if "df_for_plot" in ss:
                # Display well name
                st.write(f"📣 :rainbow[The working Well: {ss.well_name}]")
                tab2_func()
        except Exception as e:
            # Populate a message of tab2 if any error
            st.write(e)

    with tab3:
        try:   
            # Check if the data is loaded
            if "df_for_plot" in ss:
                st.write(f"📣 :rainbow[The working Well: {ss.well_name}]")
                tab3_func()
        except Exception as e:
            pass
            # st.write(e) 
        
    with tab4:
        st.write("Welcome to the TAB - Under construction")
    
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''') 
    
if __name__ == "__main__":
    main_entry()

   