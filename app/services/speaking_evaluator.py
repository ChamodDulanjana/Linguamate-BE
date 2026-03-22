import json
from app.core.openai_client import client
from app.core.openai_retry import call_openai_with_retry


class SpeakingEvaluator:
    def evaluate(self, target: str, spoken: str, language: str) -> dict:

        system_prompt = f"""
            You are LinguaMate Speaking Evaluator.

            Detected language: {language}

            TASK:
            Evaluate how closely the learner's spoken sentence matches the target sentence.

            INPUT:
            - targetSentence
            - spokenText

            RULES:
            - Give pronunciation + grammar accuracy score between 0 and 1.
            - Consider:
                pronunciation approximation,
                missing words,
                tense errors,
                word order.

            - Be strict but encouraging.
            - Provide SHORT supportive feedback like "Grate work" or "Keep it up".
            - Feedback must be less than 6 words.

            OUTPUT JSON ONLY:
        """ + """

            {
                "score": 0.0,
                "isCorrect": true/false,
                "feedback": "short feedback for learner"
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
                            "targetSentence": target,
                            "spokenText": spoken
                        })
                    }
                ],
                temperature=0.1
            )
        )

        parsed = json.loads(response.choices[0].message.content)

        return parsed
