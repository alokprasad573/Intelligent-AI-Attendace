import streamlit as st


from supabase import create_client, Client

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


def get_all_students():
    response = supabase.table('teachers').select("*").execute()
    for data in response.data:
        name = data["name"].title()
        gender = data["gender"].title()
        print(f"Name: {name}, Gender: {gender}")

get_all_students()
    