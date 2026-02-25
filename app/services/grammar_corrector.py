import json
from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry
from app.core.language_detector import language_detector
from app.services.concept_extractor import ConceptExtractor

concept_extractor = ConceptExtractor()

class GrammarCorrector:
    def respond(self, user_input: str) -> dict:
        if not user_input.strip():
            return {
                "response": "Could you please type something so I can help you? 😊",
                "hasActionButtons": False
            }

        lang_info = language_detector.detect_language(user_input)
        language = lang_info.language

        system_prompt = f"""
            You are LinguaMate, a friendly AI language tutor.

            Detected language: {language}

            IMPORTANT:
            - Always respond in the detected language unless the user switches language.
            - Do NOT assume English unless language = "en".

            Rules:
            - If the user greets or chats casually, respond naturally. Do NOT give grammar feedback for simple greetings.
            - If the sentence is grammatically correct, give positive feedback.
            - If the sentence has ANY language usage mistakes (grammar, spelling, awkward phrasing):
                1. Politely acknowledge the effort.
                2. PROVIDE THE CORRECTED VERSION of the specific sentence(s) in your response text inside "" and "**".

             The user may provide:
            - A single sentence
            - Multiple sentences
            - A full paragraph

            Your responsibilities:
            - Analyze the input and detect ALL language usage mistakes in ALL sentences.
            - Ensure the `response` field contains the readable correction.

            CRITICAL RULES (MUST FOLLOW):
            - Explain the correction in the `response` text itself so the user learns immediately.
            - BE PRECISE WITH GRAMMATICAL TERMINOLOGY.
            - Ensure the explanation matches the correction physically and grammatically.

            After responding, decide:
            - hasActionButtons = true → if correction was needed
            - hasActionButtons = false → otherwise

            Return ONLY valid JSON:
        """ + """

            {
                "response": "<natural tutor reply>",
                "hasActionButtons": true/false,
                "correctedText": "<fully corrected version>"
            }
        """

        response = call_openai_with_retry(
            lambda: client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.5
            )
        )

        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)

            if parsed.get("hasActionButtons"):
                learning_concepts = concept_extractor.extract(
                    user_input, 
                    parsed.get("correctedText", ""),
                    language
                )
                parsed["learningConcepts"] = learning_concepts
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}") + 1
            parsed = json.loads(content[start:end])

        output = {
            "response": parsed.get("response", ""),
            "language": lang_info.language,
            "hasActionButtons": parsed.get("hasActionButtons", False),
            "learningConcepts": parsed.get("learningConcepts", [])
        }

        return output
