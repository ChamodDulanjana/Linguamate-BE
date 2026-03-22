import json
from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry


class GrammarExplanator:
    def respond(self, learning_concepts: list[str], language: str) -> list[dict]:
        if not learning_concepts:
            return []
            
        system_prompt = f"""
            You are LinguaMate, an AI language learning content generator.

            Detected language: {language}

            IMPORTANT LANGUAGE RULES:
            - Generate ALL explanations and examples in the detected language.
            - Use grammatical terminology appropriate for the detected language.
            - Do NOT assume English grammar rules unless language = "en".
            - If language is unknown, default to English.

            This task is NOT conversation.
            This task is to GENERATE LEARNING CONTENT for given concepts.

            You will receive:
            - learningConcepts (list of human-readable grammar concepts)

            Your responsibilities for EACH concept:
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
            - Always return explanations in the SAME ORDER as input learningConcepts.

            Return ONLY valid JSON in this format:
        """ + """
            {
                "explanations": [
                    {
                        "learningConcept": "<concept name>",
                        "learningConceptExplanation": "<general explanation>",
                        "learningConceptExamples": [
                            { "correct": "...", "incorrect": "..." }
                        ]
                    }
                ]
            }
        """

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
                temperature=0.2  # LOW = stable output
            )
        )

        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            parsed = json.loads(content[start:end])

        return parsed.get("explanations", [])
