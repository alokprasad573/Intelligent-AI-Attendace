import streamlit as st

from src.components.header import header_home

def home_screen():
    st.header("Home Screen")
    
    header_home()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Teacher Login")
        if st.button("Login as Teacher"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
            
    with col2:
        st.subheader("Student Login")
        if st.button("Login as Student"):
            st.session_state['login_type'] = 'student'
            st.rerun()