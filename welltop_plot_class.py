# Worked Perfect!
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class MtPlot():

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
        
        
        
        
        
        
        
        
        
        