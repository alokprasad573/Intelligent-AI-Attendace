import streamlit as st

def style_background_home():
    st.markdown("""
        <style>
                .stApp {
                    background: #0F172A !important; /* Deeper Navy for Home */
                }

                .stApp div[data-testid="stColumn"]{
                    background-color: rgba(30, 41, 59, 0.7) !important; /* Glassmorphism */
                    backdrop-filter: blur(10px);
                    padding: 3.5rem !important;
                    border-radius: 5rem !important;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
        </style>  
        """, unsafe_allow_html=True)
    
def style_background_dashboard():
    st.markdown("""
        <style>
                .stApp {
                    background: #1E293B !important; /* Your requested Slate Gray */
                }
        </style>  
        """, unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
        <style>
        /* Professional Tech Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&family=Outfit:wght@100..900&display=swap');
                
            /* Hide Top Bar of streamlit */
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top:1.5rem !important;    
            }

            h1 {
                font-family: 'Space Grotesk', sans-serif !important;
                color: #F8FAFC !important;
                font-size: 3rem !important;
                line-height:1.1 !important;
                margin-bottom:0rem !important;
            }

            h2 {
                font-family: 'Space Grotesk', sans-serif !important;
                color: #38BDF8 !important; /* Electric Blue Accent */
                font-size: 3.0rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
            }
                
            h3, h4, p {
    font-family: 'Outfit', sans-serif;
    color: #000 !important; /* Pure white for maximum visibility */
    font-weight: 400 !important;
    letter-spacing: 0.5px !important; /* Improves readability on dark backgrounds */
}
                
            button {
                border-radius: 1.5rem !important;
                background-color: #38BDF8 !important; /* Sky Blue */
                color: #0F172A !important;
                padding: 10px 20px !important;
                border: none !important;
                font-weight: 700 !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="secondary"] {
                background-color: #818CF8 !important; /* Soft Indigo */
                color: #000 !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: #F8FAFC !important;
                color: #1E293B !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }

            button:hover {
                transform: scale(1.05);
            }

            .profile-card {
                background: rgba(30, 41, 59, 0.6) !important; /* Matching Slate */
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border-radius: 25px !important;
                padding: 30px !important;
                margin: 20px 0 !important;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
                transition: all 0.3s ease !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-around !important;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }

           .info {
                display: flex !important;
                flex-direction: row !important;
                justify-content: space-between !important;
            }

            .profile-card:hover {
                transform: translateY(-5px) !important;
                box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4) !important;
                border: 1px solid #38BDF8;
            }

            .profile-card p {
                font-size: 1.1rem !important;
                color: #E2E8F0 !important;
                margin: 8px 0 !important;
                display: flex !important;
                align-items: center !important;
                gap: 10px !important;
            }

            .profile-card p b {
                font-weight: 700 !important;
                color: #38BDF8 !important; /* Highlights stand out in blue */
            }
        </style>  
        """, unsafe_allow_html=True)