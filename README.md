# The Mood Machine — AI110 Module 3 Tinker / Week-5 Lab

An educational sentiment classifier comparing explicit rules with a small
bag-of-words machine-learning model. It labels short posts as positive, negative,
neutral, or mixed, and shows evidence for the rule predictions.

## Setup and run (Windows PowerShell)

Use Python 3.11 or later; this project was verified with Python 3.14.2.

```powershell
cd "C:\Users\mitch\OneDrive\Documents\ChatGPT\School\MoodMachine"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

On this computer the project environment is already installed, so run the last
command. main.py prints development results and then accepts typed posts.
Press Enter on a blank line or type quit to exit. It is a terminal program;
there is no browser interface or email prompt.

If python opens the Microsoft Store, use py or an installed Python executable
for environment creation. On macOS/Linux use .venv/bin/python in place of the
Windows executable path.

### Batch evaluation, ML comparison, and tests

```powershell
.\.venv\Scripts\python.exe main.py --batch --stress
.\.venv\Scripts\python.exe main.py --batch --stress --baseline
.\.venv\Scripts\python.exe ml_experiments.py --batch
.\.venv\Scripts\python.exe run_experiments.py
.\.venv\Scripts\python.exe -m pytest -q
```

Omit --batch from ml_experiments.py to try your own posts interactively.
run_experiments.py writes results.json and evaluation_report.md relative to
the script's folder. The JSON is generated locally and excluded from Git;
the readable evaluation report is included in the repository.
The rules need only Python; the ML comparison needs
scikit-learn. requirements.txt pins the two direct dependencies used here.

## Five lab parts and evidence

| Part | Implementation and evidence |
| --- | --- |
| Build the dataset | dataset.py: original 6 plus 8 additions; the student accepted all 8 proposed labels; lengths and label values are validated |
| Engineer the rules | mood_analyzer.py: tokenization, scores, mixed-signal detection, emojis, inspectable matches, and switchable negation |
| Stress-test and improve | 8 separately reviewed stress posts; same vocabulary/rules with negation off/on isolates the focused change |
| Evaluate and compare | main.py, ml_experiments.py, run_experiments.py; per-post predictions, data-growth and label-sensitivity experiments |
| Model card | model_card.md documents data, actual results, regressions, limitations, language coverage, and AI assistance |

## Actual results

| Variant | Development (14) | Diagnostic stress set (8) |
| --- | --- | --- |
| Keyword baseline | 9/14 (64.3%) | 2/8 (25.0%) |
| Negation improvement | 11/14 (78.6%) | 2/8 (25.0%) |
| ML trained on 6 starter posts | 10/14 (71.4%) | 2/8 (25.0%) |
| ML trained on expanded 14 | 14/14 (100%) | 4/8 (50.0%) |

The expanded ML development score is training accuracy. The rules were designed
using the development examples too. Neither score demonstrates unseen reliability.
The separate stress set never enters ML training, but is a small, deliberately
selected diagnostic set. Six labels are positive: always predicting positive
scores 75%, exceeding both models here. No neutral/mixed stress cases are present.

Negation fixes not happy and not good on development posts. On stress posts it
fixes not bad but introduces an error on not only good but amazing, leaving
stress accuracy unchanged. This is a documented tradeoff, not a hidden failure.

### Prediction evidence example

```text
This is not bad.
Expected: positive; baseline: negative; improved: positive.
Tokens: ['this', 'is', 'not', 'bad', '.']
Matches: [{'token': 'bad', 'base': -1, 'negated': True, 'contribution': 1}]
Ignored: ['this', 'is']
Score: 1
```

The full report also explains sarcasm, slang, language variation, and the new
negation regression. The [evaluation report](evaluation_report.md) includes
per-example predictions, tokens, and matched contributions.

### Software verification

```text
.....................                                                    [100%]
21 passed in 2.76s
```

Tests validate input alignment, signal behavior, explanation consistency,
negation scope, empty input, invalid data, repeatability, and exclusion of
stress-only vocabulary from training. Some sentiment predictions deliberately
remain wrong and are documented; passing software tests does not mean 100%
classification accuracy.

## Documentation and submission

- [Model card](model_card.md): purpose, rules, data, evaluation, limitations, bias concerns.
- [Evaluation report](evaluation_report.md): measured results and prediction evidence.

AI assistance and student decisions are documented in the model card.
Submit this repository URL to CodePath, then complete the Week-5 check-in in Canvas.

This is the Mood Machine lab, separate from PawPal+ and Music Recommender.
The project uses synthetic classroom posts; it does not infer actual mental health.
