import dlib 
import numpy as ns 
import face_recognition_models
import streamlit as st
import numpy as np
from sklearn.svm import SVC 
from src.databases.db import get_all_students




# Loading dlib models
@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    face_recognizer = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return detector, sp, face_recognizer

# getting face embeddings
def get_face_embbedings(image_array):
    detector, sp, face_recognizer = load_dlib_models()
    faces = detector(image_array, 1)
    
    embeddings = []
    for face in faces:
        landmarks = sp(image_array, face)
        embedding = face_recognizer.compute_face_descriptor(image_array, landmarks, 1) # 128 embbedings
        embeddings.append(np.array(embedding))
    
    return embeddings

# training the classifier with stored data from database
@st.cache_resource
def get_trained_model():
    X = []
    y = []
    
    student_db = get_all_students()
    
    if student_db is None:
        return None
    
    for student in student_db:
        embedding = student['face_embeddings']
        if embedding:
            X.append(np.array(embedding))
            y.append(student['id'])
    
    if len(X) == 0:
        return None
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    try:
        clf.fit(X,y)
    except ValueError:
        pass
    
    return {'clf': clf, 'X': X, 'y': y}
    
def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_array):
    embeddings = get_face_embbedings(class_image_array)
    
    detected_student = {}
    
    model_data = get_trained_model()
    
    if not model_data:
        return detected_student, [], len(embeddings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']
    
    all_students = sorted(list(set(y_train)))
    
    for embedding in embeddings:
        if len(all_students) >= 2:
            print(clf.predict([embedding])[0])
            predicted_id = clf.predict([embedding])[0]
        else:
            predicted_id = all_students[0]
            
        student_embedding = X_train[y_train.index(predicted_id)]
        
        best_match_score = np.linalg.norm(student_embedding - embedding)
        
        resemblance_threshold = 0.6
        
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
            
    return detected_student, all_students, len(embeddings)
            
    
    
        
        
