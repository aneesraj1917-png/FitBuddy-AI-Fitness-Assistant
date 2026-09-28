from ..config import settings
from .gemini_client import gemini_client

def demo_updated_plan(original_plan, feedback):
    return f'''FITBUDDY - UPDATED 7-DAY WORKOUT PLAN

USER FEEDBACK:
{feedback}

DAY 1 - FULL BODY
1. Squats - 3 x 12
2. Push-ups - 3 x 10
3. Glute Bridges - 3 x 15
4. Plank - 3 x 30 seconds

DAY 2 - CARDIO & CORE
1. Brisk Walking - 20-25 minutes
2. Bicycle Crunches - 3 x 15
3. Plank - 3 x 30 seconds

DAY 3 - UPPER BODY
1. Push-ups - 3 x 10
2. Shoulder Taps - 3 x 20
3. Chair Dips - 3 x 8

DAY 4 - RECOVERY
Light walking and stretching.

DAY 5 - LOWER BODY
1. Squats - 3 x 12
2. Reverse Lunges - 3 x 10 each leg
3. Calf Raises - 3 x 15

DAY 6 - FULL BODY
1. Squats - 3 x 12
2. Push-ups - 3 x 10
3. Lunges - 3 x 10
4. Plank - 3 x 30 seconds

DAY 7 - REST
Complete rest and recovery.

SAFETY: Progress gradually and stop if you experience pain, dizziness, breathing difficulty, or another concerning symptom.'''

def update_plan(original_plan, feedback, username, age, weight, goal, intensity):
    if settings.AI_DEMO_MODE: return demo_updated_plan(original_plan, feedback)
    prompt=f'''You are FitBuddy, an AI fitness planning assistant.
User: {username}, Age: {age}, Weight: {weight} kg, Goal: {goal}, Intensity: {intensity}
ORIGINAL PLAN:\n{original_plan}
USER FEEDBACK:\n{feedback}
Create an updated 7-day plan applying the feedback while keeping useful parts. Include warm-up, exercises, sets/reps or duration, rest/recovery and a short safety note. Use simple English. Return only the updated plan.'''
    return gemini_client.generate(prompt, settings.GEMINI_WORKOUT_MODEL)
