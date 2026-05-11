import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    
    header_home()
    style_base_layout()
    style_background_home()
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("I'm Student")
        st.image("https://i.ibb.co/jvprC8hn/studnet.png", width=200)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', width="stretch"):
            st.session_state['role']='student'
            st.session_state['student_login_type']='login'
            st.rerun()

    with col2:
        st.header("I'm Teacher")
        st.image("https://i.ibb.co/TDjcB5Lw/teacher-co.png", width=200)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', width="stretch"):
            st.session_state['role']='teacher'
            st.session_state['teacher_login_type']='login'
            st.rerun()
