# Model Card: Mood Machine

## 1. Model Overview

**Versions:** An inspectable keyword baseline, the same rules with a focused
negation improvement, and the starter's bag-of-words/logistic-regression model.
The untouched starter had unimplemented scoring methods; reported baseline
numbers come from a completed keyword model, not an executable original starter.

**Purpose:** Classroom exploration of expressed sentiment in short posts:
positive, negative, neutral, or mixed. These labels describe an interpretation of
text, not a person's actual emotions, intentions, or mental health. This is not
a production moderation, diagnosis, or decision-making system.

The rule model looks up selected words and two emojis. The ML model learns word
associations from reviewed examples. Neither understands meaning as a person does.

## 2. Data and Labeling

There are **14 development/training posts**: six starter posts and eight additions
proposed by Codex and explicitly reviewed and accepted by the student in chat.
The student also accepted eight separate diagnostic stress posts and their
intended labels before evaluation. Those eight posts are never used for fitting
the ML vocabulary or classifier.

Development label counts: positive 5, negative 5, neutral 2, mixed 2.
Stress label counts: positive 6, negative 2; no neutral or mixed stress cases.
Both sets are synthetic classroom examples, not collected personal messages.
dataset.validate_dataset() checks matching lengths, valid labels, and nonempty
posts before evaluation, avoiding silent truncation by zip().

The eight additions cover intended sarcasm, slang, two emojis, mixed emotion,
negation, a neutral announcement, and the British expression 'well chuffed'.
For example, 'Great, another two-hour delay.' is labeled negative with sarcastic
intent. Without context, a reader could interpret it differently. 'This is fine'
retains the starter's neutral label but could also be ironic. 'Sick' can mean
unwell or excellent; the approved music-set example intends praise.

Approval is one person's judgment about intended meaning, not a multi-rater
annotation study. The dataset is tiny, constructed, and vocabulary-limited.
The stress set was deliberately chosen to expose failures and is not a
representative random sample of real posts.

## 3. How the Rule Model Works

Preprocessing lowercases text, normalizes curly apostrophes, and separates words,
punctuation, and emoji. The positive/negative vocabularies retain the starter
words and add hopeful, proud, 😄, and 😞. Both rule variants use exactly these
same signals, tokenization, and label rules, isolating negation in the comparison.

Each matched positive signal contributes +1 and each negative signal -1. Repeated
signals count repeatedly. The model returns mixed when both effective positive
and negative contributions are present, even if they do not balance. Otherwise,
a positive total means positive, a negative total means negative, and no signal
means neutral. Mixed text therefore differs from neutral text despite both
sometimes having a total score of zero.

The focused improvement recognizes explicit negators such as not, never,
isn't, and don't. It reverses the next sentiment signal within three word
positions. Punctuation and contrast words such as but reset the scope.
The window is a hand-written approximation, not a grammatical parser.
It does not recognize ain't or reliably handle coordination and constructions
such as 'not only'. Two consecutive negators can cancel within its local window,
but this is not general double-negation understanding.

analyze() exposes tokens, matched signals, negation flags, contributions, ignored
tokens, the score, and the predicted label. score_text(), predict_label(), and
explain() all use that same analysis so explanations match predictions.

## 4. How the ML Model Works

CountVectorizer converts posts into bags of word counts, and LogisticRegression
learns class associations (max_iter=2000, random_state=110). The supplied ML
approach is retained. Its default tokenization drops emoji and one-character
tokens, and word counts do not capture order or sarcasm. Unknown words contribute
no learned feature.

The shipped ML demo trains on the 14 approved development posts. Separate
experiments train on the original six, and deliberately change ONE training
label to examine sensitivity. Neither experiment changes the accepted dataset.

Adding eight examples changes the fixed stress-set result from 2/8 to 4/8.
That is an observed difference for this run, not evidence that adding arbitrary
data always helps. Flipping the delay post's training label from negative to
positive changes its fitted prediction to positive. Against the unchanged
accepted labels, development accuracy drops from 14/14 to 13/14; stress accuracy
stays at 4/8. This demonstrates sensitivity to a label without implying all
predictions must change.

## 5. Evaluation

Reproduce with python run_experiments.py. Full per-post predictions and rule
diagnostics are in evaluation_report.md. The script also generates results.json
locally; this machine-readable duplicate is excluded from Git. Recorded environment:
Python 3.14.2, scikit-learn 1.9.1; evaluation date November 8, 2026.

| Model | Development posts | Separate stress posts |
| --- | --- | --- |
| Keyword baseline, negation disabled | 9/14 (64.3%) | 2/8 (25.0%) |
| Negation improvement | 11/14 (78.6%) | 2/8 (25.0%) |
| ML trained on original 6 | 10/14 (71.4%) | 2/8 (25.0%) |
| ML trained on expanded 14 | 14/14 (100.0%) | 4/8 (50.0%) |
| ML with one deliberately changed training label | 13/14 (92.9%) | 4/8 (50.0%) |

