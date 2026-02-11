import json
from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry
from app.core.language_detector import language_detector


class GrammarCorrector:
    def respond(self, user_input: str) -> dict:
        if not user_input.strip():
            return {
                "response": "Could you please type something so I can help you? 😊",
                "hasActionButtons": False,
                "learningConcept": None,
                "category": None
            }

        lang_info = language_detector.detect_language(user_input)

        system_prompt = f"""
            You are LinguaMate, a friendly AI language tutor.

            Detected language: {lang_info.language}
            Language confidence: {lang_info.confidence}

            IMPORTANT:
            - Always respond in the detected language unless the user switches language.
            - Apply grammar rules ONLY for the detected language.
            - Do NOT assume English unless language = "en".

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
            - If there are any spelling mistakes, highlight them and explain the correction in the `response` text itself so the user learns immediately but do not put it in the `learningConcepts`.

            After responding, decide:
            - hasActionButtons = true → if correction was needed
            - hasActionButtons = false → otherwise

            Return ONLY valid JSON:
        """ + """

            {
                "response": "<natural tutor reply>",
                "hasActionButtons": true/false,
                "learningConcepts": [
                    "<Human readable concept name>"
                ]
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
                temperature=0.3
            )
        )


        content = response.choices[0].message.content

        try:
            parsed = json.loads(content)
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

        if "Spelling" in output["learningConcepts"]:
            output["learningConcepts"].remove("Spelling")

        return output
