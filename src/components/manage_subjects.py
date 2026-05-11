import streamlit as st

from src.components.dialog_create_subjects import create_subjects
from src.components.subject_cards import subject_card
from src.components.dialog_share_subject_qr import share_dialog_box
from src.databases.db import get_all_subjects_by_teacher

def manage_subjects(teacher_data):
    teacher_id = teacher_data.get('id')
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Mange Subjects", anchor="center")
    with col2:
       if st.button("Create New Subject", type="secondary", icon=":material/add:", width="stretch"):
           create_subjects(teacher_data.get('id'))
    
    subjects = get_all_subjects_by_teacher(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            
            def share_btn(s_name=sub['name'], s_code=sub['code']):
                if st.button(f"Share QR Code: {s_name}", type='primary',key=f"share_{s_code}", icon=":material/share:", width="stretch"):
                    share_dialog_box(s_name, s_code)
                    
            subject_card(
                code = sub['code'],
                name = sub['name'].title(),
                section = sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")