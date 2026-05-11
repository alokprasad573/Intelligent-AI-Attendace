from email import message
import streamlit as st
import datetime
import time
from src.databases.config import supabase

from src.databases.db import enroll_in_subject, is_student_enrolled, get_subject_id

@st.dialog("Enroll in subject", width="small")
def enroll_dialog(student_id):
    
    st.write("Enter the details of new subject")
    subject_code = st.text_input("Subject Code", placeholder="Enter the Subject Code. Eg. CS101")
    
    if st.button("Enroll Now", type="primary", width="stretch", use_container_width=True):
        if subject_code:
            # check subject exist or not 
            success, subject = get_subject_id(subject_code)
            if success:
                check, message = is_student_enrolled(student_id, subject['id'])
                if check:
                    st.warning("You are already enrolled in this subject")
                else:
                    # query to enroll in subject
                    success, message = enroll_in_subject(student_id, subject['id'])
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error(subject)
        
        else:
            st.warning('Pleae enter a subject code')
    
    
    
    
                
        
