# Mood Machine learning walkthrough

This is a terminal lab. It has no Streamlit browser screen or email prompt.

## 1. Run the rule model

In PowerShell:

```powershell
cd "C:\Users\mitch\OneDrive\Documents\ChatGPT\School\MoodMachine"
.\.venv\Scripts\python.exe main.py
```

Read the printed predictions, true labels, and token evidence. Then type:

- I am not happy about this
- This is not bad.
- This is not only good but amazing.
- I love getting stuck in traffic.

The first two negation examples should be negative and positive respectively.
The not-only example should be mixed (a documented mistake), and the intended
sarcastic traffic example should be positive (another documented mistake).
Type quit or press Enter on a blank line to exit.

## 2. Compare before and after negation

```powershell
.\.venv\Scripts\python.exe main.py --batch --stress --baseline
.\.venv\Scripts\python.exe main.py --batch --stress
```

Trace not bad: bad is -1 without the change, but +1 after the negator reverses it.
Trace not only good but amazing: good is incorrectly reversed, while amazing stays
positive. Both signs cause mixed. This explains why a focused improvement can
help some examples and introduce a new failure.

## 3. Try the machine-learning model

```powershell
.\.venv\Scripts\python.exe ml_experiments.py
```

The script prints training accuracy separately from stress accuracy, then allows
interactive posts and shows recognized vocabulary words. Try the same sentences.
A correct answer does not prove the model understood the intended meaning.

## 4. Reproduce the comparison and tests

```powershell
.\.venv\Scripts\python.exe run_experiments.py
.\.venv\Scripts\python.exe -m pytest -q
```

Read evaluation_report.md and model_card.md. Explain why 14/14 on training posts
does not imply reliable unseen predictions, and why the 6-positive/2-negative
stress mix makes accuracy alone misleading.

## 5. Submit

Review the model card and docs/check-in-draft.md. The draft only attributes
automated runs to Codex; change it to describe your own runs only after doing
them. The student has already approved all 16 new labels and chose to document
the not-only failure rather than patch it.

Submit the personal Mood Machine repository, not PawPal+ or Music Recommender.
Complete the Week-5 check-in after the CodePath lab submission.
