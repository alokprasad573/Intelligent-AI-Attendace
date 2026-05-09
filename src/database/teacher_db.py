import bcrypt

from src.database.config import supabase


class TeacherData:

    def __init__(self, supabase=supabase, teacher_id=None, teacher_name=None, teacher_mob_no=None, teacher_pass=None, teacher_conf_pass=None):
        self.supabase=supabase
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        self.teacher_mob_no = teacher_mob_no
        self.teacher_pass = teacher_pass
        self.teacher_conf_pass = teacher_conf_pass
        
    def print(self):
        return [self.teacher_id, self.teacher_name, self.teacher_mob_no, self.teacher_pass, self.teacher_conf_pass]

    # ---------------- REGISTER ---------------- #

    def register(self):
        try:
            # Check if teacher already exists
            response = (
                self.supabase
                .table("teachers")
                .select("teacher_id")
                .eq("teacher_id", self.teacher_id)
                .execute()
            )

            if response.data:
                return False, "Teacher ID already exists"

            # Check password match
            if self.teacher_pass != self.teacher_conf_pass:
                return False, "Passwords do not match"

            # Hash password
            hashed_password = bcrypt.hashpw(
                self.teacher_pass.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            # Insert data
            data = {
                "teacher_id": self.teacher_id,
                "teacher_name": self.teacher_name,
                "teacher_mob_no": self.teacher_mob_no,
                "teacher_pass": hashed_password,
            }

            response = self.supabase.table("teachers").insert(data).execute()
            if response.data:
                message = f"Welcome {self.teacher_name.strip()}! Your faculty account has been created successfully. Your Teacher ID is {self.teacher_id}."
                return True, message
    
        except Exception as e:
            return False, f"Registration failed: {str(e)}"

    # ---------------- LOGIN ---------------- #

    def login(self, teacher_id, password):
        try:
            # Fetch teacher data
            response = (
                self.supabase
                .table("teachers")
                .select("*")
                .eq("teacher_id", teacher_id)
                .execute()
            )

            # Teacher not found
            if not response.data:
                return False, "Teacher ID not found"

            data = response.data[0]

            stored_password = data["teacher_pass"]

            # Verify password
            password_match = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            )

            if not password_match:
                return False, "Incorrect Password"

            # Store data in class
            self.teacher_id = data["teacher_id"]
            self.teacher_name = data["teacher_name"]
            self.teacher_mob_no = data["teacher_mob_no"]
            self.teacher_pass = stored_password

            return True, "Login Successful"
        except Exception as e:
            return False, f"Login failed: {str(e)}"