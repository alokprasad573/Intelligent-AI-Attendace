import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
        <div style="text-align:center; padding-top:20px;">
            <img src='{logo_url}' style='height:80px;' />
            <h1>VisionClass</h1>
        </div>   
    """, unsafe_allow_html=True)

def header_dashboard(back=False, back_key='header_back'):
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    left, right = st.columns([5, 1])
    with left:
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:15px;  margin-left:12.5%;">
                <img src='{logo_url}' style='height:50px;' />
                <h2 style='color:#F1F5F9; margin:0;'>VisionClass</h2>
            </div>   
        """, unsafe_allow_html=True)
    if back:
        with right:
            if st.button("⬅ Home", key=back_key):
                st.session_state['login_type'] = None
                st.rerun()