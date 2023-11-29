import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Magic statement to preserve widget input values across pages
st.session_state.update(st.session_state)

# Alias the Session State
ss = st.session_state

# Page configuration
st.set_page_config(page_title="DSTs and TOPs", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

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
st.markdown("<span style='color: yellow; font-size:45px; font-weight: bold;'> Well DSTs and Tops </span>", unsafe_allow_html=True)

# Create some tabs
tab1, tab2, tab3, tab4 = st.tabs(["✍️ Plot Well Tops and DSTs", "✍️ Data file example", "✍️ Help", "✍️ About"])

def well_top(df, start_depth, stop_depth, name_col, depth_col):
    # df                : The input pandas dataframe
    # top_depth_col     : Column of the top depth of DST in measure depth(md)
    # base_depth_col    : Column of the base depth of DST 
    # name_col          : Column of the DST number
    # start_depth       : Start depth(md) of borehole to plot
    # stop_depth        : Stop depth of borehole to plot        
    
    # fig, ax = plt.subplots(figsize=(3, 5)) # The default: W=6.4in=640px; H=4.8in=480px
    # Create a figure and a axis.        
    fig, ax = plt.subplots()
    
    # Plot a wellbore with depth from start_depth to TD
    ax.axhspan(start_depth, stop_depth, 0.2, 0.4, color="brown", alpha=1, label= "Wellbore")
    # Set y-axis limit
    plt.ylim(start_depth, stop_depth)    
    # Plot Tops
    for i in range(len(df)):
        # Get value at row i, depth_col for depths (md)
        ax.axhline(y=df.iloc[i,depth_col], xmin=0.2, xmax=0.4, color="yellow")
        # Get value at row i, name_col for top names
        # ax.text(0.5, df.iloc[i,depth_col], (df.iloc[i, name_col] + " @ "+ str(df.iloc[i,depth_col])), ha='left', va='center')
        ax.text(0.5, df.iloc[i,depth_col], (df.iloc[i, name_col]), ha='left', va='center')
    # Invert y axis
    ax.invert_yaxis()
    
    # Set background color
    ax.set_facecolor("pink")
    
    # Turn off x ticks and it's labels
    ax.xaxis.set_major_locator(ticker.NullLocator())
    
    # Add legend
    ax.legend(loc="upper right")
    
    # Set y-axis label position to the right
    ax.yaxis.set_label_position("right")
    
    # Set y-axis label
    ax.set_ylabel("Depth (MDm)")
    
    # Set x-axis label
    ax.set_xlabel("Plot depth from " + str(start_depth) + " to " + str(stop_depth) + "m")   
           
    return fig

def well_dst(df, start_depth, stop_depth, top_depth_col, base_depth_col, name_col):
    # df                : The input pandas dataframe
    # top_depth_col     : Column of the top depth of DST in measure depth(md)
    # base_depth_col    : Column of the base depth of DST 
    # name_col          : Column of the DST number
    # start_depth       : Start depth(md) of borehole to plot
    # stop_depth        : Stop depth of borehole to plot  
    
    # Create default figure and ax (Figure size will be: W=6.4in=640px; H=4.8in=480px)
    fig, ax = plt.subplots()
    
    # Plot a wellbore with depth from start_depth to TD
    ax.axhspan(start_depth, stop_depth, 0.2, 0.4, color="brown", alpha=1, label= "Wellbore")        
    # Set y-axis limit
    plt.ylim(start_depth, stop_depth)
    # Plot DSTs
    for i in range(len(df)):
        ax.axhspan(ymin=df.iloc[i,top_depth_col], ymax=df.iloc[i, base_depth_col], xmin=0.2, xmax=0.4, color="yellow",
                   alpha=1, label = "Dst" + str(df.iloc[i, name_col]))               
    # Invert y axis
    ax.invert_yaxis()
    
    # Set background color
    ax.set_facecolor("pink")
    
    # Turn off x ticks and it's labels
    ax.xaxis.set_major_locator(ticker.NullLocator())
    
    # Add legend
    ax.legend(loc="upper right")
    
    # Set y-axis label position to the right
    ax.yaxis.set_label_position("right")
    
    # Set y-axis label
    ax.set_ylabel("Depth (MDm)")
    
    # Set x-axis label
    ax.set_xlabel("Plot depth from " + str(start_depth) + " to " + str(stop_depth) + "m")     
          
    return fig
    
@st.cache_data # Load data, cache and store into Session State(SS)
def load_data(uploaded_file):
    if uploaded_file:
        
        # Read only sheets named "well_top" and "well_dst"
        df_well_top = pd.read_excel(uploaded_file, sheet_name="well_top")
        df_well_dst = pd.read_excel(uploaded_file, sheet_name="well_dst")
        
        # Sort the dataframes
        df_well_top = df_well_top.sort_values(["well_name", "surface_md_m"], ascending = [True, True])
        df_well_dst = df_well_dst.sort_values(["well_name", "dst_number"], ascending = [True, True])
        
        file_loaded = True
        return df_well_top, df_well_dst, file_loaded

        
# Get user input from sidebar
def get_user_input():
      
    # Input from user or get the items from SS
    number_of_wells_has_top = len(ss.unique_well_top)
    selected_well_has_top = st.sidebar.selectbox(f"📣 Found {number_of_wells_has_top} Well with Tops - Select one", 
                                                 ss.unique_well_top, key = "tab1_select_1")
       
    number_of_wells_has_dst = len(ss.unique_well_dst)
    selected_well_has_dst = st.sidebar.selectbox(f"📣 Found {number_of_wells_has_dst} Well with DSTs - Select one", 
                                                 ss.unique_well_dst, key = "tab1_select2")
    # Store the input into SS
    ss.selected_well_has_top = selected_well_has_top
    ss.selected_well_has_dst = selected_well_has_dst
   
# Main body
def tab1_func():     
       
    # Create 2 columns below above row in the Main page
    col1, col2 = st.columns(2)
    
    # Place widgets in col1
    with col1:
        
        # Setup range of the depth
        depth_range1 = st.slider("👉 Select depth range for Tops", value = [500.0, 5500.0])
        
        # Create a dataframe for plotting tops
        show_df1 = ss.df_well_top[ss.df_well_top["well_name"] == ss.selected_well_has_top]
        show_df1 = show_df1.sort_values(by="surface_md_m", ascending=True)
                
        # Call well_top function
        my_fig = well_top(show_df1, depth_range1[0], depth_range1[1], 1, 3)
                        
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
        show_df2 = ss.df_well_dst[ss.df_well_dst["well_name"] == ss.selected_well_has_dst]
                
        # Call well_dst
        my_fig = well_dst(show_df2, depth_range2[0], depth_range2[1], 3, 4, 2)
               
        # Show the matplotlib plot on col2
        st.pyplot(my_fig)
        
        # Show the data as a table
        df2a = show_df2.iloc[:, 2:]
        #st.write(df2a)
        st.dataframe(df2a, width=640, height=350)
        
def main_entry():
    text_message = ''':rainbow[👉 Please select and load an Excel data file - 
    The file must has two sheets named "well_top" and "well_dst"]:hibiscus:'''
    
    try:
        if "file_loaded" not in ss:
            # Create a file uploader widget
            uploaded_file = st.sidebar.file_uploader("👉 Please select a Exel data file", type=["xls", "xlsx"], accept_multiple_files=False)  
            # load_excel data file
            df_well_top, df_well_dst, file_loaded = load_data(uploaded_file)
            
            # Get unique blocks and wells
            unique_well_top = df_well_top["well_name"].unique().tolist()
            unique_well_dst = df_well_dst["well_name"].unique().tolist()
                  
            # Store data into SS
            ss.df_well_top = df_well_top
            ss.df_well_dst = df_well_dst
            ss.unique_well_top = unique_well_top
            ss.unique_well_dst = unique_well_dst
            ss.file_loaded = file_loaded
            
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
        try:         
                
            if "file_loaded" in ss:
                tab1_func()
        except Exception as e:
            st.write(e)

    with tab2:
        st.write("📣 :rainbow[This is an example Excel sheet of the input well top data]")
        st.image(r"./images/well_top_example.PNG")
        st.write("📣 :rainbow[This is an example Excel sheet of the input well DST data]")
        st.image(r"./images/well_dst_example.PNG")
        text_message = ''':rainbow[👉 Please select a desired TAB above for more information]:hibiscus:'''
        
    with tab3:
        st.write("Welcome to the Help TAB - Under construction")
        text_message = ''':rainbow[👉 Please select a desired TAB above for more information]:hibiscus:'''
        
    with tab4:
        st.write("Welcome to the About TAB - Under construction")
        text_message = ''':rainbow[👉 Please select a desired TAB above for more information]:hibiscus:'''
        
    st.sidebar.markdown(''' Created with ❤️ by My Thang ''')
        
    
if __name__ == "__main__":
    main_entry()