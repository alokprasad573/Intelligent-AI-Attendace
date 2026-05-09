import streamlit as st
import numpy as np
import random

from PIL import Image
from src.ui.style_base_layout import style_bg_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.student_db import StudentData

generated_ids = set()
        
def student_screen_dashboard():
    pass

def student_screen_login():
    header_dashboard(back=True, back_key='back_home')
    
    _, center_col, _ = st.columns([2, 2, 2])
    with center_col:
        st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center;">
                <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" width="120">
                <h2>Student Login</h2>
                <p>Login using face recognition.</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("student_login_form"):
            # student_id = st.text_input("Student ID", placeholder="S1234")
            image = st.camera_input("Position your face in the frame to verify your identity")
            
            login = st.form_submit_button("Sign In")
            if login:
                if image:
                    try:
                        img_array = np.array(Image.open(image))
                        st.success("Face verified")     
                    except Exception as e:
                        st.error(f"Failed to process image: {str(e)}")

                else:
                    st.error("Please provide face image to verify.")
        
        if st.button("Register as Student", use_container_width=True):
            st.session_state.student_login_type = 'register'
            st.rerun()

def student_screen_register():
    header_dashboard(back=True, back_key='reg_back')
    
    _, center_col, _ = st.columns([2, 2, 2])
    with center_col:
        st.markdown("""
            <div style="display:flex; flex-direction:column; align-items:center;">
                <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" width="120">
                <h2>Create Account</h2>
                <p>Register using face recognition.</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("student_register_form"):
            student_name = st.text_input("Full Name")
            image = st.camera_input("Position your face in the frame to register your identity")
            
            register = st.form_submit_button("Register Account")
            if register:
                if image and student_name:
                    try:
                        img_array = np.array(Image.open(image))
                        student = StudentData(student_name=student_name, image_array=img_array)
                        print(student.print())
                        # st.success("Registration Successful")
                    except Exception as e:
                        st.error(f"Failed to process image: {str(e)}")

                else:
                    st.error("Please provide your name and face image")
        
        if st.button("Back to Login", use_container_width=True):
            st.session_state.student_login_type = 'login'
            st.rerun()

def student_screen():
    style_bg_dashboard()
    style_base_layout()

    if 'student_login_type' not in st.session_state or st.session_state.student_login_type == "login":
        student_screen_login()
    else:
       student_screen_register()
    