import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
from PIL import Image, ImageTk
import random
import math
from datetime import datetime

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

class Particle:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.size = random.randint(2, 5)
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.alpha = random.uniform(0.1, 0.9)
        self.color = self.get_random_color()
        self.id = canvas.create_oval(
            self.x, self.y,
            self.x + self.size, self.y + self.size,
            fill=self.color, outline=''
        )

    def get_random_color(self):
        # Generate a nice color palette for particles
        colors = ['#4a4e69', '#9a8c98', '#c9ada7', '#f2e9e4', '#22223b', '#4a4e69']
        return random.choice(colors)

    def update(self):
        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges
        if self.x <= 0 or self.x >= self.width:
            self.vx *= -1
        if self.y <= 0 or self.y >= self.height:
            self.vy *= -1

        # Move the particle on canvas
        self.canvas.move(self.id, self.vx, self.vy)

class MentalHealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Mental Health Assessment")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # --- Animated Background Canvas ---
        self.canvas = tk.Canvas(self.root, width=900, height=700, highlightthickness=0)
        self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Create gradient background
        self.create_gradient_background()

        # Create particles
        self.particles = []
        for _ in range(50):  # Number of particles
            self.particles.append(Particle(self.canvas, 900, 700))

        # Start animation
        self.animate_particles()

        # Create a semi-transparent effect for the main frame
        # First, create a transparent frame
        self.main_frame = tk.Frame(self.root, bg='', bd=0, highlightthickness=0)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=700, height=650)

        # Create a canvas for the semi-transparent background
        self.frame_bg = tk.Canvas(self.main_frame, width=700, height=650, highlightthickness=0)
        self.frame_bg.place(x=0, y=0)

        # Draw a semi-transparent rectangle on the canvas
        # Use a more transparent stipple pattern
        self.frame_bg.create_rectangle(0, 0, 700, 650, fill='#fffbe6', outline='#9a8c98', width=3, stipple='gray25')

        # Add title label with transparent background
        title_label = tk.Label(self.main_frame, text="Mental Health Assessment", font=("Arial", 18, "bold"),
                              bg="#fffbe6", fg="#22223b")
        title_label.grid(row=0, column=0, columnspan=2, pady=(15, 25))
        title_label.configure(bg='#fffbe6')

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

        row = 1  # Start from row 1 because title is at row 0
        for q, key, widget in questions:
            # Create labels with semi-transparent background
            label = tk.Label(self.main_frame, text=q, anchor='w', bg='#fffbe6', fg='#cc7000', font=('Arial', 11, 'bold'))
            label.grid(row=row, column=0, sticky='w', padx=10, pady=4)

            # Style for comboboxes
            style = ttk.Style()
            style.configure('TCombobox', fieldbackground='white', background='white')

            if widget == ttk.Combobox:
                if "Academic" in q:
                    entry = ttk.Combobox(self.main_frame, values=list(le_academic.classes_), state='readonly')
                else:
                    entry = ttk.Combobox(self.main_frame, values=["Yes", "No"], state='readonly')
                entry.current(0)
            else:
                entry = widget(self.main_frame, bg='white')
            entry.grid(row=row, column=1, padx=10, pady=4, sticky="ew")
            self.entries[key] = entry
            row += 1

        # Create result labels with semi-transparent background
        self.result_label = tk.Label(self.main_frame, text="", font=('Arial', 16, 'bold'), fg='#007f5f', bg='#fffbe6', wraplength=600)
        self.result_label.grid(row=row, column=0, columnspan=2, pady=10)

        self.recommend_label = tk.Label(self.main_frame, text="", font=('Arial', 12), bg='#fffbe6', fg='#333', wraplength=600, justify='left')
        self.recommend_label.grid(row=row+1, column=0, columnspan=2, pady=5)

        # Create a frame for the button with transparent background
        btn_frame = tk.Frame(self.main_frame, bg='#fffbe6')
        btn_frame.grid(row=row+2, column=0, columnspan=2, pady=10)

        # Create a more visible button
        submit_btn = tk.Button(btn_frame, text="Predict", font=('Arial', 12, 'bold'),
                              bg='#22223b', fg='white',
                              activebackground='#4a4e69', activeforeground='white',
                              relief=tk.RAISED, bd=2, padx=20, pady=5,
                              command=self.predict)
        submit_btn.pack(pady=5)

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

    def create_gradient_background(self):
        # Create a gradient background from dark to light
        for y in range(700):
            # Calculate color based on y position
            r = int(33 + (y/700) * 40)
            g = int(34 + (y/700) * 40)
            b = int(59 + (y/700) * 40)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, y, 900, y, fill=color, width=1)

    def animate_particles(self):
        # Update all particles
        for particle in self.particles:
            particle.update()

        # Schedule the next animation frame
        self.root.after(50, self.animate_particles)

if __name__ == "__main__":
    root = tk.Tk()
    app = MentalHealthApp(root)
    root.mainloop()
