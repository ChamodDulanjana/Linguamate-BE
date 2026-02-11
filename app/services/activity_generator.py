import json
from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry


class ActivityGenerator:
    def generate(self, learning_concepts: list[str], activity_type: str) -> dict:

        prompt_map = {
            "QUIZ": QUIZ_PROMPT,
            "FILL_IN_THE_BLANKS": FILL_BLANK_PROMPT,
            "SPEAKING_PRACTICE": SPEAKING_PROMPT
        }

        system_prompt = prompt_map.get(activity_type)
        if not system_prompt:
            raise ValueError("Invalid activity type")

        response = call_openai_with_retry(
            lambda: client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": json.dumps({
                            "learningConcepts": learning_concepts
                        })
                    }
                ],
                temperature=0.5
            )
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)

        return parsed


QUIZ_PROMPT = """
    You are LinguaMate, an AI language learning activity generator.

    Task: Generate a multiple-choice quiz based on the learning concepts provided. Only Quiz questions should be generated.
    Do not generate any other content like fill-in-the-blanks or speaking practice.

    Input:
    - learningConcepts: list of human-readable grammar concepts

    Rules:
    - Generate EXACTLY 5 questions.
    - Each question must test ONE or MORE of the given learning concepts.
    - Each question must have EXACTLY 4 options.
    - ONLY ONE option must be correct.
    - Incorrect options must be realistic learner mistakes.
    - shuffle the options.
    - Do not include markdown.
    - Do not add extra text outside JSON.

    Output Format (JSON only):
    {
        "activityType": "QUIZ",
        "questions": [
            {
                "question": "What is the correct form of the verb?",
                "options": ["...", "...", "...", "..."],
                "correctOptionIndex": 0 | 1 | 2 | 3
            }
        ]
    }

    
"""

FILL_BLANK_PROMPT = """
    You are LinguaMate, an AI language learning activity generator.

    Task: Generate a fill-in-the-blank exercise based on the learning concepts provided.

    Input:
    - learningConcepts: list of human-readable grammar concepts

    Output Format (JSON only):
    {
        "activityType": "FILL_IN_THE_BLANKS",
        "title": "Fill in the Blanks: [Concepts]",
        "description": "Complete the sentences using the correct forms",
        "instructions": "Fill in the blanks with the correct word or phrase.",
        "sentences": [
            {
                "sentenceId": "1",
                "text": "She ___ (go) to the park yesterday.",
                "correctAnswer": "went",
                "explanation": "Use simple past tense for completed past actions."
            }
        ]
    }

    Rules:
    - Generate 5 sentences.
    - Each sentence must target ONE specific concept.
    - Use the learningConcepts to create relevant sentences.
    - Provide clear explanation for each answer.
    - Do NOT include markdown.
    - Do NOT add extra text outside JSON.
"""

SPEAKING_PROMPT = """
    You are LinguaMate, an AI language learning activity generator.

    Task: Generate speaking practice prompts based on the learning concepts provided.

    Input:
    - learningConcepts: list of human-readable grammar concepts

    Output Format (JSON only):
    {
        "activityType": "SPEAKING_PRACTICE",
        "title": "Speaking Practice: [Concepts]",
        "description": "Practice speaking about [Concepts]",
        "instructions": "Speak for 30-60 seconds on each topic.",
        "prompts": [
            {
                "promptId": "1",
                "topic": "Topic related to concept",
                "guidingQuestions": [
                    "Question 1?",
                    "Question 2?"
                ],
                "learningConcept": "Concept name"
            }
        ]
    }

    Rules:
    - Generate 3 prompts.
    - Each prompt must target ONE specific concept.
    - Provide 2-3 guiding questions per prompt.
    - Do NOT include markdown.
    - Do NOT add extra text outside JSON.
"""
