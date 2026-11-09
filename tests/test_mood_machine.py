"""Verify model plumbing and inspectable behavior; model errors are not test failures."""
import pytest

from dataset import SAMPLE_POSTS, TRUE_LABELS, STRESS_POSTS, STRESS_LABELS, validate_dataset
from mood_analyzer import MoodAnalyzer
from main import evaluate_rule_based
from ml_experiments import train_ml_model, predict_single_text


@pytest.mark.parametrize("text,label", [
    ("I love this!", "positive"), ("This is terrible.", "negative"),
    ("The meeting starts at noon.", "neutral"), ("I'm tired but proud.", "mixed"),
    ("I am not happy about this.", "negative"), ("This is not bad.", "positive"),
    ("I'm not very happy.", "negative"), ("This isn't good.", "negative"),
    ("Happy 😄", "positive"), ("Missed it 😞", "negative"),
])
def test_obvious_signals_and_negation(text, label):
    assert MoodAnalyzer().predict_label(text) == label


def test_alignment_and_reviewed_dataset_sizes():
    assert len(SAMPLE_POSTS) == len(TRUE_LABELS) == 14
    assert len(STRESS_POSTS) == len(STRESS_LABELS) == 8
    assert not set(SAMPLE_POSTS) & set(STRESS_POSTS)


def test_dataset_validation_prevents_silent_zip_truncation():
    with pytest.raises(ValueError, match="exactly one"):
        evaluate_rule_based(["happy", "sad"], ["positive"])
    with pytest.raises(ValueError):
        validate_dataset([""], ["neutral"])
    with pytest.raises(ValueError):
        validate_dataset(["hello"], ["unknown"])


def test_baseline_and_improvement_isolate_negation():
    assert MoodAnalyzer(handle_negation=False).predict_label("not happy") == "positive"
    assert MoodAnalyzer(handle_negation=True).predict_label("not happy") == "negative"


def test_mixed_is_not_the_same_as_no_signals():
    analyzer = MoodAnalyzer()
    assert analyzer.score_text("happy sad") == analyzer.score_text("table chair") == 0
    assert analyzer.predict_label("happy sad") == "mixed"
    assert analyzer.predict_label("table chair") == "neutral"


def test_explanation_agrees_with_score_and_prediction():
    analyzer = MoodAnalyzer()
    result = analyzer.analyze("Not happy, but excited!")
    assert sum(match["contribution"] for match in result["matches"]) == analyzer.score_text("Not happy, but excited!")
    assert result["label"] == analyzer.predict_label("Not happy, but excited!")
    assert result["matches"][0]["negated"]
    assert not result["matches"][1]["negated"]
    assert "negated" in analyzer.explain("Not happy, but excited!")


def test_window_does_not_negate_across_punctuation_or_contrast():
    analyzer = MoodAnalyzer()
    assert analyzer.predict_label("not. happy") == "positive"
    assert analyzer.predict_label("not, happy") == "positive"
    assert analyzer.predict_label("not sure but happy") == "positive"
    assert analyzer.predict_label("not one two three happy") == "positive"


def test_custom_empty_vocabulary_is_respected():
    assert MoodAnalyzer([], []).predict_label("happy sad") == "neutral"
    with pytest.raises(ValueError):
        MoodAnalyzer(["same"], ["same"])


def test_invalid_text_and_empty_evaluation():
    with pytest.raises(ValueError):
        MoodAnalyzer().preprocess(None)
    assert evaluate_rule_based([], []) == 0


def test_ml_vocabulary_excludes_stress_only_words():
    vectorizer, model = train_ml_model(SAMPLE_POSTS, TRUE_LABELS)
    assert "excellent" not in vectorizer.vocabulary_
    assert predict_single_text("hello", vectorizer, model) in set(TRUE_LABELS)


def test_ml_invalid_training_data():
    with pytest.raises(ValueError):
        train_ml_model([], [])
    with pytest.raises(ValueError):
        train_ml_model(["happy"], ["positive"])
    with pytest.raises(ValueError):
        train_ml_model(["happy"], [])


def test_ml_is_repeatable_without_changing_labels():
    before = TRUE_LABELS.copy()
    first_vectorizer, first_model = train_ml_model(SAMPLE_POSTS, TRUE_LABELS)
    second_vectorizer, second_model = train_ml_model(SAMPLE_POSTS, TRUE_LABELS)
    first = first_model.predict(first_vectorizer.transform(STRESS_POSTS))
    second = second_model.predict(second_vectorizer.transform(STRESS_POSTS))
    assert list(first) == list(second)
    assert TRUE_LABELS == before
