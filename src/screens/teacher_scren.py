import streamlit as st
import random

from src.ui.style_base_layout import style_bg_dashboard, style_base_layout
from src.components.header import header_dashboard

# Generate Teacher ID
generated_ids = set()

def generate_teacher_id():
    while True:
        number = random.randint(1, 999999)
        teacher_id = f"T{number:04d}"

        if teacher_id not in generated_ids:
            generated_ids.add(teacher_id)
            return teacher_id
        
        
# Teacher Login
def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    
    with c1:
        header_dashboard()
        
    with c2:
        if st.button("Go Back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
        
    st.header("Login using password", text_alignment="center")
    
    st.space()
    st.space()
    teacher_id = st.text_input("Enter your Id", placeholder='T0234')
    teacher_pass = st.text_input("Enter your password", type='password', placeholder='Enter your password')
    
    st.divider()
    
    btnc1, btnc2 = st.columns(2)
    
    with btnc1:
        if st.button('Login',  shortcut='control+enter', width='stretch'):
           st.session_state.teacher_login_type = 'login'
           st.rerun()
        
    with btnc2:
       if st.button('Register Instead', type='primary',  width='stretch'):
           st.session_state.teacher_login_type = 'register'
           st.rerun()


# Teacher Register
def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    
    with c1:
        header_dashboard()
        
    with c2:
        if st.button("Go Back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()
        
    st.header("Register Yourself As Teacher", text_alignment="center")
    
    st.space()
    st.space()
    
    teacher_id = generate_teacher_id()
    teacher_name = st.text_input("Enter Your Name")
    teacher_subject1 = st.text_input("Subject You Teach", placeholder='Subject 1')
    teacher_subject2 = st.text_input("Subject You Teach", placeholder='Subject 2')
    teacher_subject3 = st.text_input("Subject You Teach", placeholder='Subject 3')
    teacher_mon_no = st.text_input("Enter your mobile number", placeholder='10 digits mobile number')
    teacher_pass = st.text_input("Enter your password", type='password', placeholder='Enter your password')
    teacher_conf_pass = st.text_input("Confirm_your_password", type='password', placeholder='Enter your password')
    teacher_subject = [teacher_subject1, teacher_subject2, teacher_subject3]
    
    
    st.divider()
    
    btnc1, btnc2 = st.columns(2)
    
    with btnc1:
        if st.button('Register', type='primary',  width='stretch'):
           st.session_state.teacher_login_type = 'register'
           st.rerun()
        
    with btnc2:    
       if st.button('Login Instead',  shortcut='control+enter', width='stretch'):
           st.session_state.teacher_login_type = 'login'
           st.rerun()
        
        
        
def teacher_screen():
    style_bg_dashboard()
    style_base_layout()
    
    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login() 
    elif  st.session_state.teacher_login_type=="register":
        teacher_screen_register()
 
    
    
        
    
    