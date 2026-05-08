import streamlit as st

def style_bg_home():
    st.markdown("""
        <style>
            /* Remove header & footer */
            #MainMenu, footer, header {
                visibility: hidden;
            }
            
            /* ── Background ── */
            .stApp {
                background: radial-gradient(circle at top right, #1E293B, #0F172A) !important;
            }

            /* Main Glass Card Container */
            .portal-card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 25px;
                padding: 30px;
                text-align: center;
                transition: all 0.3s ease;
                margin-bottom: 20px;
                width: 100%;
                aspect-ratio: 1 / 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            /* Hover Effect */
            [data-testid="stColumn"]:hover .portal-card {
                background: rgba(255, 255, 255, 0.08);
                border-color: #3B82F6;
                transform: translateY(-10px);
            }

        </style>
    """, unsafe_allow_html=True)

def style_bg_dashboard():
    st.markdown("""
       <style>
            /* ── Background: matches home screen ── */
            .stApp {
                background: radial-gradient(circle at top right, #1E293B, #0F172A) !important;
            }

            /* ── Headings: white on dark ── */
            h1 { color: #F1F5F9 !important; font-size: 2rem !important; font-weight: 800 !important; letter-spacing: -1px !important; }
            h2 { color: #F1F5F9 !important; font-size: 1.35rem !important; font-weight: 700 !important; margin-top: 8px !important; }
            h3 { color: #CBD5E1 !important; font-weight: 600 !important; }
            p  { color: #94A3B8 !important; }

            /* ── Form card: glassmorphism ── */
            div[data-testid="stForm"] {
                background: rgba(255, 255, 255, 0.05) !important;
                border: 1px solid rgba(255, 255, 255, 0.12) !important;
                border-radius: 20px !important;
                padding: 2rem !important;
                backdrop-filter: blur(12px) !important;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
            }

            /* ── Input labels ── */
            label, .stTextInput label, .stSelectbox label,
            div[data-testid="stWidgetLabel"] p {
                color: #0F172A !important;
                font-weight: 600 !important;
                font-size: 0.875rem !important;
            }

            /* ── Input fields ── */
            input[type="text"], input[type="password"],
            div[data-testid="stTextInput"] input,
            div[data-baseweb="input"] input {
                background: #1E293B !important;
                color: #F1F5F9 !important;
                border: 1.5px solid #334155 !important;
                border-radius: 10px !important;
                padding: 0.55rem 0.85rem !important;
                font-size: 0.95rem !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            }

            div[data-testid="stTextInput"] input:focus,
            div[data-baseweb="input"] input:focus {
                border-color: #3B82F6 !important;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
                outline: none !important;
                background: #0F172A !important;
            }

            /* ── Placeholder text ── */
            input::placeholder { color: #475569 !important; }

            /* ── Disabled inputs (e.g. assigned ID) ── */
            input:disabled {
                background: #0F172A !important;
                color: #475569 !important;
                cursor: not-allowed !important;
            }
        </style>
    """, unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

            /* ══════════════════════════════════════
               Strip Streamlit Default Styling
            ══════════════════════════════════════ */

            /* Override Streamlit CSS variables (kills the orange/red accent) */
            :root {
                --primary-color: #3B82F6 !important;
                --background-color: transparent !important;
                --secondary-background-color: transparent !important;
                --text-color: #F1F5F9 !important;
                --font: 'Inter', sans-serif !important;
            }

            /* Hide Streamlit chrome */
            #MainMenu, footer, header { visibility: hidden !important; }

            /* Remove default block-container padding & max-width */
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 0 !important;
                max-width: 100% !important;
            }

            /* Kill default Streamlit widget border / box decoration */
            div[data-baseweb="base-input"] {
                border: none !important;
                box-shadow: none !important;
            }

            /* Remove default Streamlit orange focus ring */
            *:focus { outline: none !important; }

            /* Remove default Streamlit bottom border on inputs */
            div[data-baseweb="input"] {
                border-bottom: none !important;
            }

            /* Remove Streamlit's default stMarkdown margin */
            .stMarkdown { margin-bottom: 0 !important; }

            /* ══ Typography ══ */
            html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

            h1 {
                font-weight: 800 !important;
                color: white !important;
                font-size: 3.5rem !important;
                letter-spacing: -1.5px !important;
                margin-bottom: 0px !important;
                text-align: center;
            }
            h2 { font-weight: 600 !important; color: #F1F5F9 !important; margin-top: 10px !important; }
            p  { color: #94A3B8 !important; font-size: 1rem !important; }

            /* ══ Buttons ══ */
            div.stButton > button {
                width: 100% !important;
                border-radius: 12px !important;
                background-color: #3B82F6 !important;
                color: white !important;
                border: none !important;
                padding: 0.5rem 1rem !important;
                font-weight: 600 !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: none !important;
            }

            div.stButton > button:hover {
                background: #2563EB !important;
                transform: translateY(-4px) scale(1.02) !important;
                box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.3) !important;
            }

            div.stButton > button:active {
                transform: translateY(-1px) scale(0.98) !important;
            }
        </style>
    """, unsafe_allow_html=True)
