import json
from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry

class ConceptExtractor:

    def extract(self, original_text: str, corrected_text: str, language: str) -> list[str]:

        CONCEPT_EXTRACTOR_PROMPT = f"""
            You are LinguaMate AI language learning Concept Extractor.

            Detected language: {language}

            IMPORTANT:
            - Always respond in the detected language unless the user switches language.
            - Do NOT assume English unless language = "en".

            TASK:
            Identify grammar learning concepts by comparing ORIGINAL text and CORRECTED text.

            INPUT:
            - originalText
            - correctedText
            - language

            LEARNING CONCEPTS EXAMPLES (for reference only):
            - Precent, Past, Future perfect continuous tense
            - Precent, Past, Future continuous tense
            - Precent, Past, Future perfect tense
            - Precent, Past, Future simple tense
            - Subject-verb agreement
            - Articles

            WORKFLOW (STRICT):
            1. Compare original and corrected text.
            2. Identify ONLY the changes.
            3. Each DISTINCT grammar change = ONE learning concept.
            4. Ignore spelling-only corrections.
            5. Use classroom-friendly grammar terminology.

            Forbidden vague labels:
            - Auxiliary verbs
            - Grammar usage
            - Verb errors

            Return JSON ONLY:
        """ + """
            {
                "learningConcepts": [
                    "<Human readable concept>"
                ]
            }
        """

        response = call_openai_with_retry(
            lambda: client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": CONCEPT_EXTRACTOR_PROMPT},
                    {
                        "role": "user",
                        "content": json.dumps({
                            "originalText": original_text,
                            "correctedText": corrected_text
                        })
                    }
                ],
                temperature=0.1  # VERY LOW for stability
            )
        )

        parsed = json.loads(response.choices[0].message.content)

        return parsed.get("learningConcepts", [])
