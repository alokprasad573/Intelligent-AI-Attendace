import numpy as np
from sklearn.svm import SVC

# Simulating the behavior in face_recognition_pipeline.py
X = []
y = []

# Mock student data (list of lists of floats)
student_1_emb = [[0.1] * 128]
student_2_emb = [[0.2] * 128]

X.append(np.array(student_1_emb))
y.append("S1")
X.append(np.array(student_2_emb))
y.append("S2")

print(f"X shape: {np.array(X).shape}")

clf = SVC(kernel='linear', probability=True, class_weight='balanced')
try:
    clf.fit(X, y)
    print("Fit successful")
except ValueError as e:
    print(f"Fit failed with ValueError: {e}")
