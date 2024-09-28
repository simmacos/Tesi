from flask import Blueprint, jsonify, request
import requests
import os
import json
from dotenv import load_dotenv
import random

load_dotenv()

quests_ai_bp = Blueprint('quests_ai', __name__)

@quests_ai_bp.route('/generate_quests', methods=['POST'])
def generate_quests():
    try:
        user_data = request.json
        habits = user_data.get('habits', [])
        goals = user_data.get('goals', [])

        # Scegli casualmente 3 goal diversi
        selected_goals = random.sample(goals, k=min(3, len(goals)))

        url = "https://api.perplexity.ai/chat/completions"

        prompt = f"""
        Generate 3 unique, practical, and engaging daily quests for a productivity app. Each quest should be a small step towards one of these goals: {', '.join(selected_goals)}.

        Key requirements:
        1. Each quest must be completable in 15-120 minutes.
        2. Quests should be specific, actionable, and measurable.
        3. Focus on practical, real-world actions that directly contribute to the goal.
        4. Avoid generic advice or vague suggestions.
        5. Do not repeat or closely resemble the user's existing habits.
        6. Quests should be diverse: mix digital tasks, physical activities, and personal development.
        7. Occasionally (15% chance), include a brief self-reflection or mindfulness task.
        8. Be creative and think outside the box - suggest actions the user might not have considered.
        9. For each quest, determine its difficulty (EASY, MEDIUM, or HARD) and the most relevant skill category.

        User's existing habits (DO NOT SUGGEST THESE): {', '.join(habits)}

        Skill categories:
        - GENERAL: General life skills and activities
        - CULTURE: Activities related to arts, literature, history, etc.
        - SPORT: Physical activities and sports
        - WELLBEING: Mental and physical health, self-care
        - PRODUCTIVITY: Work-related skills, time management, organization
        - CREATIVITY: Artistic pursuits, problem-solving, innovation
        - SOCIAL: Interpersonal skills, communication, networking

        For each goal, consider various types of actions. The following are just examples to inspire creativity, not to limit your suggestions:
        - Job change/remote work: Skill development, job search activities, networking, personal branding.
        - Reducing anxiety: Confidence-building exercises, social interactions, stress management techniques, exposure therapy.
        - Finding a partner: Self-improvement, social activities, communication skills, self-reflection.
        - Active social life: Community involvement, event planning, reaching out to friends/acquaintances, trying new social activities.
        - Buying a house with a farm: Financial planning, agricultural knowledge, property research, sustainability practices.

        Be creative and suggest actions beyond these examples that are relevant to the user's goals.

        Respond ONLY with a JSON object containing 3 quests, each with a title, description, difficulty, and skill:

        {{
            "quests": [
                {{
                    "title": "Concise, action-oriented title",
                    "description": "Brief explanation of the task and how it contributes to the goal",
                    "difficulty": "EASY/MEDIUM/HARD",
                    "skill": "GENERAL/CULTURE/SPORT/WELLBEING/PRODUCTIVITY/CREATIVITY/SOCIAL"
                }},
                {{
                    "title": "Concise, action-oriented title",
                    "description": "Brief explanation of the task and how it contributes to the goal",
                    "difficulty": "EASY/MEDIUM/HARD",
                    "skill": "GENERAL/CULTURE/SPORT/WELLBEING/PRODUCTIVITY/CREATIVITY/SOCIAL"
                }},
                {{
                    "title": "Concise, action-oriented title",
                    "description": "Brief explanation of the task and how it contributes to the goal",
                    "difficulty": "EASY/MEDIUM/HARD",
                    "skill": "GENERAL/CULTURE/SPORT/WELLBEING/PRODUCTIVITY/CREATIVITY/SOCIAL"
                }}
            ]
        }}
        """

        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant for a productivity app. Your role is to generate practical, diverse, and engaging daily quests that help users take small steps towards their long-term goals. Focus on specific, actionable tasks that can be completed in 15-30 minutes. Always respond with a valid JSON object containing exactly 3 quests, each with a title, description, difficulty, and skill category."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7,
            "top_p": 0.9,
            "return_citations": False,
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        quest_data = response.json()
        
        content = quest_data['choices'][0]['message']['content']
        content = content.strip().lstrip('`').rstrip('`')
        if content.startswith('json'):
            content = content[4:].strip()
        
        generated_quests = json.loads(content)

        return jsonify(generated_quests), 200

    except requests.RequestException as e:
        print(f"API request error: {str(e)}")
        return jsonify({'error': 'Failed to generate quests'}), 500
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {str(e)}")
        print(f"Problematic content: {content}")
        return jsonify({'error': 'Failed to parse generated quests', 'content': content}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
