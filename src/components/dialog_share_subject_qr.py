import streamlit as st
import segno
import io

@st.dialog("Share Class Link", width="medium")
def share_dialog_box(s_name, s_code):
    app_domain = 'smartroll-main.streamlit.app/'
    join_url = f"{app_domain}/?join-class={s_code}"
    
    st.subheader(f"Scan to join {s_name}")
    st.write(f"Subject Code: {s_code}")
    st.markdown("<br>",unsafe_allow_html=True)
    
    qr = segno.make(join_url)
    png_io = io.BytesIO()
    qr.save(png_io, scale=10, kind="png")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.info("Copy this Link to share on Whatsapp or Email")
        
    with col2:
        st.markdown("### Scan to join")
        st.image(png_io.getvalue(), width="stretch", caption=f'QR Code to join class of {s_name}')
    
