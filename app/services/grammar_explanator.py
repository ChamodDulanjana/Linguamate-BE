import json
from app.core.openai_client import client


class GrammarExplanator:
    def respond(self, learning_concept: str, category: str) -> dict:
        if not learning_concept.strip():
            return {
                "learningConceptExplanation": "",
                "learningConceptExamples": []
            }
        system_prompt = """
            You are LinguaMate, an AI language learning content generator.

            This task is NOT conversation.
            This task is to GENERATE LEARNING CONTENT for a GIVEN concept.

            You will receive:
            - learningConcept (canonical snake_case ID)
            - category (broad category)

            Your responsibilities:
            - Generate a GENERAL explanation of the learning concept.
            - Generate EXACTLY 3 example pairs (correct vs incorrect).
            - Examples must be GENERIC and reusable.
            - Do NOT reference any user input.
            - Do NOT add extra concepts.
            - Do NOT rename the learning concept.

            STRICT RULES:
            - Explanation must be concise and neutral.
            - Incorrect examples must be realistic learner mistakes.
            - Do NOT include markdown or extra text.

            Return ONLY valid JSON:

            {
                "learningConceptExplanation": "<general explanation>",
                "learningConceptExamples": [
                    { "correct": "...", "incorrect": "..." }
                ]
            }
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": json.dumps({
                        "learningConcept": learning_concept,
                        "category": category
                    })
                }
            ],
            temperature=0.2  # LOW = stable output
        )

        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            parsed = json.loads(content[start:end])

        return {
            "learningConcept": learning_concept,
            "category": category,
            "learningConceptExplanation": parsed.get(
                "learningConceptExplanation", ""
            ),
            "learningConceptExamples": parsed.get(
                "learningConceptExamples", []
            )
        }
