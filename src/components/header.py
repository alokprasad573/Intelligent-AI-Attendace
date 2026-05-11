import streamlit as st


def header_home():

    logo_url = "https://i.ibb.co/9P5TwcB/app-icon.png"
    
    st.markdown(f"""
        <div style="display:flex; flex-direction:row; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px">
            <img src='{logo_url}' style='height:180px;' />
            <h1 style='text-align:center; color:#E0E3FF'>SmartRoll</h1>
        </div>   
                
                """, unsafe_allow_html=True)


def header_dashboard():

    logo_url = "https://i.ibb.co/9P5TwcB/app-icon.png"
    
    st.markdown(f"""
        <div style="display:flex; flex-direction:row; align-items:center; justify-content:center; margin-bottom:30px; margin-top:30px; gap:10px">
            <img src='{logo_url}' style='height:120px;' />
            <h2 style='width:fit-content !important;text-align:center; color:#5865F2'>SmartRoll</h2>
        </div>   
                
                """, unsafe_allow_html=True)