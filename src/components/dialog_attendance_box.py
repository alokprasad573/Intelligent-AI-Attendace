import streamlit as st
from src.databases.db import take_attendance

@st.dialog("Attendance Report", width="medium")
def attedanace_box(df, log):
   st.write("Please confirm before submitting")
   st.dataframe(df, hide_index=True, width='stretch')
   
   col1, col2 = st.columns(2)
   with col1:
      if st.button("Discard", type="primary", width="stretch"):
         st.rerun()
   with col2:
      if st.button("Confirm & Save", type="secondary", width="stretch"):
        try:
            success, message = take_attendance(log)
            if success:
                st.toast(message, icon="✅")
                st.session_state.attendance_images = []
                st.rerun()
            else:
                st.toast(message, icon="❌")
        except Exception as e:
            st.error(f'Sync Failed Try Again : {str(e)}')
         