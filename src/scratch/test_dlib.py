import dlib
import numpy as np
from PIL import Image
import face_recognition_models

def test_detection():
    try:
        detector = dlib.get_frontal_face_detector()
        print("Detector loaded successfully")
        
        # Create a dummy black image
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        faces = detector(img, 1)
        print(f"Detection on dummy image successful, found {len(faces)} faces")
        
        sp_path = face_recognition_models.pose_predictor_model_location()
        sp = dlib.shape_predictor(sp_path)
        print(f"Shape predictor loaded from {sp_path}")
        
        rec_path = face_recognition_models.face_recognition_model_location()
        face_recognizer = dlib.face_recognition_model_v1(rec_path)
        print(f"Face recognizer loaded from {rec_path}")
        
    except Exception as e:
        print(f"Error during dlib test: {e}")

if __name__ == "__main__":
    test_detection()
