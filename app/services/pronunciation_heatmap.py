import difflib


class PronunciationHeatmap:
    def generate(self, target: str, spoken: str):

        target_words = target.lower().split()
        spoken_words = spoken.lower().split()

        matcher = difflib.SequenceMatcher(
            None,
            target_words,
            spoken_words
        )

        heatmap = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == "equal":
                for word in target_words[i1:i2]:
                    heatmap.append({
                        "word": word,
                        "status": "correct"
                    })

            elif tag == "replace":
                for word in target_words[i1:i2]:
                    heatmap.append({
                        "word": word,
                        "status": "incorrect"
                    })

            elif tag == "delete":
                for word in target_words[i1:i2]:
                    heatmap.append({
                        "word": word,
                        "status": "missing"
                    })

        return heatmap
