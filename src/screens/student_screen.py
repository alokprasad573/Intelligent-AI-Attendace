import streamlit as st
import random
import time
from src.components.header import header_dashboard, header_home
from src.ui.base_layout import style_base_layout, style_background_dashboard
from PIL import Image
import numpy as np

from src.databases.db import get_all_students, check_duplicates, create_student_account
from src.pipelines.face_recognition_pipeline import predict_attendance, get_face_embbedings
from src.pipelines.voice_recognition_pipeline import get_voice_embeddings


def generate_student_id():
    number = random.randint(1000, 9999)
    sid = "S" + str(number)
    return sid


def student_register_form():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()

    with c2:
        if st.button("go back to home", type="secondary", icon=":material/arrow_back:", key="loginbackbtn", width="stretch"):
            st.session_state["role"] = None
            st.rerun()
    
    st.header("New Student Enrollement", anchor="center")
    if 'generated_student_id' not in st.session_state:
        st.session_state['generated_student_id'] = generate_student_id()
    
    s_id = st.session_state['generated_student_id']
    st.subheader(f"Assigned Student ID: {s_id}")
    
    with st.form("New Student Enrollement Form", border=False):
        s_name = st.text_input("Student Full Name", key="s_name_input", placeholder="Enter your full name")
        s_email_id = st.text_input("Student Email ID", key="s_email_id_input", placeholder="Enter your email id")
        s_mobile_number = st.text_input("Student Mobile Number", key="s_mobile_number_input", placeholder="10-digit mobile number", max_chars=10)
        
        input_col1, input_col2 = st.columns(2, gap="large")
        with input_col1:
            s_age = st.number_input("Age", min_value=5, max_value=100)
    
        with input_col2:
            s_gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
            
        enable = st.checkbox("Enable camera", value=True)
        st.write("Enable camera to enroll your face.")
        picture = st.camera_input("Position your face in the center", disabled=not enable, key="s_camera_input")
        
        enable = st.checkbox("Enable microphone", value=True)
        st.write("Enable microphone to enroll your voice.")
        audio_value = st.audio_input("Speak 'I am a student' five times.", sample_rate=16000, key="s_audio_input")
        
        if st.form_submit_button("Register", icon=":material/app_registration:", type="primary", use_container_width=True, key="registerbtn"):
            if not picture:
                st.error("Please capture your face.")
                return
            if not audio_value:
                st.error("Please record your voice.")
                return
            if not s_name or not s_email_id or not s_mobile_number or not s_age or not s_gender:
                st.error("Please fill in all the required fields.")
                return
            if len(s_mobile_number) != 10:
                st.error("Mobile number must be 10 digits long.")
                return
            if s_age < 5 or s_age > 100:
                st.error("Age must be between 5 and 100.")
                return

            image = Image.open(picture)
            image_array = np.array(image)
            audio_bytes = audio_value.read()
            
            with st.spinner("Please Wait..."):
                s_face_embbedings = get_face_embbedings(image_array)
                s_voice_embbedings = get_voice_embeddings(audio_bytes)
                
                if not s_face_embbedings:
                    st.error("Could not extract face embeddings. Please try again.")
                    return
                if not s_voice_embbedings:
                    st.error("Could not extract voice embeddings. Please try again.")
                    return
                
                success, message = check_duplicates("students", s_id, s_email_id, s_mobile_number)
                if success:
                    success, message = create_student_account(s_id, s_name, s_email_id, s_mobile_number, s_age, s_gender, s_face_embbedings, s_voice_embbedings)
                    if success:
                        st.success(message)
                        st.session_state.is_registered = True
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
                        
                else:
                    st.error(message)
            
            
        
        
    
    
def student_login_form():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()

    with c2:
        if st.button("go back to home", type="secondary", icon=":material/arrow_back:", key="loginbackbtn", width="stretch"):
            st.session_state["role"] = None
            st.rerun()
    
    st.header("Student Login using FaceID", anchor="center")
    enable = st.checkbox("Enable camera", value=True)
    picture = st.camera_input("Position your face in the center", disabled=not enable)

    if picture:
        image = Image.open(picture)
        image_array = np.array(image)
            
        with st.spinner('AI is scanning...'):
            detected_student, all_students, num_faces = predict_attendance(image_array)
            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces > 1:
                st.warning('More than one face detected!')
            else:
                if detected_student:
                    student_id = list(detected_student.keys())[0]
                    all_students_data = get_all_students()
                    student = next((s for s in all_students_data if s['id']==student_id), None)
                        
                    if student:
                        st.toast(f"Welcome Back {student['name']}! ✨")
                        st.session_state.is_loggedin = True
                        st.session_state.user_type = "student"
                        st.session_state.student_data = student
                        time.sleep(2)
                        st.rerun()
                        
                else:
                    st.info('Face not recognized! You might be a new student!')
                    if st.button("Don't have an account? Register", icon=":material/app_registration:", type="primary", use_container_width=True, key="registerbtn"):
                        st.session_state.is_registered = False
                        st.rerun()
    
    
    
def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    if st.session_state.get('is_registered', False):
        student_login_form()
    else:
        student_register_form()

            
            
                
            
                
                
                    
                    
                
                    