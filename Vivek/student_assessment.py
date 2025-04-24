import joblib
import pandas as pd

# Load model and encoders (trained on 2500 samples)
clf = joblib.load('mental_health_rf_model_2500.pkl')
le_academic = joblib.load('le_academic_2500.pkl')
le_condition = joblib.load('le_condition_2500.pkl')

# Recommendations for different conditions
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

def get_user_input(prompt, options=None):
    """Get input from user with validation"""
    while True:
        if options:
            print(f"{prompt} {options}")
            value = input("> ").strip()
            if value in options:
                return value
            print(f"Please enter one of: {', '.join(options)}")
        else:
            try:
                print(prompt)
                value = input("> ").strip()
                return int(value)
            except ValueError:
                print("Please enter a number")

def predict_mental_health():
    """Main function to predict mental health condition"""
    print("\n===== Student Mental Health Assessment =====\n")

    # Collect inputs
    sleep_hours = get_user_input("How many hours do you sleep per night?")
    academic_performance = get_user_input("Academic performance:", list(le_academic.classes_))
    bullied = 1 if get_user_input("Have you been bullied recently?", ["Yes", "No"]) == "Yes" else 0
    has_close_friends = 1 if get_user_input("Do you have close friends at school?", ["Yes", "No"]) == "Yes" else 0
    homesick_level = get_user_input("How homesick do you feel? (1=Not at all, 5=Extremely)")
    mess_food_rating = get_user_input("How do you rate the mess food? (1=Very bad, 5=Excellent)")
    sports_participation = 1 if get_user_input("Do you participate in sports?", ["Yes", "No"]) == "Yes" else 0
    social_activities = get_user_input("How do you rate your social activities? (0=none, 5=excellent)")
    study_hours = get_user_input("How many hours do you study per day?")
    screen_time = get_user_input("How many hours of screen time per day?")

    # Encode academic performance
    academic_performance_enc = le_academic.transform([academic_performance])[0]

    # Create input dataframe
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

    # Make prediction
    print("\nAnalyzing your responses...")
    pred_idx = clf.predict(input_df)[0]
    condition = le_condition.inverse_transform([pred_idx])[0]

    # Display results
    print("\n===== Assessment Result =====")
    print(f"\nPredicted Condition: {condition}")

    # Display recommendation
    print("\nRecommendation:")
    # Check if condition is "Bipolar" but dictionary has "Bipolar Disorder"
    if condition == "Bipolar" and "Bipolar Disorder" in recommendations:
        print(recommendations["Bipolar Disorder"])
    else:
        print(recommendations.get(condition, "No specific recommendations available."))

    print("\nIf you're concerned about your mental health, please consult a professional.")

if __name__ == "__main__":
    predict_mental_health()
