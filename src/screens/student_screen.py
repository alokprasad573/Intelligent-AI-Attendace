import streamlit as st
import numpy as np
import random

from PIL import Image
from src.ui.style_base_layout import style_bg_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.database.student_db import StudentData


def generate_student_id():
    """Generate a unique student ID. Called only during registration."""
    number = random.randint(1, 9999)
    student_id = f"S{number:04d}"
    return student_id
        
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
        
        if st.session_state.get('student_reg_success'):
            st.success(st.session_state.get('student_reg_msg', ))
            if st.button("Proceed to Login", use_container_width=True):
                st.session_state.student_reg_success = False
                st.session_state.student_login_type = 'login'
                st.rerun()
        else:
            with st.form("student_register_form"):
                student_name = st.text_input("Full Name")
                image = st.camera_input("Position your face in the frame to register your identity")
                voice = st.audio_input("Speak 5 times 'I am a student' to register your voice")
                
                register = st.form_submit_button("Register Account")
                if register:
                    # Validation
                    if not student_name.strip():
                        st.warning("Please enter your full name.")
                    elif image is None:
                        st.warning("Please capture your face image.")
                    elif voice is None:
                        st.warning("Please record your voice.")
                    else:
                        try:
                            # Process image
                            img = Image.open(image)
                            img_array = np.array(img)

                            # Process audio
                            audio_bytes = voice.read()

                            # Create student object
                            student = StudentData(
                                student_id=generate_student_id(),
                                student_name=student_name.strip(),
                                image_array=img_array,
                                audio_array=audio_bytes
                            )
                            st.write(student.print())  
                            # Register student
                            with st.spinner("Processing face and voice biometrics..."):
                                success, message = student.register()
                                if success:
                                    st.session_state.student_reg_success = True
                                    st.session_state.student_reg_msg = message
                                    st.rerun()
                                else:
                                    st.error(message)
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")
            
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
    