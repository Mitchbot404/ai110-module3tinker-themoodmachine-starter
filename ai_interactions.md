# AI Assistance and Student Decisions

## Actual task and tool

The student supplied the five Mood Machine lab parts after distinguishing this
lab from PawPal+ and the Music Recommender project. Codex inspected and cloned
CodePath's starter, prepared the local environment, implemented and ran the
rules/ML comparison, and drafted documentation. Work used this continuing chat,
not separate phase chats or multiple models.

## Dataset proposals and human review

Codex proposed eight new development posts with labels, covering sarcasm, slang,
emoji, mixed sentiment, negation, neutral content, and a regional expression.
The student replied: **"I agree with all 8 labels."**

Codex then proposed eight separate stress posts, including not bad, not only,
sarcasm, formal and regional positive wording, ain't happy, and affirmative happy.
The student again replied: **"I agree with these 8 labels."**

The six original labels came from the course starter. No group annotation or
independent agreement statistic is claimed. Ambiguous/sarcastic labels represent
the reviewed intended reading, not universal ground truth.

## Focused change and evaluation

The completed keyword baseline and improved model share tokenization, word
lists, emoji signals, and mixed-label logic. The controlled difference is
negation handling. The baseline has 9/14 development predictions correct; the
improved model has 11/14. Both score 2/8 on the selected stress set because a
gain on not bad is offset by a regression on not only good but amazing.

The student was shown the regression and asked whether to patch it or retain it
as a documented limitation. They chose:
**"Document the limitation and keep the focused change."**
The model card records that choice. No successful fix for this construction is
claimed.

The expanded ML model fits all 14 training examples but scores only 4/8 on stress
posts. Codex flagged this distinction and the constant-positive 6/8 reference
on this imbalanced stress set. Training on six versus fourteen posts and flipping
one sarcasm label are separately recorded sensitivity experiments. The altered
label is not used in the shipped dataset.

## AI review and concerns raised

Codex identified narrow vocabulary and negation coverage, the sarcasm/label
ambiguity, a newly introduced regression, and the danger of presenting training
accuracy as unseen performance. It also noted that dialect examples do not
establish group-level fairness. Those observations are checked against tokens,
matched contributions, predicted labels, and the recorded dataset counts.

The model card's overt-bias discussion uses specific language-coverage examples;
its covert-compliance discussion records the assistant's actual cautions rather
than inventing a conversation where every suggestion was accepted uncritically.

## Work completed and evidence

Files: dataset.py, mood_analyzer.py, main.py, ml_experiments.py,
run_experiments.py, tests/test_mood_machine.py, model_card.md, README.md,
requirements.txt, pytest.ini, .gitignore, evaluation_report.md, results.json,
rule_output.txt, ml_output.txt, and docs/.

Codex installed dependencies, ran the rule and ML batch CLIs, generated
per-example reports, and ran pytest: **21 passed in 2.76s**.
The student reviewed labels, created their personal fork, and chose to document
the negation regression. No student-run execution, manual code edits, or
independent model training is claimed yet.

## Remaining student work

Run the walkthrough to inspect the evidence yourself, review the model card and
check-in draft, submit the personal repository URL to CodePath, then complete
the Week-5 Canvas check-in. Future first-person accounts should distinguish the
student's own checks from the commands Codex ran.
