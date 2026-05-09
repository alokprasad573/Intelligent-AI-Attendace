import random

from src.database.config import supabase
from src.pipelines.face_pipeline import get_face_embeddings
from src.pipelines.voice_pipeline import get_voice_embedding


class StudentData:

    def __init__(self, supabase=supabase, student_id=None, student_name=None,
                 image_array=None, audio_array=None):
        self.supabase = supabase
        self.student_id = student_id 
        self.student_name = student_name
        face_list = get_face_embeddings(image_array)
        self.face_embeddings = face_list[0].tolist() if face_list else None
        self.voice_embeddings = get_voice_embedding(audio_array) # pass the audio array

    def print(self):
        return [self.student_id, self.student_name, self.face_embeddings, self.voice_embeddings]


    #register student
    def register(self):
        try:
            if not self.face_embeddings:
                return False, "No face detected in the image. Please try again."
            
            if not self.voice_embeddings:
                return False, "Voice processing failed. Please try again."

            # Check if student already exists
            response = (
                self.supabase
                .table("students")
                .select("student_id")
                .eq("student_id", self.student_id)
                .execute()
            )

            if response.data:
                return False, "Student ID already exists"


            # Insert data
            data = {
                "student_id": self.student_id,
                "student_name": self.student_name,
                "face_embeddings": self.face_embeddings,
                "voice_embeddings": self.voice_embeddings,
            }
            print(data)
            response = self.supabase.table("students").insert(data).execute()
            print(response)
            if response.data:
                message = f"🎊 Welcome, {self.student_name.strip()}! Your student profile has been registered successfully. You can now proceed to login."
                return True, message
 
        except Exception as e:
            return False, f"An error occurred: {str(e)}"