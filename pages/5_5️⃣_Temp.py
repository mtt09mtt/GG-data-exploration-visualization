import streamlit as st

# Config the page
st.set_page_config(page_title="General", page_icon=":camel:", layout='wide', initial_sidebar_state='expanded')

# Read CSS file to apply the style
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    

def main_entry():
    pass

    
    
if __name__ == "__main__":
    main_entry()
      
'''
1) Style the blocks. labels
2) Tooltip / Popup for well, block
3) Explore attributes of the block, well
4) Store map to SS rather than data??? why not???
5) 
6) Global range of well log values dictionary and apply to the well!
7) Invert depth; Square plot then add option on the right side
8) HTML 5 and CSS and MARKDOWN
9) Edit well shapefile... Done for some!

'''