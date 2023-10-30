# import libraries
import tkinter as tk
from tkinter import filedialog

# The input arguments:
    # button_label: The label of the button
    # button_holder: Where the button will be put in? in the sidebar and/or also in a st.empty() widget
    # if the button is put in a st.empty() widget, it can be deleted whenever we call button_holder.empty()

def file_picker(button_label, button_holder, filetypes):
    # Set up tkinter
    root = tk.Tk()
    root.withdraw()    
    # Make file picker dialog appears on top of other windows
    root.wm_attributes('-topmost', 1)
    
    try:
        clicked = button_holder.button(button_label)           
        if clicked:
            # full_path_fileName = st.text_input('Selected file:', filedialog.askopenfilename(master=root))  
            full_path_fileName = filedialog.askopenfilename(master=root, filetypes=filetypes) 

    except:
        pass
    return full_path_fileName
    
def folder_picker(button_label, button_holder):
    # Set up tkinter
    root = tk.Tk()
    root.withdraw()
    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    try:
        clicked = button_holder.button(button_label)            
        if clicked:
            # folder_name = st.text_input('Selected folder:', filedialog.askdirectory(master=root))   
            folder_name = filedialog.askdirectory(master=root)
    except:
        pass
    return folder_name