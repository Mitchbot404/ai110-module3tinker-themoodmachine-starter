"""Rule evaluation and interactive demo: python main.py [--batch] [--stress]."""
import argparse

from dataset import SAMPLE_POSTS, TRUE_LABELS, STRESS_POSTS, STRESS_LABELS, validate_dataset
from mood_analyzer import MoodAnalyzer


def evaluate_rule_based(posts, labels, analyzer=None, title="Rule evaluation"):
    """Print each label with inspectable evidence, after checking label alignment."""
    validate_dataset(posts, labels)
    analyzer = MoodAnalyzer() if analyzer is None else analyzer
    correct = 0
    print(f"=== {title} ===")
    for text, expected in zip(posts, labels):
        result = analyzer.analyze(text)
        correct += result["label"] == expected
        status = "OK" if result["label"] == expected else "MISMATCH"
        print(f"{status}: {text!r} -> predicted={result['label']}, true={expected}")
        print("  " + analyzer.explain(text))
    accuracy = correct / len(posts) if posts else 0.0
    print(f"Accuracy: {correct}/{len(posts)} = {accuracy:.2%}")
    return accuracy


def run_interactive_loop():
    """Inspect user text until a blank line, quit, or closed input."""
    analyzer = MoodAnalyzer()
    print("\nType a post; Enter or 'quit' exits. This predicts text sentiment, not mental health.")
    while True:
        try:
            text = input("You: ").strip()
        except EOFError:
            break
        if not text or text.casefold() == "quit":
            break
        print(analyzer.explain(text))


def main():
    """Evaluate development data and optionally the separate stress set."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="store_true", help="Evaluate and exit without asking for input.")
    parser.add_argument("--stress", action="store_true", help="Also evaluate separate challenge examples.")
    parser.add_argument("--baseline", action="store_true", help="Disable only negation handling.")
    args = parser.parse_args()
    analyzer = MoodAnalyzer(handle_negation=not args.baseline)
    evaluate_rule_based(SAMPLE_POSTS, TRUE_LABELS, analyzer,
                        "14 development posts (negation " + ("off" if args.baseline else "on") + ")")
    if args.stress:
        evaluate_rule_based(STRESS_POSTS, STRESS_LABELS, analyzer, "8 separate diagnostic stress posts")
    if not args.batch:
        run_interactive_loop()


if __name__ == "__main__":
    main()
