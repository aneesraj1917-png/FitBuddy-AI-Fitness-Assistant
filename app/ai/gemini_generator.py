from ..config import settings
from .gemini_client import gemini_client

def demo_workout_plan(username, age, weight, goal, intensity):
    return f'''FITBUDDY - PERSONALIZED 7-DAY WORKOUT PLAN

USER: {username} | Age: {age} | Weight: {weight} kg | Goal: {goal} | Intensity: {intensity}

DAY 1 - FULL BODY
Warm-up: 5-10 minutes walking and mobility.
1. Bodyweight Squats - 3 x 12
2. Push-ups - 3 x 8-12
3. Glute Bridges - 3 x 15
4. Plank - 3 x 30 seconds
Rest: 60-90 seconds. Cooldown: 5 minutes.

DAY 2 - CARDIO & CORE
1. Brisk Walking - 20 minutes
2. Mountain Climbers - 3 x 20
3. Bicycle Crunches - 3 x 15
4. Plank - 3 x 30 seconds

DAY 3 - UPPER BODY
1. Push-ups - 3 x 10
2. Incline Push-ups - 3 x 12
3. Chair Dips - 3 x 8
4. Shoulder Taps - 3 x 20

DAY 4 - ACTIVE RECOVERY
20-30 minutes easy walking plus light stretching.

DAY 5 - LOWER BODY
1. Squats - 3 x 12
2. Reverse Lunges - 3 x 10 each leg
3. Glute Bridges - 3 x 15
4. Calf Raises - 3 x 15

DAY 6 - FULL BODY
1. Squats - 3 x 12
2. Push-ups - 3 x 10
3. Lunges - 3 x 10 each leg
4. Plank - 3 x 30 seconds

DAY 7 - REST & RECOVERY
Rest, hydration, balanced meals and adequate sleep.

SAFETY: Start gradually, use proper form, and stop if you experience pain, dizziness, breathing difficulty, or another concerning symptom.'''

def generate_workout(username, age, weight, goal, intensity):
    if settings.AI_DEMO_MODE: return demo_workout_plan(username, age, weight, goal, intensity)
    prompt=f'''You are FitBuddy, an AI fitness planning assistant.
Create a personalized 7-day workout plan for Name: {username}, Age: {age}, Weight: {weight} kg, Goal: {goal}, Intensity: {intensity}.
Requirements: exactly 7 days; adapt to goal/intensity; include warm-up, exercises, sets/reps or duration, rest, cooldown/recovery and rest days; simple English; no diagnosis or unsafe recommendations; end with a short safety note. Return only the plan.'''
    return gemini_client.generate(prompt, settings.GEMINI_WORKOUT_MODEL)
