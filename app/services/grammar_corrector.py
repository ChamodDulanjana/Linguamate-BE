import json
from app.core.openai_client import client


class GrammarCorrector:
    def respond(self, user_input: str) -> dict:
        if not user_input.strip():
            return {
                "response": "Could you please type something so I can help you? 😊",
                "hasActionButtons": False
            }

        system_prompt = """
            You are LinguaMate, a friendly AI language tutor.

            Rules:
            - If the user greets or chats casually, respond naturally. No grammar feedback.
            - If the sentence has a grammar mistake, politely explain and correct it.
            - If the sentence is already correct, give positive feedback.
            - Sound friendly, human, and encouraging.

            After responding, decide:
            - hasActionButtons = true → if grammar correction was needed
            - hasActionButtons = false → otherwise

            Return ONLY valid JSON in this format:
            {
            "response": "<natural tutor reply>",
            "hasActionButtons": true/false
            }
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},  # forces JSON
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5
        )

        # Parse JSON safely
        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            # fallback: extract JSON manually
            start = content.find("{")
            end = content.rfind("}") + 1
            parsed = json.loads(content[start:end])

        return {
            "response": parsed.get("response", ""),
            "hasActionButtons": parsed.get("hasActionButtons", False)
        }
