import streamlit as st
from src.databases.config import supabase
from src.databases.db import enroll_in_subject
import time

@st.dialog("Auto Enrolling", width='small')
def auto_enroll_box(subject_code):
    student_data = st.session_state.get('student_data')
    if not student_data:
        st.error("Student data not found. Please log in again.")
        return
    student_id = student_data.get('id')
    
    response = supabase.table('subjects').select('id', 'name').eq('code', subject_code).execute()
    if not response.data:
        st.error("Subject not found")
        if st.button("Close", type="secondary"):
            st.query_params.clear()
            st.rerun()
        return
    
    subject = response.data[0]
    check = supabase.table('subject_students').select('*').eq('subject_id', subject['id']).eq('student_id', student_id).execute()
    if check.data:
        st.info("You are already enrolled in this subject.")
        if st.button('Got it', type='tertiary'):
            st.query_params.clear()
            st.rerun()
        return
    
    st.markdown(f"Would you like to enroll in **{subject['name'].title()}** ?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('No thanks'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes enroll now!', type='primary', width='stretch'):
            success, message = enroll_in_subject(student_id, subject['id'])
            if success:
                st.toast(message, icon="✅")
                st.query_params.clear()
                time.sleep(2)
                st.rerun()
            else:
                st.toast(message, icon="❌")
            
    
    