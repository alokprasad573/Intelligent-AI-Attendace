# Intelligent AI Attendance with Face Recognition

**SmartRoll** is a modern, AI-powered attendance management system that leverages Face Recognition to provide a seamless and secure attendance-tracking experience. Built with Streamlit and Supabase, it offers dedicated portals for both teachers and students.

---

## 🚀 Features

### For Teachers
- **Class Management**: Create and manage multiple classes.
- **Attendance Reports**: View and export detailed attendance logs.
- **QR Code Generation**: Generate unique QR codes for students to join classes easily.
- **Manual Overrides**: Ability to manually mark attendance if needed.

### For Students
- **Face Enrollment**: Securely register facial embeddings for recognition.
- **AI-Powered Attendance**: Mark attendance simply by showing your face to the camera.
- **Enrollment Dashboard**: Track enrolled classes and attendance history.

### Core Technology
- **Face Recognition**: Uses `dlib` and `face_recognition` for high-accuracy facial matching.
- **Real-time Database**: Powered by **Supabase** for instant data synchronization.
- **Glassmorphism UI**: A sleek, modern interface built with Streamlit and custom CSS.

---

## 📊 Database Schema

The system uses a robust relational database structure hosted on Supabase.

[View Database Schema](https://i.ibb.co/8DPPSbxz/supabase-schema-pxjnrmqbfzzoxjyhsebf.png)

![Database Schema](https://i.ibb.co/8DPPSbxz/supabase-schema-pxjnrmqbfzzoxjyhsebf.png)

---

## 🧠 Face Recognition Pipeline

The system follows a state-of-the-art deep learning pipeline for face detection and identification.

### 1. Feature Extraction (Embedding Generation)
```mermaid
graph LR
    A[Face Image] --> B[Face Detector dlib]
    B --> C[Shape Predictor sp - Landmarks]
    C --> D[ResNet facerec]
    D --> E[128D Embedding]
```

### 2. Identification Process
```mermaid
graph LR
    F[Face Image] --> G[ResNet Feature Extractor]
    G --> H[128D Embedding Face Descriptor]
    H --> I[KNN Classifier]
    I --> J[Student ID]
```


---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Database**: [Supabase](https://supabase.com/)
- **AI Models**: 
  - Face: `face_recognition` (dlib-based)
- **Backend Logic**: Python
- **Utilities**: `bcrypt` (Hashing), `segno` (QR Codes), `pandas`, `numpy`

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Intelligent-AI-Attendance.git
cd Intelligent-AI-Attendance
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create a `.streamlit/secrets.toml` file and add your Supabase credentials:
```toml
SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_key"
SUPABASE_PASSW = "your_database_password"
```

### 5. Run the Application
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```text
├── .streamlit/          # Streamlit configuration & secrets
├── src/
│   ├── components/      # Reusable UI components
│   ├── databases/       # Database connection & queries
│   ├── pipelines/       # AI logic (Face & Voice recognition)
│   ├── screens/         # Page layouts (Home, Teacher, Student)
│   └── ui/              # Custom CSS and styling
├── app.py               # Main entry point
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🛡️ Security
- **Data Privacy**: Facial embeddings are stored as mathematical vectors, not raw images/audio.
- **Authentication**: Secure password hashing using `bcrypt`.

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License
This project is licensed under the MIT License.
