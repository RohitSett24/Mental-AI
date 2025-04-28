1. Requirement Specification

🔧 Software Requirements: Python 3.x

Libraries: pandas, numpy, scikit-learn, joblib, tkinter

IDE: VS Code / PyCharm / Jupyter Notebook

📂 Files Required:
boarding_school_mental_health_1000.csv (Dataset)
train_model.py (Model training code)
student_assessment.py (CLI-based interaction logic)
gui_app.py (Tkinter GUI to interact with users)

🧠 Functional Requirements:
Load and preprocess student mental health data.
Train a machine learning model (Random Forest) to classify mental health conditions.
Allow user inputs via GUI (or CLI).
Predict a student’s likely mental health condition based on lifestyle and school experiences.
Recommend personalized, practical coping strategies based on prediction.


💡 2. Motivation

In today’s highly competitive and socially pressured school environments, boarding school students often experience mental health issues like anxiety, depression, and stress. However, due to stigma, lack of awareness, or limited resources, early detection and intervention rarely happen.

This project aims to:

Bridge that gap with a smart, simple, and interactive tool.
Empower students to understand their mental state.
Provide helpful and stigma-free advice instantly — even before talking to a counselor.
The goal is not to replace professionals but to encourage self-awareness and early action — in a way that feels safe, private, and approachable.


🧪 3. Description of Usage of the Project

👨‍🎓 End User:
Primarily boarding school students, but also useful for:

School counselors (as a quick screening tool)
Parents/teachers
College students under pressure

🕹️ How It Works:
The student launches the GUI window (gui_app.py).
They answer simple questions like:
Sleep hours, screen time, if they feel homesick, study time, etc.
The model predicts their mental health condition (e.g., Stress, Depression, Normal, etc.)
Based on the prediction, a custom recommendation is displayed immediately.

🔒 Privacy:
No sensitive personal data stored or shared.
Users answer anonymously, which increases honesty and reliability.


🤖 4. How AI is Enabling the System

🧠 Machine Learning (AI) Role:

Classification: A trained Random Forest model classifies mental health conditions based on input features.
Features include both numerical (e.g., sleep hours) and categorical/boolean (e.g., bullied, academic performance).
Label encoding converts categories into model-friendly numbers.

Pattern Recognition: ML model identifies hidden relationships between lifestyle patterns and mental states that may not be obvious to humans.

Decision Making: Instead of relying on rigid rules, the system learns from real student data to make decisions — adapting to various input combinations.

Recommendations System: AI not only predicts but triggers context-specific advice. These aren't random tips — they’re tied directly to the model's classification.
