import random
import bcrypt

from src.database.config import supabase
from src.pipelines.face_pipeline import get_face_embeddings



def _generate_student_id():
    """Generate a unique student ID. Called only during registration."""
    number = random.randint(1, 9999)
    student_id = f"S{number:04d}"
    return student_id


class StudentData:

    def __init__(self, supabase=supabase, student_id=None, student_name=None,
                 image_array=None, audio_array=None):
        self.supabase = supabase
        self.student_id = student_id
        self.student_name = student_name
        self.face_embeddings = get_face_embeddings(image_array)  # pass the image array
        self.voice_embeddings = audio_array # pass the audio array

    def print(self):
        self.student_id = _generate_student_id()
        return [self.student_id, self.student_name, self.face_embeddings, self.voice_embeddings]


    #register student
    def register(self):
        try:
            self.student_id = _generate_student_id()

            response = (
                self.supabase
                .table("students")
                .select("student_id")
                .eq("student_id", self.student_id)
                .execute()
            )

            if response.data:
                return False, "Student ID already exists", None


            # Insert data
            data = {
                "student_id": self.student_id,
                "student_name": self.student_name,
                "face_embeddings": self.face_embeddings,
                "voice_embeddings": self.voice_embeddings,
            }

            response = self.supabase.table("students").insert(data).execute()
            if response.data:
                return True, "Registration Successful", response.data[0]
            else:
                return False, "Registration Failed", None
        except Exception as e:
            return False, f"An error occurred: {str(e)}", None