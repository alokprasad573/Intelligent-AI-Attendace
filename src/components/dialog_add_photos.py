# pyrefly: ignore [missing-import]
import streamlit as st

from PIL import Image


@st.dialog("Capture or Upload Photos", width="small")
def add_photos():
    st.subheader("Add classroom photos for attendance",help="Upload images of the classroom for attendance. The AI will detect faces and mark attendance automatically.")
    
    if 'photo_tab' not in st.session_state:
        st.session_state['photo_tab'] = "camera"
        
    t1, t2 = st.columns(2)
    
    with t1:
        type_camera = "primary" if st.session_state['photo_tab'] == "camera" else "tertiary"
        if st.button("Camera", type=type_camera, width="stretch"):
            st.session_state['photo_tab'] = "camera"

    with t2:
        type_upload = "primary" if st.session_state['photo_tab'] == "upload" else "tertiary"
        if st.button("Upload", type=type_upload, width="stretch"):
            st.session_state['photo_tab'] = "upload"

        
    if st.session_state['photo_tab'] == "upload":
        st.subheader("Upload")
        upload_file = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True, key="dialog_upload")
        
        if upload_file:
            for file in upload_file:
                st.session_state.attendance_images.append(Image.open(file))
            st.toast("Photo added successfully", icon="✅")
            st.rerun()
    else:
        st.subheader("Camera")
        cam_photo = st.camera_input("Take Snapshot", key="dialo_cam")
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo added successfully", icon="✅")
            st.rerun()
            
    if st.button("Done", type="primary", width="stretch"):
        st.rerun()
            
            
    
            
            
    