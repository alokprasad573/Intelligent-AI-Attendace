import streamlit as st
import random
import time
from src.components.header import header_dashboard, header_home
from src.ui.base_layout import style_base_layout, style_background_dashboard
from PIL import Image
import numpy as np

from src.databases.db import get_all_students
from src.pipelines.face_recognition_pipeline import predict_attendance, get_face_embbedings
from src.pipelines.voice_recognition_pipeline import get_voice_embeddings


def generate_student_id():
    number = random.randint(1000, 9999)
    sid = "S" + str(number)
    return sid


def student_register_form():
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()
    
    st.header("New Student Enrollement", anchor="center")
    if 'generated_student_id' not in st.session_state:
        st.session_state['generated_student_id'] = generate_student_id()
    
    s_id = st.session_state['generated_student_id']
    st.subheader(f"Assigned Student ID: {s_id}")
    
    # with st.form("New Student Enrollement Form", border=False):
    
    
def student_login_form():
    c1, c2 = st.columns(2, vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn'):
            st.session_state['login_type'] = None
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
                        st.session_state.is_loggedin = True
                        st.session_state.user_type = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}! ✨")
                        time.sleep(1)
                        st.rerun()
                        
                else:
                    st.info('Face not recognized! You might be a new student!')
                    if st.button("Don't have an account? Register", icon=":material/app_registration:", type="primary", use_container_width=True, key="registerbtn"):
                        st.session_state.is_registered = False
                        st.rerun()
    
    
    
def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    if 'is_registered' not in st.session_state and st.session_state.is_registered == False:
        student_register_form()
    else:
        student_login_form()

            
            
                
            
                
                
                    
                    
                
                    