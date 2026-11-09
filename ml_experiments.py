"""Bag-of-words/logistic-regression comparison, retaining the provided approach."""
import argparse

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from dataset import SAMPLE_POSTS, TRUE_LABELS, STRESS_POSTS, STRESS_LABELS, validate_dataset


def train_ml_model(texts, labels):
    """Fit vocabulary and model on training posts only, never on the stress set."""
    validate_dataset(texts, labels)
    if not texts or len(set(labels)) < 2:
        raise ValueError("Training needs nonempty data and at least two sentiment classes.")
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(texts)
    model = LogisticRegression(max_iter=2000, random_state=110)
    model.fit(features, labels)
    return vectorizer, model


def evaluate_on_dataset(texts, labels, vectorizer, model, title="ML evaluation"):
    """Report accuracy with an explicit name for the dataset being measured."""
    validate_dataset(texts, labels)
    print(f"=== {title} ===")
    if not texts:
        print("No examples; accuracy reported as 0.")
        return 0.0
    predictions = model.predict(vectorizer.transform(texts))
    correct = 0
    for text, expected, predicted in zip(texts, labels, predictions):
        correct += expected == predicted
        marker = "OK" if expected == predicted else "MISMATCH"
        print(f"{marker}: {text!r} -> predicted={predicted}, true={expected}")
    accuracy = correct / len(texts)
    print(f"Accuracy: {correct}/{len(texts)} = {accuracy:.2%}")
    return accuracy


def predict_single_text(text, vectorizer, model):
    """Predict one label; out-of-vocabulary text may have no useful evidence."""
    return str(model.predict(vectorizer.transform([text]))[0])


def run_interactive_loop(vectorizer, model):
    """Accept new posts while displaying which words exist in the learned vocabulary."""
    tokenizer = vectorizer.build_analyzer()
    print("\nType a post; Enter or 'quit' exits.")
    while True:
        try:
            text = input("You: ").strip()
        except EOFError:
            break
        if not text or text.casefold() == "quit":
            break
        known = [word for word in tokenizer(text) if word in vectorizer.vocabulary_]
        print(f"ML: {predict_single_text(text, vectorizer, model)}; known words={known}")


def main():
    """Separate training accuracy from results on untrained diagnostic examples."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="store_true")
    args = parser.parse_args()
    vectorizer, model = train_ml_model(SAMPLE_POSTS, TRUE_LABELS)
    evaluate_on_dataset(SAMPLE_POSTS, TRUE_LABELS, vectorizer, model,
                        "Training accuracy (NOT unseen-data performance)")
    evaluate_on_dataset(STRESS_POSTS, STRESS_LABELS, vectorizer, model,
                        "Separate diagnostic stress set (small and intentionally difficult)")
    if not args.batch:
        run_interactive_loop(vectorizer, model)


if __name__ == "__main__":
    main()
