import streamlit as st
import random
import time
import datetime
from src.components.header import header_dashboard, header_home
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.take_attendance import take_attendance
from src.components.manage_subjects import manage_subjects
from src.components.attendance_records import attendance_records

# pyrefly: ignore [missing-import]
from src.databases.db import create_teacher_account, check_duplicates, teacher_login

def generate_teacher_id():
    number = random.randint(1000, 9999)
    tid = "T" + str(number)
    return tid


# teacher dashboard part
def teacher_dashboard():
    teacher_data = st.session_state.get("teacher_data", None)

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Logout",
            type="secondary",
            icon=":material/logout:",
            key="Logoutbtn",
            width="stretch",
        ):
            st.session_state["is_loggedin"] = False
            st.session_state["user_type"] = None
            del st.session_state.teacher_data
            if st.session_state.get("teacher_id"):
                del st.session_state.teacher_id
            st.rerun()

    id = teacher_data.get("id", "N/A")
    email = teacher_data.get("email_id", "N/A")
    mobile = teacher_data.get("mobile_number", "N/A")

    if teacher_data.get("gender") == "male":
        name = "Mr. " + teacher_data.get("name").title()
        pronunce = "Sir"
    else:
        name = "Ms. " + teacher_data.get("name").title()
        pronunce = "Ma'am"

    hour = datetime.datetime.now().hour

    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= hour < 20:
        greeting = "Good Evening"
    else:
        greeting = "Hey there"

    st.markdown(
        f"""
        <div class="profile-card">
            <h2>{greeting}, {pronunce}! 👋</h2>
            <div class="info">
                 <div>
                    <p>Role: <b>{st.session_state['user_type'].title()}</b></p>
                    <p>Teacher ID: <b>{id}</b></p>
                    <p>Name: <b>{name}</b></p>
                 </div>
                 <div>
                    <p>Email ID: <b>{email}</b></p>
                    <p>Contact: <b>+91 {mobile}</b></p>
                 </div>
            </div>         
        </div>
    """,
        unsafe_allow_html=True,
    )
    
    st.divider()
    
    tab1, tab2, tab3 = st.columns(3)

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    with tab1:
        type1 = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "tertiary"
        )
        if st.button(
            "Take Attendance", width="stretch", icon=":material/ar_on_you:", type=type1
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "tertiary"
        )
        if st.button(
            "Manage Subjects",
            width="stretch",
            icon=":material/book_ribbon:",
            type=type2,
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = (
            "primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "tertiary"
        )
        if st.button(
            "Attendance Records", width="stretch", icon=":material/stacks:", type=type3
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    
    if st.session_state.current_teacher_tab == "take_attendance":
        take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        manage_subjects(teacher_data)

    if st.session_state.current_teacher_tab == "attendance_records":
        attendance_records()


# Teacher Register Part
def teacher_register_form():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")
    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "go back to home",
            type="secondary",
            icon=":material/arrow_back:",
            key="loginbackbtn",
            width="stretch",
        ):
            st.session_state["role"] = None
            st.rerun()

    st.header("Teacher Registration", anchor="center")
    if "generated_teacher_id" not in st.session_state:
        st.session_state["generated_teacher_id"] = generate_teacher_id()

    t_id = st.session_state["generated_teacher_id"]
    st.subheader(f"Assigned Teacher ID: {t_id}")

    with st.form("teacher_register_form", border=False):
        t_name = st.text_input("Enter your Name", key="t_name", placeholder="John Doe")
        t_email_id = st.text_input(
            "Enter your Email", key="t_email_id", placeholder="john@example.com"
        )
        t_mobile_number = st.text_input(
            "Enter your Mobile Number",
            key="t_mobile_number",
            placeholder="10-digit mobile number",
            max_chars=10,
        )
        t_gender = st.selectbox(
            "Select your Gender", ["Select", "Male", "Female", "Other"], key="t_gender"
        )
        t_password = st.text_input(
            "Enter your password",
            type="password",
            key="t_password",
            placeholder="Choose a strong password",
        )
        t_confirm_password = st.text_input(
            "Confirm your password",
            type="password",
            key="t_confirm_password",
            placeholder="Repeat your password",
        )

        st.divider()

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.form_submit_button(
                "Register Account",
                icon=":material/app_registration:",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("Please Wait..."):
                    if (
                        not all(
                            [
                                t_name,
                                t_email_id,
                                t_mobile_number,
                                t_gender,
                                t_password,
                                t_confirm_password,
                            ]
                        )
                        or t_gender == "Select"
                    ):
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

                    teacher_data = {
                        "id": t_id,
                        "name": t_name.lower(),
                        "email_id": t_email_id,
                        "mobile_number": t_mobile_number,
                        "gender": t_gender.lower(),
                        "password": t_password,
                    }

                    success, message = check_duplicates("teachers", teacher_data)
                    if success:
                        success, message = create_teacher_account(teacher_data)
                        if success:
                            st.session_state.is_registered = True
                            st.session_state.teacher_id = t_id
                            st.rerun()
                        else:
                            st.error(message)
                    else:
                        st.error(message)

        with btn2:
            if st.form_submit_button(
                "Back to Login",
                icon=":material/login:",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state.is_registered = True
                st.rerun()


# Teacher Login Part
def teacher_login_form():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "go back to home",
            type="secondary",
            icon=":material/arrow_back:",
            key="loginbackbtn",
            width="stretch",
        ):
            st.session_state["role"] = None
            st.rerun()

    st.header("Teacher Login", anchor="center")

    if st.session_state.get("teacher_id"):
        placeholder_id = st.session_state["teacher_id"]
    else:
        placeholder_id = ""

    with st.form("teacher_login_form", border=False):
        t_id = st.text_input(
            "Enter Teacher ID",
            placeholder="Ex - T4567",
            value=placeholder_id,
            disabled=bool(placeholder_id),
        )
        t_password = st.text_input(
            "Enter your password", type="password", placeholder="Enter your password"
        )

        st.divider()

        btn1, btn2 = st.columns(2, gap="large")
        with btn1:
            if st.form_submit_button(
                "Login",
                icon=":material/login:",
                type="primary",
                use_container_width=True,
            ):
                if not t_id or not t_password:
                    st.error("Please enter both Teacher ID and password")
                    return

                with st.spinner("Verifying...."):
                    success, message, teacher_data = teacher_login(t_id, t_password)
                    if success:
                        st.session_state.is_loggedin = True
                        st.session_state.user_type = "teacher"
                        st.session_state.teacher_data = teacher_data
                        st.rerun()
                    else:
                        st.error(message)

        with btn2:
            if st.form_submit_button(
                "Don't have an account? Register",
                icon=":material/app_registration:",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state.is_registered = False
                st.rerun()


def teacher_screen():
    style_base_layout()
    style_background_dashboard()

    if (
        st.session_state.get("is_loggedin", True)
        and st.session_state.get("user_type", "") == 'teacher'
        and st.session_state.get("teacher_data", None) is not None
    ):
        teacher_dashboard()
    else:
        if st.session_state.get("is_registered", True):
            teacher_login_form()
        else:
            teacher_register_form()
