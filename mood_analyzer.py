"""Inspectable keyword sentiment rules with a switchable negation improvement."""
import re

from dataset import NEGATIVE_WORDS, POSITIVE_WORDS


class MoodAnalyzer:
    """Classify expressed sentiment, not a person's actual emotional state."""

    NEGATORS = {"not", "never", "no", "isn't", "aren't", "wasn't", "don't",
                "doesn't", "didn't", "can't", "cannot", "won't"}
    BOUNDARIES = {".", "!", "?", ",", ";", ":", "but", "however", "yet"}
    TOKEN_PATTERN = re.compile(r"[:;]-?[)(]|[^\W\d_]+(?:'[^\W\d_]+)?|[.!?,;:]|[^\w\s]")

    def __init__(self, positive_words=None, negative_words=None, handle_negation=True):
        """Use custom vocabularies when supplied and optionally invert negated signals."""
        self.positive_words = {w.casefold() for w in (
            POSITIVE_WORDS if positive_words is None else positive_words)}
        self.negative_words = {w.casefold() for w in (
            NEGATIVE_WORDS if negative_words is None else negative_words)}
        if self.positive_words & self.negative_words:
            raise ValueError("A signal cannot be in both sentiment word lists.")
        self.handle_negation = handle_negation

    def preprocess(self, text: str) -> list[str]:
        """Normalize case/apostrophes and separate words, punctuation, and emoji."""
        if not isinstance(text, str):
            raise ValueError("Text must be a string.")
        return self.TOKEN_PATTERN.findall(text.casefold().replace("’", "'"))

    def analyze(self, text: str) -> dict:
        """Return the exact tokens, matches, contributions, score, and prediction."""
        tokens = self.preprocess(text)
        matches, ignored = [], []
        remaining = 0
        for token in tokens:
            if token in self.BOUNDARIES:
                remaining = 0
                continue
            if self.handle_negation and token in self.NEGATORS:
                remaining = 0 if remaining else 3
                continue
            base = 1 if token in self.positive_words else -1 if token in self.negative_words else 0
            if base:
                negated = self.handle_negation and remaining > 0
                matches.append({"token": token, "base": base, "negated": negated,
                                "contribution": -base if negated else base})
                # Negate one sentiment signal, rather than the entire sentence.
                remaining = 0
            else:
                ignored.append(token)
                if token.isalpha() or "'" in token:
                    remaining = max(0, remaining - 1)
        contributions = [match["contribution"] for match in matches]
        score = sum(contributions)
        if any(value > 0 for value in contributions) and any(value < 0 for value in contributions):
            label = "mixed"
        else:
            label = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        return {"tokens": tokens, "matches": matches, "ignored": ignored,
                "score": score, "label": label}

    def score_text(self, text: str) -> int:
        """Sum the same contributions used by the explanation and prediction."""
        return self.analyze(text)["score"]

    def predict_label(self, text: str) -> str:
        """Distinguish mixed signals from neutral text with no recognized signals."""
        return self.analyze(text)["label"]

    def explain(self, text: str) -> str:
        """Expose tokens and signed contributions without inventing semantic reasoning."""
        result = self.analyze(text)
        signals = [f"{m['token']}:{m['contribution']:+d}"
                   + (" (negated)" if m["negated"] else "") for m in result["matches"]]
        return (f"tokens={result['tokens']}; matches={signals}; ignored={result['ignored']}; "
                f"score={result['score']}; label={result['label']}")
