import streamlit as st

from src.databases.db import create_subject_now

@st.dialog("Create New Subject", width="small")
def create_subjects(teacher_id):
    
    st.write("Enter the details of new subject")
    subject_code = st.text_input("Enter Subject Code", key="subject_code", placeholder="CS101")
    subject_name = st.text_input("Enter Subject Name", key="subject_name", placeholder="Introduction to AI")
    subject_section = st.text_input("Enter Subject Section", key="subject_section", placeholder="A")
    
    if st.button("Create Subject Now", key="create_subject", type="primary", icon=":material/add:", width="stretch"):
        if subject_code and subject_name and subject_section:
            try:
                success, message = create_subject_now(subject_code, subject_name, subject_section, teacher_id)
                if success:
                    st.toast(message, icon="✅")
                    st.rerun()
                else:
                    st.toast(message, icon="❌")
            except Exception as e:
                st.toast(str(e), icon="❌")
        else:
            st.warning("Please fill in all the required fields.")
                
        
        