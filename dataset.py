"""
Shared data for the Mood Machine lab.

This file defines:
  - POSITIVE_WORDS: starter list of positive words
  - NEGATIVE_WORDS: starter list of negative words
  - SAMPLE_POSTS: short example posts for evaluation and training
  - TRUE_LABELS: human labels for each post in SAMPLE_POSTS
"""

# ---------------------------------------------------------------------
# Starter word lists
# ---------------------------------------------------------------------

POSITIVE_WORDS = [
    "happy",
    "great",
    "good",
    "love",
    "excited",
    "awesome",
    "fun",
    "chill",
    "relaxed",
    "amazing",
    "hopeful",
    "proud",
    "😄",
]

NEGATIVE_WORDS = [
    "sad",
    "bad",
    "terrible",
    "awful",
    "angry",
    "upset",
    "tired",
    "stressed",
    "hate",
    "boring",
    "😞",
]

# ---------------------------------------------------------------------
# Starter labeled dataset
# ---------------------------------------------------------------------

# Short example posts written as if they were social media updates or messages.
SAMPLE_POSTS = [
    "I love this class so much",
    "Today was a terrible day",
    "Feeling tired but kind of hopeful",
    "This is fine",
    "So excited for the weekend",
    "I am not happy about this",
]

# Human labels for each post above.
# Allowed labels in the starter:
#   - "positive"
#   - "negative"
#   - "neutral"
#   - "mixed"
TRUE_LABELS = [
    "positive",  # "I love this class so much"
    "negative",  # "Today was a terrible day"
    "mixed",     # "Feeling tired but kind of hopeful"
    "neutral",   # "This is fine"
    "positive",  # "So excited for the weekend"
    "negative",  # "I am not happy about this"
]

# Original lab guidance (the reviewed additions are implemented below).
#
# Requirements:
#   - For every new post you add to SAMPLE_POSTS, you must add one
#     matching label to TRUE_LABELS.
#   - SAMPLE_POSTS and TRUE_LABELS must always have the same length.
#   - Include a variety of language styles, such as:
#       * Slang ("lowkey", "highkey", "no cap")
#       * Emojis (":)", ":(", "🥲", "😂", "💀")
#       * Sarcasm ("I absolutely love getting stuck in traffic")
#       * Ambiguous or mixed feelings
#
# Tips:
#   - Try to create some examples that are hard to label even for you.
#   - Make a note of any examples that you and a friend might disagree on.
#     Those "edge cases" are interesting to inspect for both the rule based
#     and ML models.
#
# Example of how you might extend the lists:
#
# SAMPLE_POSTS.append("Lowkey stressed but kind of proud of myself")
# TRUE_LABELS.append("mixed")
#
# Remember to keep them aligned:
#   len(SAMPLE_POSTS) == len(TRUE_LABELS)

# Eight proposed examples reviewed and accepted by the student in chat.
ADDED_POSTS = [
    "Great, another two-hour delay.",
    "That set was sick, no cap.",
    "Got my tickets 😄",
    "Missed the train 😞",
    "I'm tired but proud of what I finished.",
    "This update is not good.",
    "The meeting starts at noon.",
    "I'm well chuffed with the result.",
]
ADDED_LABELS = ["negative", "positive", "positive", "negative",
                "mixed", "negative", "neutral", "positive"]
STARTER_POSTS = SAMPLE_POSTS.copy()
STARTER_LABELS = TRUE_LABELS.copy()
SAMPLE_POSTS.extend(ADDED_POSTS)
TRUE_LABELS.extend(ADDED_LABELS)

# Separately reviewed diagnostic examples; NEVER supplied to model.fit().
# Small, deliberately selected challenge set, not a representative benchmark.
STRESS_POSTS = [
    "This is not bad.",
    "This is not only good but amazing.",
    "I love getting stuck in traffic.",
    "That set was excellent.",
    "I'm very pleased with the result.",
    "I'm well chuffed with this.",
    "I ain't happy about this.",
    "I am happy about this.",
]
STRESS_LABELS = ["positive", "positive", "negative", "positive",
                 "positive", "positive", "negative", "positive"]
LABELS = {"positive", "negative", "neutral", "mixed"}


def validate_dataset(posts, labels):
    """Reject missing labels before zip() could silently drop examples."""
    if len(posts) != len(labels):
        raise ValueError("Every post must have exactly one matching label.")
    if any(not isinstance(post, str) or not post.strip() for post in posts):
        raise ValueError("Posts must be nonempty strings.")
    if any(label not in LABELS for label in labels):
        raise ValueError("Labels must be positive, negative, neutral, or mixed.")


validate_dataset(SAMPLE_POSTS, TRUE_LABELS)
validate_dataset(STRESS_POSTS, STRESS_LABELS)
