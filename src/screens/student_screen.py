import streamlit as st
import random
import time
import datetime
from src.components.header import header_dashboard, header_home
from src.ui.base_layout import style_base_layout, style_background_dashboard
from PIL import Image
import numpy as np

from src.databases.db import get_all_students, check_duplicates, create_student_account, get_enrolled_subjects, get_student_attendance, unenroll_student_to_subject
from src.pipelines.face_recognition_pipeline import predict_attendance, get_face_embbedings
from src.components.dialog_enroll_subject import enroll_dialog
from src.components.subject_cards import subject_card

def generate_student_id():
    number = random.randint(1000, 9999)
    sid = "S" + str(number)
    return sid

def student_dashboard():
    student_data = st.session_state.get('student_data', None)
    
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()

    with c2:
        if st.button("Logout", type='secondary', icon=':material/logout:', key='Logoutbtn', width="stretch"):
            st.session_state["is_loggedin"] = False
            st.session_state["user_type"] = None
            del st.session_state.student_data
            if st.session_state.get("student_id"):
                del st.session_state.student_id
            st.rerun()
            
    id = student_data.get('id', 'N/A')
    name = student_data.get('name', 'N/A').title()
    email = student_data.get('email_id', 'N/A')
    mobile = student_data.get('mobile_number', 'N/A')
    age = student_data.get('age', 'N/A')
    gender = student_data.get('gender', 'N/A').title()

    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good Morning, Student"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon, Student"
    elif 17 <= hour < 20:
        greeting = "Good Evening, Student"
    else:
        greeting = "Hello, Student 👋"
        
    st.markdown(f"""
        <div class="profile-card">
            <h2>{greeting}</h2>
            <div class="info">
                 <div>
                    <p>Role: <b>{st.session_state['user_type'].title()}</b></p>
                    <p>Student ID: <b>{id}</b></p>
                    <p>Name: <b>{name}</b></p>
                 </div>
                 <div>
                    <p>Email ID: <b>{email}</b></p>
                    <p>Contact: <b>+91 {mobile}</b></p>
                    <p>Gender: <b>{gender}</b> &nbsp; &nbsp; &nbsp; &nbsp; Age: <b>{age}</b></p>
                 </div>
            </div>         
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.header("Enrolled Subjects", anchor="center")
        st.markdown("<br>",unsafe_allow_html=True)
    with c2:
        if st.button('Enroll in subject.', icon=':material/add:',type='secondary', width='stretch'):
            enroll_dialog(id)
            
    with st.spinner("Loading your enrolled subjects..."):
        enrolled_subjects = get_enrolled_subjects(id)
        attendance_data = get_student_attendance(id)
    
    stats_map = {}
    
    for log in attendance_data:
        s_id = log['subject_id']
        
        if s_id not in stats_map:
            stats_map[s_id] = {
                "total": 0,
                "attended": 0
            }
        
        stats_map[s_id]['total'] += 1
        if log.get('is_present'):
            stats_map[s_id]['attended'] += 1
            
    cols = st.columns(2)
    for i, subject_node in enumerate(enrolled_subjects):
        sub = subject_node['subjects']
        sid = sub['id']
        stats = stats_map.get(sid, {"total": 0, "attended": 0})
       
        def unenroll_button(s_name=sub['name'], s_id=sub['id']):
            if st.button(f"Unenroll from {s_name}", type='tertiary', width='stretch', icon=':material/delete_forever:', key=f"unenroll_{s_id}"):
                unenroll_student_to_subject(id, s_id)
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )

# Student Registration Form
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
        
       
        
        if st.form_submit_button("Register", icon=":material/app_registration:", type="primary", width="stretch", key="registerbtn"):
            if not picture:
                st.error("Please capture your face.")
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
            
            with st.spinner("Please Wait..."):
                s_face_embbedings = get_face_embbedings(image_array)
                
                if not s_face_embbedings:
                    st.error("Could not extract face embeddings. Please try again.")
                    return
                
                student_data = {
                    "id": s_id,
                    "name": s_name.lower(),
                    "email_id": s_email_id,
                    "mobile_number": s_mobile_number,
                    "age": s_age,
                    "gender": s_gender.lower(),
                    "face_embeddings": s_face_embbedings,
                }
                
                success, message = check_duplicates("students", student_data)
                if success:
                    success, message = create_student_account(student_data)
                    if success:
                        st.success(message)
                        st.session_state.is_registered = True
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
                    student_data = next((s for s in all_students_data if s['id']==student_id), None)
                        
                    if student_data:
                        st.session_state.is_loggedin = True
                        st.session_state.user_type = "student"
                        st.session_state.student_data = student_data
                        st.rerun()
                        
                else:
                    st.info('Face not recognized! You might be a new student!')
                    if st.button("Don't have an account? Register", icon=":material/app_registration:", type="primary", width="stretch", key="registerbtn"):
                        st.session_state.is_registered = False
                        st.rerun()
    
    
def student_screen():
    style_background_dashboard()
    style_base_layout()
    
    if st.session_state.get('is_loggedin', True) and st.session_state.get('user_type', '') == 'student' and st.session_state.get('student_data', None) is not None:
        student_dashboard()
    else:
        if st.session_state.get('is_registered', True):
            student_login_form()
        else:
            student_register_form()