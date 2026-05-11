import dlib 
import face_recognition_models
import streamlit as st
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from src.databases.db import get_all_students

from PIL import Image, ImageEnhance

# Loading dlib models
@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    face_recognizer = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return detector, sp, face_recognizer

def preprocess_image(image_array):
    # Convert numpy array to PIL Image
    img = Image.fromarray(image_array)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    
    # Enhance brightness slightly
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    return np.array(img)

# getting face embeddings
def get_face_embbedings(image_array):
    detector, sp, face_recognizer = load_dlib_models()
    
    # Try with original image
    faces = detector(image_array, 1)
    
    # If no faces found, try with preprocessed image
    if len(faces) == 0:
        enhanced_image = preprocess_image(image_array)
        faces = detector(enhanced_image, 1)
        if len(faces) > 0:
            image_array = enhanced_image
            
    # If still no faces found, try upsampling more (slower but better for small faces)
    if len(faces) == 0:
        faces = detector(image_array, 2)
    
    embeddings = []
    for face in faces:
        landmarks = sp(image_array, face)
        embedding = face_recognizer.compute_face_descriptor(image_array, landmarks, 1) # 128 embeddings
        embeddings.append(np.array(embedding).tolist())
    
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
        embeddings = student.get('face_embeddings', [])
        if embeddings and isinstance(embeddings, list):
            # Take the first embedding if it's a list of embeddings
            first_embedding = embeddings[0] if isinstance(embeddings[0], list) else embeddings
            X.append(np.array(first_embedding))
            y.append(student['id'])
    
    if len(X) == 0:
        return None
    
    # KNN works even with a single class
    clf = KNeighborsClassifier(n_neighbors=1, metric='euclidean')
    try:
        clf.fit(X, y)
        return {'clf': clf, 'X': X, 'y': y}
    except Exception as e:
        st.error(f"Error training model: {e}")
        return None
    
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
    y_train = model_data['y']
    
    all_students = sorted(list(set(y_train)))
    
    resemblance_threshold = 0.6
    
    for embedding in embeddings:
        # Use KNN to find the nearest neighbor and its distance
        distances, indices = clf.kneighbors([embedding], n_neighbors=1)
        
        best_match_score = distances[0][0]
        predicted_id = clf.classes_[indices[0][0]]
        
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True
            
    return detected_student, all_students, len(embeddings)
            
    
    
        
        
