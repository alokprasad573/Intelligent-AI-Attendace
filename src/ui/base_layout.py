import streamlit as st



def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #5865F2 !important;
                }

                .stApp div[data-testid="stColumn"]{
                    background-color:#E0E3FF !important;
                    padding: 3.5rem !important;
                    border-radius: 5rem !important;                   
                    }
        </style>  

                """
            ,unsafe_allow_html=True)
    
def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: #E0E3FF !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)
    

    

def style_base_layout():
# asdasd
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

                
         /* Hide Top Bar of streamlit */
                
            # #MainMenu, footer, header {
            #     visibility: hidden;
            # }
                
            .block-container {
                padding-top:1.5rem !important;    
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1 !important;
                margin-bottom:0rem !important;
            }
                

            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
            }
                
            h3, h4, p {
                font-family: 'Outfit', sans-serif;    
            }
                
            
            button{
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="secondary"]{
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button:hover{
                transform :scale(1.05)}

            .profile-card {
                background: rgba(255, 255, 255, 0.6) !important;
                backdrop-filter: blur(12px) !important;
                -webkit-backdrop-filter: blur(12px) !important;
                border-radius: 25px !important;
                padding: 30px !important;
                margin: 20px 0 !important;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15) !important;
                transition: all 0.3s ease !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-around !important;
            }

           .info {
                display: flex !important;
                flex-direction: row !important;
                justify-content: space-between !important;
            }

            .profile-card:hover {
                transform: translateY(-5px) !important;
                box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25) !important;
            }


            .profile-card p {
                font-size: 1.1rem !important;
                color: #2c3e50 !important;
                margin: 8px 0 !important;
                display: flex !important;
                align-items: center !important;
                gap: 10px !important;
                
                b {
                    font-weight: 700 !important;
                }
            }
        </style>  

                """
            ,unsafe_allow_html=True)