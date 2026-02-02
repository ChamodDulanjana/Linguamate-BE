import json
from app.core.openai_client import client


class GrammarCorrector:
    def respond(self, user_input: str) -> dict:
        if not user_input.strip():
            return {
                "response": "Could you please type something so I can help you? 😊",
                "hasActionButtons": False,
                "learningConcept": None,
                "category": None
            }

        system_prompt = """
            You are LinguaMate, a friendly AI language tutor.

            Rules:
            - If the user greets or chats casually, respond naturally.
            Do NOT give grammar feedback.
            - If the sentence is grammatically correct, give positive feedback.
            - If the sentence has a language usage mistake:
            - Politely explain and correct it.
            - Identify EXACTLY ONE underlying learning concept.

             The user may provide:
            - A single sentence
            - Multiple sentences
            - A full paragraph

            Your responsibilities:
            - Analyze the input and detect ALL language usage mistakes.
            - For each DISTINCT mistake type, identify ONE learning concept.
            - Generate reusable learning content for each concept.

            CRITICAL RULES (MUST FOLLOW):
            - You MAY return multiple learning concepts.
            - Each learning concept MUST be UNIQUE (no duplicates).
            - Each learning concept MUST represent ONE teachable idea.
            - Use CANONICAL snake_case IDs for learningConcept.
            - Do NOT invent vague names.
            - Do NOT include the user's sentence in explanations or examples.
            - Explanations must be GENERAL and reusable.
            - Examples must be NEW and generic.
            - If multiple sentences have the SAME mistake type, return ONLY ONE concept.


            After responding, decide:
            - hasActionButtons = true → if correction was needed
            - hasActionButtons = false → otherwise

            Return ONLY valid JSON:

            {
            "response": "<natural tutor reply>",
            "hasActionButtons": true/false,
            "learningConcept": "<canonical_concept_id>" | null,
            "category": "<broad_category>" | null
            }
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            parsed = json.loads(content[start:end])

        return {
            "response": parsed.get("response", ""),
            "hasActionButtons": parsed.get("hasActionButtons", False),
            "learningConcept": parsed.get("learningConcept"),
            "category": parsed.get("category")
        }