The seed6 development result combines its six training examples with eight new
examples. The expanded ML development result is **training accuracy**. The rules
were also developed with this set, so their development accuracy is not an
unbiased estimate of unseen performance.

The stress set contains six positive and two negative examples. A constant-positive
reference gets 6/8 (75%), exceeding both measured models here. Neither model
should be presented as reliable based on these results. One stress error changes
accuracy by 12.5 percentage points, and neutral/mixed stress performance was not
measured.

### Correct behavior and focused improvement

- 'I am not happy about this': keyword baseline positive; improved negative,
  matching the starter label.
- 'This update is not good.': baseline positive; improved negative.
- 'This is not bad.': baseline negative; improved positive. The bad contribution
  changes from -1 to +1 when not is recognized.
- 'Feeling tired but kind of hopeful': improved mixed from tired=-1, hopeful=+1.
- 'Got my tickets 😄': improved positive from the recognized emoji.

### Errors and decisions

- 'This is not only good but amazing.': baseline positive, improved mixed,
  expected positive. The new rule wrongly negates good, then counts amazing
  positively. It introduces a regression even as other negation cases improve.
  A future narrow 'not only' exception is plausible, but the observed defect is
  retained and documented for this lab rather than silently tuning away the
  diagnostic failure. After seeing this tradeoff, the student explicitly chose
  to document the limitation and keep the focused change.
- 'I love getting stuck in traffic.': both improved rules and expanded ML predict
  positive, expected negative under the approved sarcastic interpretation.
  The rules count love=+1 and ignore getting/stuck/traffic; ML learned love in
  positive contexts. Sarcasm is documented as a contextual limitation.
- 'That set was sick, no cap.': rules predict neutral because sick is unknown.
  Adding sick globally as positive would create problems for illness statements,
  so it is not added without contextual tests.
- 'I'm well chuffed with this.': rules neutral, expanded ML positive, expected
  positive. The rules have no chuffed signal.
- 'I ain't happy about this.': rules positive, ML negative, expected negative.
  The rules ignore ain't and count happy. Expanding negation is a correctable
  coverage gap, left visible in the current evaluation.
- 'I am happy about this.': rules positive, expanded ML negative, expected positive.
  Happy occurs in the negative 'not happy' training sentence and has no matching
  affirmative training example. This suggests a spurious learned association;
  the prediction alone does not establish human-like understanding of negation.

Twenty-one automated tests pass. They verify alignment, expected simple rule
behavior, consistent explanations, scope boundaries, invalid inputs, repeatable
ML predictions, and exclusion of stress-only vocabulary from training. Passing
software tests does not mean every sentiment prediction is correct.

## 6. Limitations

Neither model handles sarcasm, context, ambiguity, long posts, all emoji, all
language styles, or grammatical scope reliably. The rules treat unknown sentiment
as neutral. The ML model can still output a confident-looking class when useful
words are absent; no confidence threshold or abstention behavior is provided.

No production accuracy, demographic fairness, clinical validity, or robustness
claim follows from these synthetic examples. The stress set is separate from
fitting, but its cases were selected during development as diagnostics; it is
not an untouched final benchmark. Future rule changes need new evaluation data.

## 7. Ethical Considerations and AI Assistance

**Language coverage and the lab's overt-bias concern:** The formal negative
'I am not happy about this' is recognized, while the equivalent intent using
'ain't' is misread. Missing 'chuffed' and 'sick' also exposes narrow vocabulary
coverage. These errors can disadvantage people using informal or regional
language. A few examples show a coverage risk, not a measured claim about
demographic groups. Positive wording such as 'pleased' is also missed, so not
every failure is specific to one language community.

**The lab's covert-compliance concern:** Codex proposed data and code, but the
student explicitly accepted all new development and stress labels. The assistant
flagged that training accuracy can be misleading, that negation introduced a
new error, and that the imbalanced stress set favors an always-positive
reference. It did not treat the high training result or every suggested fix as
proof of success. Automated checks support those observations; they do not
remove the need for human review of labels and conclusions.

The assistant implemented and ran the experiments and drafted this model card.
The student reviewed proposed labels and supplied the personal fork. No separate
group discussion, independent student execution, multi-model comparison, or
personal discovery is invented. AI assistance is documented in this section.

In real use, sentiment labels could misrepresent distress or a speaker's intent.
Analyzing private messages also raises consent and privacy concerns. This
classroom model is for exploration with synthetic data, not consequential
judgments about people.

## 8. Ideas for Improvement

- Collect more varied examples with multiple annotators and record disagreements.
- Add and test a narrow 'not only' exception and broader negation coverage.
- Evaluate slang in both positive and negative contexts before adding vocabulary.
- Test formal/informal paraphrases with the same intended sentiment.
- Build a larger, class-balanced independent test set and inspect per-class errors.
- Compare richer language features while retaining readable explanations.
- Consider an unknown/uncertain outcome rather than forcing a sentiment label.

The lab's useful outcome is an inspectable improvement and an honest account of
what still fails, not a perfect score on examples used to build the system.
