from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
import streamlit as st

def main():
    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon= "https://i.ibb.co/YTYGn5qV/logo.png"
    )
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    
    if st.session_state['role'] == 'teacher':
        teacher_screen()
    elif st.session_state['role'] == 'student':
        student_screen()
    else:
        home_screen()
    

if __name__ == "__main__":
    main()
    