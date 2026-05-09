import streamlit as st
import random
import time
from src.ui.style_base_layout import style_bg_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.teacher_db import TeacherData

# Generate Teacher ID

def generate_teacher_id():
    while True:
        number = random.randint(1, 9999)
        teacher_id = f"T{number:04d}"
        return teacher_id

def teacher_screen_dashboard():
    _, center_col, _ = st.columns([2, 1.8, 2])
    with center_col:
        st.markdown("""
            <div style = 'display:flex; flex-direction:column;align-items:center;' >
                <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" width="120">
                <h2>👋 Welcome Back, Let's Begin Today's Session</h2>
            </div>
        """, unsafe_allow_html=True)
        if 'teacher_id' not in st.session_state:
            st.session_state['teacher_id'] = 'NA'
        if 'teacher_name' not in st.session_state:
            st.session_state['teacher_name'] = 'NA'
        if 'teacher_mob_no' not in st.session_state:
            st.session_state['teacher_mob_no'] = 'NA'

        st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(255,255,255,0.12);
                border-radius: 20px;
                padding: 1.8rem 2rem;
                backdrop-filter: blur(12px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                margin-top: 1rem;
            ">
                <div style="display:flex; align-items:center; padding: 0.65rem 0; border-bottom: 1px solid rgba(255,255,255,0.07);">
                    <span style="color:#64748B; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; width:45%;">Teacher ID</span>
                    <span style="color:#F1F5F9; font-size:0.95rem; font-weight:500;">{st.session_state.teacher_id}</span>
                </div>
                <div style="display:flex; align-items:center; padding: 0.65rem 0; border-bottom: 1px solid rgba(255,255,255,0.07);">
                    <span style="color:#64748B; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; width:45%;">Teacher Name</span>
                    <span style="color:#F1F5F9; font-size:0.95rem; font-weight:500;">{st.session_state.teacher_name}</span>
                </div>
                <div style="display:flex; align-items:center; padding: 0.65rem 0;">
                    <span style="color:#64748B; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; width:45%;">Teacher Mob. No.</span> 
                    <span style="color:#F1F5F9; font-size:0.95rem; font-weight:500;">{st.session_state.teacher_mob_no}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

def teacher_screen_login():
    header_dashboard(back=True, back_key='back_home')

    _, center_col, _ = st.columns([2, 1.8, 2])
    with center_col:
        st.markdown("""
            <div style = 'display:flex; flex-direction:column;align-items:center;' >
                <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" width="120">
                <h2>Teacher Login</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("vision_login"):
            teacher_id = st.text_input("Teacher ID", placeholder="T1234")
            teacher_pass = st.text_input("Password", type="password")
            
            login = st.form_submit_button("Sign In")
            if login:
                teacher = TeacherData()
                success, message = teacher.login(teacher_id=teacher_id, password=teacher_pass)
                if success: 
                    st.session_state.teacher_id = teacher.teacher_id
                    st.session_state.teacher_name = teacher.teacher_name
                    st.session_state.teacher_mob_no = teacher.teacher_mob_no
                    st.session_state.is_teacher_logged_in = True
                    st.rerun()
                else: 
                    st.error(message)
                
        if st.button("New Instructor? Create Account", use_container_width=True):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

def teacher_screen_register():
    header_dashboard(back=True, back_key='reg_back')

    _, center_col, _ = st.columns([2, 2, 2])
    with center_col:
        st.markdown("""
            <div style = 'display:flex; flex-direction:column;align-items:center;' >
                <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" width="120">
                <h2>Create Account</h2>
                <p>Join the faculty dashboard to streamline attendance management</p>
            </div>
        """, unsafe_allow_html=True)
        
        if 'teacher_id' not in st.session_state:
            st.session_state['teacher_id'] = generate_teacher_id()

        if st.session_state.get('teacher_reg_success'):
            st.success(st.session_state.get('teacher_reg_msg'))
            if st.button("Proceed to Login", use_container_width=True):
                st.session_state.teacher_reg_success = False
                st.session_state.teacher_login_type = 'login'
                st.rerun()
        else:
            with st.form("teacher_register_form"):
                teacher_id = st.text_input("Assigned ID", value=st.session_state['teacher_id'], disabled=True)
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
                        st.session_state.teacher_reg_success = True
                        st.session_state.teacher_reg_msg = message
                        st.rerun()
                    else: 
                        st.error(message)

            if st.button("Back to Login", type='secondary', use_container_width=True):
                st.session_state.teacher_login_type = 'login'
                st.rerun()

def teacher_screen():
    style_bg_dashboard()
    style_base_layout()
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        if st.session_state.get('is_teacher_logged_in') == True:
            teacher_screen_dashboard()
        else:
            teacher_screen_login()
    else:
        teacher_screen_register()