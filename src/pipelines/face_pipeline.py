import dlib 
import numpy as np 
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
import os
import json

@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    
    return detector, sp, facerec
    
def get_face_embeddings(image_array):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_array, 1)
    
    embeddings = []
    for face in faces:
        shape = sp(image_array, face) # landmarks of face
        embedding = facerec.compute_face_descriptor(image_array, shape) # 128 Embeddings of face
        embeddings.append(np.array(embedding))
        
    return embeddings
    
    
@st.cache_resource
def get_trained_model():
    X = []
    y = []
    
    student_db = get_all_students()
    
    if not student_db:
        return None
    
    for student in student_db:
        X.append(student['face_embeddings'])
        y.append(student['student_id'])
        
    if len(X) == 0:
        return 0
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    
    try:
        clf.fit(X, y)
    except ValueError as e:
        pass
    
    return {"Classifier" : clf, "X" : X, "y" : y}



def train_classifier():
    st.cache_resource.clear()
    return bool(get_trained_model())

def predict_attendance(class_image_np):
    emmbeddings = get_face_embeddings(class_image_np)
    if not emmbeddings:
        return None
    
    detected_students = {}
    model_data = get_trained_model()
    
    if not model_data:
        return detected_students, [], len(emmbeddings)
    
    clf = model_data['Classifier']
    X_train = model_data['X']
    y_train = model_data['y']
    
    all_students = sorted(list(set(y_train)))
    
    for emmbedding in emmbeddings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([emmbedding])[0])
        else:
            predicted_id = int(all_students[0])
        
        studnet_embedding = X_train[y_train.index(predicted_id)]
        
        best_match_score = np.linalg.norm(emmbedding - studnet_embedding)
        threshold = 0.6
        if best_match_score <= threshold:
            detected_students[predicted_id] = True
            
    return detected_students, all_students, len(emmbeddings)
    
    
    
    
    
    