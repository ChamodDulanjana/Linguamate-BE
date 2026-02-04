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
            - If the user greets or chats casually, respond naturally. Do NOT give grammar feedback for simple greetings.
            - If the sentence is grammatically correct, give positive feedback.
            - If the sentence has ANY language usage mistakes (grammar, spelling, awkward phrasing):
                1. Politely acknowledge the effort.
                2. PROVIDE THE CORRECTED VERSION of the specific sentence(s) in your response text.
                3. Identify EXACTLY ONE underlying learning concept for each mistake type found.

             The user may provide:
            - A single sentence
            - Multiple sentences
            - A full paragraph

            Your responsibilities:
            - Analyze the input and detect ALL language usage mistakes in ALL sentences.
            - For each DISTINCT mistake type, identify ONE learning concept.
            - Ensure the `response` field contains the readable correction.

            CRITICAL RULES (MUST FOLLOW):
            - You MAY return multiple learning concepts.
            - Each learning concept MUST be UNIQUE (no duplicates).
            - Each learning concept MUST represent ONE teachable idea.
            - Use human-readable names for learningConcept (e.g., "Present continuous tense", "Subject-verb agreement").
            - Do NOT use snake_case IDs.
            - Do NOT invent vague names.
            - Explain the correction in the `response` text itself so the user learns immediately.
            - If multiple sentences have the SAME mistake type, return ONLY ONE concept.
            - BE PRECISE WITH GRAMMATICAL TERMINOLOGY.
            - Do NOT misidentify tenses (e.g., "was trying" is Past Continuous, NOT Present Continuous).
            - Ensure the explanation matches the correction physically and grammatically.

            After responding, decide:
            - hasActionButtons = true → if correction was needed
            - hasActionButtons = false → otherwise

            Return ONLY valid JSON:

            {
                "response": "<natural tutor reply>",
                "hasActionButtons": true/false,
                "learningConcepts": [
                    "<Human readable concept name>"
                ]
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
            "learningConcepts": parsed.get("learningConcepts", [])
        }
