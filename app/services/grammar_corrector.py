import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class GrammarCorrector:
    def correct_grammar(self, text: str) -> dict:
        if not text.strip():
            return {
                "original": text,
                "corrected": text,
                "explanation": "No text provided."
            }

        prompt = (
            "You are an English grammar tutor. "
            "Correct the sentence and explain the correction briefly.\n\n"
            f"Sentence: {text}\n\n"
            "Return response in this format:\n"
            "Corrected: <sentence>\n"
            "Explanation: <short explanation>"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful grammar assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        corrected = ""
        explanation = ""

        for line in content.split("\n"):
            if line.lower().startswith("corrected"):
                corrected = line.split(":", 1)[1].strip()
            elif line.lower().startswith("explanation"):
                explanation = line.split(":", 1)[1].strip()

        return {
            "original": text,
            "corrected": corrected or text,
            "explanation": explanation or "No explanation provided."
        }
