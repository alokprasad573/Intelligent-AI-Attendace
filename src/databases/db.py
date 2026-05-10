import dataclasses
from src.databases.config import supabase
import bcrypt

    
# check is teacher already registered
def check_teacher_exists(t_id, t_email_id, t_mobile_number):
    # check for unique id, email_id, mobile_number in the database return already exists or taken
    response = supabase.table("teachers").select("*").eq("id", t_id).execute()
    if len(response.data) > 0:
        return False, "You are already registerd."
    
    response = supabase.table("teachers").select("*").eq("email_id", t_email_id).execute()
    if len(response.data) > 0:
        return False, "This email id is already registered."
    
    response = supabase.table("teachers").select("*").eq("mobile_number", t_mobile_number).execute()
    if len(response.data) > 0:
        return False, "This mobile number is already registered."
    
    return True, "Teacher account does not exist"
    

# tecaher registeration function
def create_teacher_account(t_id, t_name, t_email, t_number, t_gender, t_password):
    try:
        data = {
            "id": t_id,
            "name": t_name.lower(),
            "email_id": t_email,
            "mobile_number": t_number,
            "gender": t_gender.lower(),
            "password": bcrypt.hashpw(t_password.encode("utf-8"), bcrypt.gensalt()).decode()  # applying hashing on password
        }
        try:
            response = supabase.table("teachers").insert(data).execute()
        except Exception as e:
            return False, str(e)
            
        return True, f"Success! Your teacher account has been created.Teacher ID is {t_id}. Please Login now. 🔐"
    except Exception as e:
        return False, str(e)
   
# teacher login function 
def teacher_login(t_id, t_password):
    try:
        response = supabase.table("teachers").select("*").eq("id", t_id).execute()
        if len(response.data) == 0:
            return False, "Teacher ID not found, Please Register First.", None
        
        # checking password
        if not bcrypt.checkpw(t_password.encode("utf-8"), response.data[0]["password"].encode("utf-8")):
            return False, "Incorrect password", None
        
        data = {
            "t_id" : response.data[0]["id"],
            "t_name" : response.data[0]["name"].title(),
            "t_email_id" : response.data[0]["email_id"],
            "t_mobile_number" : response.data[0]["mobile_number"],
            "t_gender" : response.data[0]["gender"].title()
        }
        
        return True, f"Welcome back, {data['t_name']}! Your dedication to teaching makes a world of difference.", data
    except Exception as e:
        return False, str(e), None
    
    
# fetch data of all students
def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data
    
    
    
    
    