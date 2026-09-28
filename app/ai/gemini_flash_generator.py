from ..config import settings
from .gemini_client import gemini_client

def demo_nutrition_tip(goal):
    g=goal.lower()
    if "muscle" in g or "gain" in g or "strength" in g: return "For muscle and strength goals, include a protein source in each main meal. Eat balanced meals, stay hydrated, and get enough sleep and recovery time."
    if "loss" in g or "weight" in g: return "For weight management, focus on vegetables, protein-rich foods, whole foods and adequate hydration. Avoid crash diets and aim for consistent healthy habits."
    return "Maintain balanced meals with protein, whole grains, fruits and vegetables. Drink enough water and allow adequate recovery after exercise."

def generate_nutrition_tip(goal):
    if settings.AI_DEMO_MODE: return demo_nutrition_tip(goal)
    prompt=f'''You are FitBuddy's nutrition assistant. Fitness goal: {goal}. Provide one concise nutrition and recovery tip, maximum 120 words, in simple English. Encourage balanced nutrition, protein when appropriate, hydration and sleep/recovery. Do not recommend crash diets, medication or medical treatment. Return only the tip.'''
    return gemini_client.generate(prompt, settings.GEMINI_NUTRITION_MODEL)
