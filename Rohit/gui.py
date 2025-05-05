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
    "Depression": (
        "Establish a consistent daily routine that balances activity and rest, including regular sleep and meal times. "
        "Engage in light physical activity, such as walking outdoors or gentle stretching, even if motivation is low-movement can help lift mood over time. "
        "Stay connected with supportive friends or family members, and consider sharing your feelings with someone you trust. "
        "Set small, achievable goals each day, and try to participate in activities you previously enjoyed, even in brief intervals."
    ),
    "Anxiety": (
        "Incorporate daily relaxation techniques, such as slow deep breathing, progressive muscle relaxation, or guided imagery, to help manage physical symptoms of anxiety. "
        "Practice grounding exercises-focus on your senses by naming five things you can see, four you can touch, three you can hear, two you can smell, and one you can taste-to anchor yourself in the present moment. "
        "Limit stimulants like caffeine and reduce screen time before bed. "
        "Keep a journal to track anxious thoughts and identify patterns or triggers."
    ),
    "Stress": (
        "Prioritize self-care by scheduling regular short breaks throughout your day for relaxation or mindfulness. "
        "Organize your environment to reduce overwhelm, and break larger tasks into smaller, manageable steps. "
        "Practice simple stress-reduction techniques such as deep breathing, gentle stretching, or short walks. "
        "Maintain social connections by reaching out to friends or family, and make time for hobbies or activities that bring you joy. "
        "Reflect on your accomplishments at the end of each day, no matter how small."
    ),
    "ADHD": (
        "Use visual reminders, checklists, and planners to organize tasks and appointments. "
        "Break assignments or chores into smaller, achievable steps and set specific time limits for each. "
        "Establish a consistent daily routine, including regular sleep and meal times, to support focus and predictability. "
        "Incorporate daily physical activity, such as brisk walking or cycling, to help regulate energy and improve concentration. "
        "Minimize distractions in your workspace and use timers to stay on track. "
        "Practice self-acceptance and celebrate progress."
    ),
    "PTSD": (
        "Practice grounding techniques, such as focusing on your breath, describing your surroundings in detail, or holding a comforting object, to help manage distressing memories or feelings. "
        "Engage in creative outlets like drawing, journaling, or music to express emotions safely. "
        "Build a support network by spending time with people or pets who help you feel secure. "
        "Maintain a predictable daily routine and prioritize sleep hygiene. "
        "Avoid self-isolation and gradually reintroduce activities that you find meaningful."
    ),
    "OCD": (
        "Schedule a specific, brief time each day to acknowledge and write down your worries or intrusive thoughts, then redirect your attention to other activities. "
        "Practice mindfulness techniques to observe thoughts without judgment or the need to act on them. "
        "Maintain healthy daily habits, including consistent sleep, balanced nutrition, and regular physical activity."
    ),
    "Bipolar Disorder": (
        "Maintain a stable daily schedule for sleep, meals, and physical activity, as consistency can help regulate mood. "
        "Track your mood changes and energy levels in a journal or app to identify patterns and early warning signs. "
        "Engage in gentle exercise, such as yoga or walking, to support emotional well-being. "
        "Limit alcohol and recreational drugs. "
        "Build a reliable support system of trusted friends or family, and communicate openly about your needs."
    ),
    "Eating Disorder": (
        "Structure your day with regular meals and snacks, aiming to eat at consistent times. "
        "Avoid labeling foods as 'good' or 'bad,' and focus on nourishing your body with a variety of foods. "
        "Practice self-kindness and challenge negative self-talk related to food or appearance. "
        "Engage in activities that foster self-esteem and enjoyment, such as art, music, or spending time with loved ones, that are unrelated to food or body image."
    ),
    "Adjustment Disorder": (
        "Allow yourself time to adapt to recent changes, and acknowledge that adjustment is a process. "
        "Talk to a trusted friend, or a family member, about your experiences and feelings. "
        "Set small, realistic goals each day to foster a sense of accomplishment and control. "
        "Keep a gratitude journal to focus on positive aspects of your life, even during challenging times. "
        "Engage in stress-reducing activities such as deep breathing, gentle exercise, or creative pursuits."
    ),
    "Normal": (
        "Continue to nurture your mental health by maintaining healthy habits, such as regular physical activity, balanced nutrition, and consistent sleep. "
        "Stay connected with friends and family, and make time for enjoyable activities and hobbies. "
        "Practice regular self-reflection to check in with your emotions and stress levels."
    )
}

class MentalHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Mental Health Assessment")
        self.root.geometry("950x700")
        self.root.resizable(False, False)

        # --- Background Image Section ---
        try:
            bg_image = Image.open("space.jpg")  # Use your downloaded image
            bg_image = bg_image.resize((950, 700), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            self.root.configure(bg='#ffe066')  # Sunny yellow fallback

        # --- Main Frame with semi-transparent background ---
        self.main_frame = tk.Frame(self.root, bg='#fffbe6', bd=2, relief='ridge')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=700, height=650)

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
            label = tk.Label(self.main_frame, text=q, anchor='w', bg='#fffbe6', fg='#cc7000', font=('Arial', 14, 'bold'))
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

        self.result_label = tk.Label(self.main_frame, text="", font=('Arial', 18, 'bold'), fg='#007f5f', bg='#fffbe6', wraplength=600)
        self.result_label.grid(row=row, column=0, columnspan=2, pady=20)

        self.recommend_label = tk.Label(self.main_frame, text="", font=('Arial', 14), bg='#fffbe6', fg='#333', wraplength=600, justify='left')
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
