import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
from PIL import Image, ImageTk

# Load model and encoders
clf = joblib.load('mental_health_rf_model.pkl')
le_academic = joblib.load('le_academic.pkl')
le_condition = joblib.load('le_condition.pkl')

recommendations = {
    'Depression': "Engage in regular exercise, maintain social connections, and seek support from friends/family. If symptoms persist, consult a mental health professional.",
    'Anxiety': "Practice relaxation techniques (deep breathing, meditation). Maintain a routine, avoid excessive caffeine, and talk to someone you trust. Seek professional help if anxiety interferes with daily life.",
    'Stress': "Try mindfulness, yoga, or physical activity. Break tasks into manageable steps and take regular breaks. Reach out to support groups or counselors if needed.",
    'ADHD': "Establish routines, use reminders, and break tasks into smaller steps. Consider professional evaluation for therapy or medication if attention issues are persistent.",
    'PTSD': "Seek trauma-informed counseling. Practice grounding techniques and connect with support groups. Professional therapy (CBT, EMDR) is highly recommended.",
    'OCD': "Cognitive-behavioral therapy (CBT) is effective. Practice exposure and response prevention with professional guidance. Medication may help in some cases.",
    'Bipolar Disorder': "Consult a psychiatrist for mood stabilizers and therapy. Maintain regular sleep and activity patterns. Avoid substance misuse and seek ongoing support.",
    'Eating Disorder': "Seek help from a nutritionist and mental health professional. Join support groups and involve family in recovery. Early intervention is key.",
    'Adjustment Disorder': "Talk to a counselor about recent changes. Practice stress management and self-care. Most cases resolve with time and support.",
    'Normal': "Continue healthy habits: regular sleep, balanced diet, exercise, and social engagement. Monitor your well-being and seek help if you notice changes."
}

class MentalHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Mental Health Assessment")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # --- Background Image Section ---
        try:
            bg_image = Image.open("space.jpg")  # Use your downloaded image
            bg_image = bg_image.resize((900, 700), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            self.root.configure(bg='#ffe066')  # Sunny yellow fallback

        # --- Main Frame with semi-transparent background ---
        self.main_frame = tk.Frame(self.root, bg='#fffbe6', bd=2, relief='ridge')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=700, height=600)

        self.entries = {}
        questions = [
            ("How many hours do you sleep per night?", "sleep_hours", tk.Entry),
            ("Academic performance (Poor/Average/Good):", "academic_performance", ttk.Combobox),
            ("Have you been bullied recently? (Yes/No):", "bullied", ttk.Combobox),
            ("Do you have close friends at school? (Yes/No):", "has_close_friends", ttk.Combobox),
            ("How homesick do you feel? (1=Not at all, 5=Extremely):", "homesick_level", tk.Entry),
            ("How do you rate the mess food? (1=Very bad, 5=Excellent):", "mess_food_rating", tk.Entry),
            ("Do you participate in sports? (Yes/No):", "sports_participation", ttk.Combobox),
            ("How do you rate your social activities?", "social_activities", tk.Entry),
            ("How many hours do you study per day?", "study_hours", tk.Entry),
            ("How many hours of screen time per day?", "screen_time", tk.Entry)
        ]

        row = 0
        for q, key, widget in questions:
            label = tk.Label(self.main_frame, text=q, anchor='w', bg='#fffbe6', fg='#cc7000', font=('Arial', 12, 'bold'))
            label.grid(row=row, column=0, sticky='w', padx=10, pady=6)
            if widget == ttk.Combobox:
                if "Academic" in q:
                    entry = ttk.Combobox(self.main_frame, values=list(le_academic.classes_), state='readonly')
                else:
                    entry = ttk.Combobox(self.main_frame, values=["Yes", "No"], state='readonly')
                entry.current(0)
            else:
                entry = widget(self.main_frame)
            entry.grid(row=row, column=1, padx=10, pady=6, sticky="ew")
            self.entries[key] = entry
            row += 1

        self.result_label = tk.Label(self.main_frame, text="", font=('Arial', 16, 'bold'), fg='#007f5f', bg='#fffbe6', wraplength=600)
        self.result_label.grid(row=row, column=0, columnspan=2, pady=20)

        self.recommend_label = tk.Label(self.main_frame, text="", font=('Arial', 12), bg='#fffbe6', fg='#333', wraplength=600, justify='left')
        self.recommend_label.grid(row=row+1, column=0, columnspan=2, pady=10)

        submit_btn = tk.Button(self.main_frame, text="Predict", font=('Arial', 12, 'bold'), bg='#f9c74f', fg='#333', command=self.predict)
        submit_btn.grid(row=row+2, column=0, columnspan=2, pady=10)

    def predict(self):
        try:
            sleep_hours = int(self.entries['sleep_hours'].get())
            academic_performance = self.entries['academic_performance'].get()
            bullied = 1 if self.entries['bullied'].get().lower() == "yes" else 0
            has_close_friends = 1 if self.entries['has_close_friends'].get().lower() == "yes" else 0
            homesick_level = int(self.entries['homesick_level'].get())
            mess_food_rating = int(self.entries['mess_food_rating'].get())
            sports_participation = 1 if self.entries['sports_participation'].get().lower() == "yes" else 0
            social_activities = int(self.entries['social_activities'].get())
            study_hours = int(self.entries['study_hours'].get())
            screen_time = int(self.entries['screen_time'].get())

            academic_performance_enc = le_academic.transform([academic_performance])[0]

            input_dict = {
                'sleep_hours': [sleep_hours],
                'academic_performance': [academic_performance_enc],
                'bullied': [bullied],
                'has_close_friends': [has_close_friends],
                'homesick_level': [homesick_level],
                'mess_food_rating': [mess_food_rating],
                'sports_participation': [sports_participation],
                'social_activities': [social_activities],
                'study_hours': [study_hours],
                'screen_time': [screen_time]
            }
            input_df = pd.DataFrame(input_dict)

            pred_idx = clf.predict(input_df)[0]
            condition = le_condition.inverse_transform([pred_idx])[0]

            self.result_label.config(text=f"Predicted Condition: {condition}")
            self.recommend_label.config(text=f"Recommendation:\n{recommendations.get(condition, '')}")

        except Exception as e:
            messagebox.showerror("Input Error", f"Please check your inputs.\nError: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MentalHealthApp(root)
    root.mainloop()
