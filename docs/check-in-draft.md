# Week-5 Canvas check-in draft

Review this draft against your experience before submitting. It reports actual
student label approvals and the documented choice to retain a limitation.
Automated runs were performed by Codex; no independent student run is claimed.

## 1. Most important concept or skill (150–400 words)

The most important concept I strengthened was that an AI system's accuracy
depends on the data and rules used, and that one score can hide important
failures. In The Mood Machine, I reviewed and accepted eight additional posts
and their sentiment labels, along with eight separate stress-test examples.
Some labels depended on intended context, such as reading a positive-sounding
sentence as sarcasm.

Codex implemented and ran the comparison between a keyword baseline, a negation
improvement, and a small machine-learning classifier. Negation handling improved
the development result from 9 out of 14 to 11 out of 14. However, the stress
result stayed at 2 out of 8 because fixing "not bad" also introduced an error
on "not only good but amazing." I chose to document that limitation and keep
the focused change instead of adding another exception immediately.

The machine-learning model classified all 14 training examples correctly but
only 4 of the 8 separate stress examples. That difference showed why training
accuracy is not evidence of reliable performance on new text. The stress set
was also imbalanced, so accuracy alone was a poor summary.

This matters when building software because I need to inspect individual
predictions, explain errors, and document limitations before trusting a model.
AI assistance can speed up implementation, but human review is still needed
for labels and decisions about which failures to fix.

## 2. GitHub project URL

https://github.com/Mitchbot404/ai110-module3tinker-themoodmachine-starter

## 3. Completion status

Select FULLY COMPLETED after submitting the Mood Machine exercise to CodePath.
A GitHub upload alone does not confirm that the course submission was completed.

## 4. Usefulness

Your earlier screenshot selected SOMEWHAT USEFUL. Retain it only if that matches
your experience with this lab; choose the option that now fits best.

## 5. Difficulty

Your earlier screenshot selected MANAGEABLE. Retain it only if it accurately
describes this lab.

## 6. Feedback for improvement (optional draft)

Add one worked example that compares the keyword model, an improved rule, and
the ML prediction for the same sentence. Showing tokens, scores, and a case
where an improvement creates a new error would make the tradeoffs easier to
follow. I would also label training accuracy and separate-test accuracy clearly
in the example output so students can see why a high training score does not
necessarily mean the system is reliable.
