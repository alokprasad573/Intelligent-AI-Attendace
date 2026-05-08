import streamlit as st
from src.components.header import header_home
from src.ui.style_base_layout import style_bg_home

def home_screen():
    style_bg_home()
    header_home()

    st.markdown("<p style='text-align:center; margin-bottom:40px;'>The AI-Powered Smart Attendance System</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
            <div class="portal-card">
                <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" width="120">
                <h2>Student</h2>
                <p>Access your portal to mark attendance and track progress.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button('Enter Student Portal', key='btn_student', type='primary'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with c2:
        st.markdown("""
            <div class="portal-card">
                <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" width="120">
                <h2>Instructor</h2>
                <p>Manage classes, verify attendance, and generate reports.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button('Enter Instructor Portal', key='btn_teacher', type='primary'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()