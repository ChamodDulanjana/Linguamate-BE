import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class GrammarCorrector:
    def respond(self, user_input: str) -> dict:
        if not user_input.strip():
            return {
                "response": "Could you please type something so I can help you? 😊"
            }

        system_prompt = """
            You are LinguaMate, a friendly and polite AI English tutor.

            Your behavior rules:
            - If the user greets (hi, hello, good morning, etc.), respond warmly and naturally. Do NOT correct grammar.
            - If the user explicitly asks to correct grammar, help them politely with explanation.
            - If the user writes a sentence with a grammar mistake, gently explain and correct it.
            - If the sentence is already correct, give positive feedback.
            - Never sound robotic or harsh.
            - Vary responses slightly each time.
            - Keep explanations short, friendly, and easy to understand.
            - Do NOT show labels like "Corrected:" or "Original:".
            - Respond like a human tutor chatting with a student.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        reply = response.choices[0].message.content.strip()

        return {
            "response": reply
        }
