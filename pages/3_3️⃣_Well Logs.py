import streamlit as st
import plotly.express as px
import lasio
# from io import StringIO
import pandas as pd
import st_tk_file_folder_dialog as sttk  # This library made by mtt!

st.set_page_config(page_title="Well Logs", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')
st.title("Well Logs")

# Read CSS file to apply the style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
@st.cache_data # Will use the session state
def load_data(full_file_name):
    # This function takes input as the full file name(system path + filename + extension) a las file 
    # of version 2 or older. It returns 5 data frames of all data from the input
    
    # Have to use try-exception for each header section due to header of las file is very offen get error during parsing
    if full_file_name:       
        try:
            myInputLas = lasio.read(full_file_name, engine="normal")
            # Convert input las data to pandas dataframe. This method use depth as index
            well_data_df = myInputLas.df()           
            # Then we need convert index to column data
            well_data_df.reset_index(inplace=True)     # -> This is a dataframe of all well log data values
        except:
            pass
        
        try:        
            # Convert each header section to a dataframe
            well_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                      for item in myInputLas.well]
            well_header_df = pd.DataFrame(well_header).astype(str)   # -> This is a dataframe of all well information
        except:
            pass
        
        try:
            #Convert well curve section to a dataframe
            curves_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Description': item.descr, 
                              'Original name': item.original_mnemonic, 'Number of points': item.data.shape[0]}
                      for item in myInputLas.curves]
            curves_header_df = pd.DataFrame(curves_header).astype(str)   # -> This is a dataframe of all curve information
        except:
            pass
        
        try:
            # Convert well params section to a dataframe
            parameter_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                      for item in myInputLas.params]
            parameter_header_df = pd.DataFrame(parameter_header).astype(str)   # -> This is a dataframe of all parameter information
        except:
            pass
        
        try:
            # Convert well other section to a dataframe
            other_header = [{'Name': item.mnemonic, 'Unit': item.unit, 'Value': item.value, 'Description': item.descr}
                      for item in myInputLas.other]
            other_header_df = pd.DataFrame(other_header).astype(str)   # -> This is a dataframe of all other information
        except:
            pass
        
    # Finally, return 5 dataframes    
    return well_data_df, well_header_df, curves_header_df, parameter_header_df, other_header_df
    
def cross_plot(in_df, well_name):
    # Display well name
    st.subheader(well_name) 
    
    # Define a color palette
    color_template = ["orange", "red","green", "blue", "purple"]
    
    # Setup 4 columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Get user input for plot
    x_axis_val = col1.selectbox('Select the X-axis', options=in_df.columns)
    x_scale_type = col2.selectbox("Select the X-axis scale type", options=["Linear", "Logarithmic"])
    y_axis_val = col3.selectbox('Select the Y-axis', options=in_df.columns)
    y_scale_type = col4.selectbox("Select the Y-axis scale type", options=["Linear", "Logarithmic"])
    color_by = st.selectbox("Color the data by", options=in_df.columns)
    
    # Check scale types of X and Y axises
    if x_scale_type == "Logarithmic":
        log_x = True
    else:
        log_x = False
    if y_scale_type == "Logarithmic":
        log_y = True
    else:
        log_y = False    
    # Plot    
    plot = px.scatter(in_df, x=x_axis_val, y=y_axis_val, color= color_by, color_continuous_scale= color_template,
                      log_x= log_x, log_y= log_y)
    # Slyling the plots
    plot.update_xaxes(showline=True, showgrid= True, linewidth=1, linecolor='white', mirror=True)
    plot.update_yaxes(showline=True, linewidth=1, linecolor='white', mirror=True)
    st.plotly_chart(plot, use_container_width=True)    
    
def well_infor(well_header_df, curves_header_df, parameter_header_df, other_header_df):
    # This function is simply put the header sections in to the streamlit expanders

    with st.expander("Well information 	:arrow_down:"):
        st.dataframe(well_header_df, width=960, height=350)

    with st.expander("Curve information :arrow_down:"):
        st.dataframe(curves_header_df, width=960, height=350)
 
    with st.expander("Parameter information	:arrow_down:"):
        st.dataframe(parameter_header_df, width=960, height=350)

    with st.expander("Other information	:arrow_down:"):
        st.dataframe(other_header_df, width=960, height=350)

            
def main_entry():    
       
    # Check if the session state(SS) is not existing -> Upload the file then store it to SS
    try:
        if "df_for_plot" not in st.session_state:
            
            # Create a placeholder for the button in order to delete the button after file loaded successfully
            button_holder = st.sidebar.empty()
            
            # Define the file types to open
            filetypes = [("Well log LAS file", "*.las *.LAS")]
            
            # Call select the file button from tmt library to get the full file name (include path and extension)
            full_file_name = sttk.file_picker(button_label="Please select well data - a las file", 
                                              button_holder=button_holder, filetypes=filetypes)
            
            well_data_df, well_header_df, curves_header_df, parameter_header_df, other_header_df = load_data(full_file_name)
            
            # Dig out well name from well header section
            well_name = well_header_df.loc[well_header_df["Name"]=="WELL", "Value"].values[0]
            
            data_loaded = True
            
            # Store the data of the well into SS
            st.session_state["df_for_plot"] = well_data_df
            st.session_state["well_name"] = well_name
            st.session_state["well_header_df"] = well_header_df
            st.session_state["curves_header_df"] = curves_header_df
            st.session_state["parameter_header_df"] = parameter_header_df
            st.session_state["other_header_df"] = other_header_df
                        
        # Call out the data from the SS
        df1 = st.session_state["df_for_plot"]
        well_name = st.session_state["well_name"]
        df2 = st.session_state["well_header_df"]
        df3 = st.session_state["curves_header_df"]
        df4 = st.session_state["parameter_header_df"]
        df5 = st.session_state["other_header_df"]
        
        # Call the main functions - it is always called in try-except block of the main_entry function
        cross_plot(df1, well_name) 
        well_infor(df2, df3, df4, df5)
        
        # Delete the select well data button if everything looks good!
        if data_loaded:
            button_holder.empty()
            
            
    except Exception:
        st.markdown(''':rainbow[Please select the well LAS file to begin] :hibiscus:''') 
        
    
if __name__ == "__main__":
    main_entry()

   