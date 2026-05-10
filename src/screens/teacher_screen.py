import streamlit as st
import random
import time
from src.components.header import header_dashboard, header_home
from src.ui.base_layout import style_base_layout, style_background_dashboard

# pyrefly: ignore [missing-import]
from src.databases.db import create_teacher_account, check_duplicates, teacher_login

def generate_teacher_id():
    number = random.randint(1000, 9999)
    tid = "T" + str(number)
    return tid


# Teacher Register Part
def teacher_register_form():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()

    with c2:
        if st.button("go back to home", type="secondary", icon=":material/arrow_back:", key="loginbackbtn", width="stretch"):
            st.session_state["role"] = None
            st.rerun()
    
    st.header("Teacher Registration", anchor="center")
    if 'generated_teacher_id' not in st.session_state:
        st.session_state['generated_teacher_id'] = generate_teacher_id()
    
    t_id = st.session_state['generated_teacher_id']
    st.subheader(f"Assigned Teacher ID: {t_id}")
    
    with st.form("teacher_register_form", border=False):
        t_name = st.text_input("Enter your Name", key="t_name", placeholder="John Doe")
        t_email_id = st.text_input("Enter your Email", key="t_email_id", placeholder="john@example.com")
        t_mobile_number = st.text_input("Enter your Mobile Number", key="t_mobile_number", placeholder="10-digit mobile number", max_chars=10)
        t_gender = st.selectbox("Select your Gender", ['Select','Male', 'Female', 'Other'], key="t_gender")
        t_password = st.text_input("Enter your password", type="password", key="t_password", placeholder="Choose a strong password")
        t_confirm_password = st.text_input("Confirm your password", type="password", key="t_confirm_password", placeholder="Repeat your password")
        
        st.divider()
        
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.form_submit_button("Register Account", icon=":material/app_registration:", type="primary", use_container_width=True):
                with st.spinner("Please Wait..."):
                    if not all([t_name, t_email_id, t_mobile_number, t_gender, t_password, t_confirm_password]) or t_gender == 'Select':
                        st.error("Please fill in all the required fields.")
                        return

                    if len(t_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                        return

                    if t_password != t_confirm_password:
                        st.error("Passwords do not match. Please try again.")
                        return
                    
                    if len(t_mobile_number) != 10:
                        st.error("Mobile number must be 10 digits long.")
                        return
                    
                    success, message = check_duplicates("teachers", t_id, t_email_id, t_mobile_number)
                    if success:
                        success, message = create_teacher_account(t_id, t_name, t_email_id, t_mobile_number, t_gender, t_password)
                        if success:
                            st.success(message)
                            st.session_state.is_registered = True
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error(message)
                    
        with btn2:
            if st.form_submit_button("Back to Login", icon=":material/login:", type="secondary", use_container_width=True):
                st.session_state.is_registered = True
                st.rerun()


# Teacher Login Part
def teacher_login_form():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("go back to home", type="secondary", icon=":material/arrow_back:", key="loginbackbtn", width="stretch"):
            st.session_state["role"] = None
            st.rerun()

    st.header("Teacher Login", anchor="center")

    with st.form("teacher_login_form", border=False):
        t_id = st.text_input("Enter Teacher ID", placeholder="Ex - T4567")
        t_password = st.text_input("Enter your password", type="password", placeholder="Enter your password")

        st.divider()

        btn1, btn2 = st.columns(2, gap="large")
        with btn1:
            if st.form_submit_button("Login", icon=":material/login:", type="primary", use_container_width=True):
                if not t_id or not t_password:
                    st.error("Please enter both Teacher ID and password")
                    return
                
                with st.spinner("Verifying...."):
                    success, message, data = teacher_login(t_id, t_password)
                    if success:
                        st.success(message)
                        st.session_state.is_loggedin = True
                        st.session_state.user_type = "teacher"
                        st.session_state.teacher_data = data
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
        
        with btn2:
            if st.form_submit_button("Don't have an account? Register", icon=":material/app_registration:", type="secondary", use_container_width=True):
                st.session_state.is_registered = False
                st.rerun()


def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    
    if st.session_state.get('is_registered', True):
        teacher_login_form()
    else:
        teacher_register_form()
