from src.databases.config import supabase
from src.pipelines.face_recognition_pipeline import predict_attendance
import streamlit as st
from src.databases.db import get_all_subjects_by_teacher
from src.components.dialog_add_photos import add_photos
from src.components.dialog_attendance_box import attedanace_box
import numpy as np
import pandas as pd
import datetime

def take_attendance():
    teacher_id = st.session_state.get('teacher_data', {}).get('id')
    if not teacher_id:
        st.error("Please login first.")
        return
    st.header("Take Attendance")
    
    if 'attendance_images' not in st.session_state:
        st.session_state['attendance_images'] = []
        
    subjects = get_all_subjects_by_teacher(teacher_id)
    if not subjects:
        st.error("No subjects found. Please create a subject first.")
        return
    
    subject_options = {f"{subject['code']}: {subject['name']}": subject['id'] for subject in subjects}
    col1, col2 = st.columns([3, 1])
    
    with col1:
        options = ["Select Subject"]
        options.extend(list(subject_options.keys()))
        selected_subject= st.selectbox("Select Subject", options, key="select_subject")
        
    with col2:
        st.write(" ")
        if st.button("Add Photo", type="secondary", icon=':material/add_a_photo:',width="stretch"):
            add_photos()
            
    selected_subject_id = subject_options.get(selected_subject, None)
    st.divider()
    
    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2 = st.columns(2)
    
    with c1:
        if st.session_state.attendance_images:
            if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
                st.session_state.attendance_images = []
                st.rerun()
    
    with c2:
        
        if st.session_state.attendance_images:
            
            if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/familiar_face_and_zone:', disabled=not has_photos or selected_subject_id is None):
                if selected_subject_id is None:
                    st.warning("Please select a subject first.")
                else:
                    with st.spinner("Scanning Classroom photos..."):
                        all_detected_id = {}
                        
                        for idx, img in enumerate(st.session_state.attendance_images):
                            image_arr = np.array(img.convert('RGB'))
                            
                            detected, _, _ = predict_attendance(image_arr)
                            
                            if detected:
                                for s_id in detected.keys():
                                    student_id = s_id
                                    all_detected_id.setdefault(student_id, []).append(f"Photo {idx+1}")
                        
                        enrolled_res =  supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                        enrolled_students = enrolled_res.data
                        if not enrolled_students:
                            st.warning("No students are enrolled in this course.")
                            return
                        else:
                            results, attendace_log = [], [] #creating tables
                            current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            
                            for node in enrolled_students:
                                student = node['students']
                                source = all_detected_id.get(student['id'], [])
                                is_present = len(source) > 0
                                
                                results.append({
                                    "Name" : student['name'].title(),
                                    "ID" :  student['id'],
                                    "Source": ", ".join(source) if is_present else "_",
                                    "Status" : "✅ Present" if is_present else "❌ Absent"
                                })
                                
                                attendace_log.append({
                                    "student_id" : student['id'],
                                    "subject_id" : selected_subject_id,
                                    "is_present" : is_present,
                                    "timestamp" : current_timestamp
                                })
                        
                        attedanace_box(pd.DataFrame(results), attendace_log)
    
    
    
    
    
    
    
     