import streamlit as st
import random
from src.ui.style_base_layout import style_bg_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.teacher_db import TeacherData

# Generate Teacher ID
generated_ids = set()

def generate_teacher_id():
    while True:
        number = random.randint(1, 9999)
        teacher_id = f"T{number:04d}"

        if teacher_id not in generated_ids:
            generated_ids.add(teacher_id)
            return teacher_id


def teacher_screen_login():
    header_dashboard(back=True, back_key='back_home')

    _, center_col, _ = st.columns([2, 1.8, 2])
    with center_col:
        st.markdown("<h2 style='text-align:center;'>Instructor Login</h2>", unsafe_allow_html=True)
        with st.form("vision_login"):
            teacher_id = st.text_input("Teacher ID", placeholder="T1234")
            teacher_pass = st.text_input("Password", type="password")
            
            login = st.form_submit_button("Sign In")
            if login:
                teacher = TeacherData()
                success, message = teacher.login(teacher_id=teacher_id, password=teacher_pass)
                if success: 
                    st.success(message)
                    st.session_state.teacher_login_type = 'login'
                else: 
                    st.error(message)
                
        if st.button("New Instructor? Create Account", use_container_width=True):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

def teacher_screen_register():
    header_dashboard(back=True, back_key='reg_back')

    _, center_col, _ = st.columns([2, 2, 2])
    with center_col:
        st.markdown("<h2 style='color:#1E293B; text-align:center;'>Create Account</h2>", unsafe_allow_html=True)
        
        if 'teacher_id' not in st.session_state:
            st.session_state['teacher_id'] = generate_teacher_id()

        with st.form("teacher_register_form"):
            teacher_id=st.text_input("Assigned ID", value=st.session_state['teacher_id'], disabled=True)
            teacher_name = st.text_input("Full Name")
            teacher_mob_no = st.text_input("Mobile Number")
            teacher_pass = st.text_input("Password", type='password')
            teacher_conf_pass = st.text_input("Confirm", type='password')
            
            register = st.form_submit_button("Register Account")

            if register:
                teacher = TeacherData(
                    teacher_id=teacher_id,
                    teacher_name=teacher_name,
                    teacher_mob_no=teacher_mob_no,
                    teacher_pass=teacher_pass,
                    teacher_conf_pass=teacher_conf_pass
                )
                success, message = teacher.register()
                if success: 
                    st.success(message)
                else: 
                    st.error(message)

        if st.button("Back to Login", use_container_width=True):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

def teacher_screen():
    style_bg_dashboard()
    style_base_layout()
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    else:
        teacher_screen_register()