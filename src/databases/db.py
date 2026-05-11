import dataclasses
from src.databases.config import supabase
import bcrypt
import datetime


# check is duplicates already registered
def check_duplicates(table, data_dict):
    # check for unique id, email_id, mobile_number in the database return already exists or taken
    response = supabase.table(table).select("*").eq("id", data_dict["id"]).execute()
    if len(response.data) > 0:
        return False, "You are already registerd."

    response = (
        supabase.table(table)
        .select("*")
        .eq("email_id", data_dict["email_id"])
        .execute()
    )
    if len(response.data) > 0:
        return False, "This email id is already registered."

    response = (
        supabase.table(table)
        .select("*")
        .eq("mobile_number", data_dict["mobile_number"])
        .execute()
    )
    if len(response.data) > 0:
        return False, "This mobile number is already registered."

    if table == "teachers":
        return True, "Teacher account does not exist."
    elif table == "students":
        return True, "Student account does not exist."


# tecaher registeration function
def create_teacher_account(data_dict):
    try:
        data = {
            "id": data_dict["id"],
            "name": data_dict["name"],
            "email_id": data_dict["email_id"],
            "mobile_number": data_dict["mobile_number"],
            "gender": data_dict["gender"],
            "password": bcrypt.hashpw(
                data_dict["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode(),  # applying hashing on password
        }
        try:
            response = supabase.table("teachers").insert(data).execute()
        except Exception as e:
            return False, str(e)

        return (
            True,
            f"Success! Your teacher account has been created.Teacher ID is {data_dict['id']}. Please Login now. 🔐",
        )
    except Exception as e:
        return False, str(e)


# teacher login function
def teacher_login(t_id, t_password):
    try:
        response = supabase.table("teachers").select("*").eq("id", t_id).execute()
        if len(response.data) == 0:
            return False, "Teacher ID not found, Please Register First.", None

        # checking password
        if not bcrypt.checkpw(
            t_password.encode("utf-8"), response.data[0]["password"].encode("utf-8")
        ):
            return False, "Incorrect password", None

        data = {
            "id": response.data[0]["id"],
            "name": response.data[0]["name"],
            "email_id": response.data[0]["email_id"],
            "mobile_number": response.data[0]["mobile_number"],
            "gender": response.data[0]["gender"],
        }

        return (
            True,
            f"Welcome back, {data['name']}! Your dedication to teaching makes a world of difference.",
            data,
        )
    except Exception as e:
        return False, str(e), None


# fetch data of all students
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data


# student enrollment
def create_student_account(data_dict):
    try:
        data = {
            "id": data_dict["id"],
            "name": data_dict["name"],
            "email_id": data_dict["email_id"],
            "mobile_number": data_dict["mobile_number"],
            "age": data_dict["age"],
            "gender": data_dict["gender"],
            "face_embeddings": data_dict["face_embeddings"],
            "voice_embeddings": data_dict["voice_embeddings"],
        }
        try:
            response = supabase.table("students").insert(data).execute()
        except Exception as e:
            return False, str(e)

        return (
            True,
            f"Success! Your student account has been created.Student ID is {data_dict['id']}. Please Login now. 🔐",
        )
    except Exception as e:
        return False, str(e)


# create new subject function
def create_subject_now(subject_code, subject_name, subject_section, teacher_id):
    try:
        data = {
            "code": subject_code,
            "name": subject_name.lower(),
            "section": subject_section.upper(),
            "teacher_id": teacher_id,
        }
        try:
            response = supabase.table("subjects").insert(data).execute()
        except Exception as e:
            return False, str(e)

        return True, f"Subject created successfully !"
    except Exception as e:
        return False, str(e)


# fetch data of all subjects
def get_all_subjects_by_teacher(teacher_id):
    response = (
        supabase.table("subjects")
        .select("*, subject_students(count), attendance_logs(timestamp)")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = response.data

    for sub in subjects:
        sub["total_students"] = (
            sub.get("subject_students", [{}])[0].get("count", 0)
            if sub.get("subject_students")
            else 0
        )
        attendance = sub.get("attendance_logs", [])
        unique_sessions = len(set(log["timestamp"] for log in attendance))
        sub["total_sessions"] = unique_sessions
        sub["total_classes"] = unique_sessions

        sub.pop("subject_students", None)
        sub.pop("attendance_logs", None)

        sub["name"] = sub["name"].title()
    return subjects


# get subject by id
def get_subject_id(subject_code):
    try:
        response = (
            supabase.table("subjects").select("*").eq("code", subject_code).execute()
        )
        if response.data:
            return True, response.data[0]
        else:
            return False, "Subject not found"
    except Exception as e:
        return False, str(e)


# check if student is enrolled in subject
def is_student_enrolled(student_id, subject_id):
    try:
        response = (
            supabase.table("subject_students")
            .select("*")
            .eq("student_id", student_id)
            .eq("subject_id", subject_id)
            .execute()
        )
        if response.data:
            return True, response.data[0]
        else:
            return False, "Not enrolled"
    except Exception as e:
        return False, str(e)


# enroll in a subject
def enroll_in_subject(student_id, subject_id):
    try:
        response = (
            supabase.table("subject_students")
            .select("*")
            .eq("subject_id", subject_id)
            .eq("student_id", student_id)
            .execute()
        )
        if len(response.data) > 0:
            return True, "You are already enrolled in this subject."
        else:
            response = (
                supabase.table("subject_students")
                .insert(
                    {
                        "student_id": student_id,
                        "subject_id": subject_id,
                        "created_at": datetime.datetime.now().isoformat(),
                    }
                )
                .execute()
            )
            return True, "You are successfully enrolled in this subject."
    except Exception as e:
        return False, str(e)


def unenroll_student_to_subject(student_id, subject_id):
    response = (
        supabase.table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )
    return response.data


def get_enrolled_subjects(student_id):
    response = (
        supabase.table("subject_students")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data


def get_student_attendance(student_id):
    response = (
        supabase.table("attendance_logs")
        .select("*, subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data
