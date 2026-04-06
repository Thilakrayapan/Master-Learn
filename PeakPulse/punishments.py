"""PeakPulse — Funny Punishment Engine 😂"""

import random

# ─── Punishment Catalog ─────────────────────────────────────────────
PUNISHMENTS = {
    "easy": [
        "🏃 Do 10 jumping jacks right now!",
        "📵 No phone for 30 minutes!",
        "💧 Drink a full glass of water and reflect on your choices.",
        "✍️ Write down 3 things you're grateful for.",
        "🧘 Do 2 minutes of deep breathing.",
        "🚶 Take a 5-minute walk — no phone allowed!",
        "😤 Hold a plank for 30 seconds. No excuses.",
        "📝 Write a 1-paragraph apology letter to your future self.",
    ],
    "medium": [
        "📵 No Instagram for 2 hours. Seriously.",
        "✍️ Write 'I will finish my tasks on time' 50 times.",
        "🧹 Clean your desk right now — spot check incoming!",
        "🥗 No junk food for the rest of the day.",
        "📖 Read 10 pages of a book before your next break.",
        "🚫 No YouTube for 3 hours. Yes, really.",
        "🏋️ Do 20 squats and 20 push-ups. NOW.",
        "🕐 Wake up 30 minutes earlier tomorrow. Set the alarm now!",
    ],
    "hard": [
        "📚 Double your study time tomorrow. No negotiation.",
        "🥶 Cold shower time! 2 minutes minimum!",
        "📵 Full digital detox for 4 hours. Hand over your phone.",
        "🏃 Run 1 kilometer before you can use your phone again.",
        "✍️ Write a 500-word essay on why procrastination is bad.",
        "🧹 Deep clean your entire room before any fun activities.",
        "🚫 No social media for 24 hours. Delete the apps if you must.",
        "😱 Tell a friend about your failure and ask them to hold you accountable.",
    ],
}


def get_punishment(missed_count: int) -> str:
    """Return a random punishment based on how many tasks have been missed.

    Args:
        missed_count: Total number of missed tasks (determines severity).

    Returns:
        A funny punishment message string.
    """
    if missed_count <= 2:
        level = "easy"
    elif missed_count <= 5:
        level = "medium"
    else:
        level = "hard"

    return random.choice(PUNISHMENTS[level])


def get_all_punishments() -> dict:
    """Return the full punishment catalog."""
    return PUNISHMENTS


def get_level_for_count(missed_count: int) -> str:
    """Return the severity level name for a given missed count."""
    if missed_count <= 2:
        return "easy"
    elif missed_count <= 5:
        return "medium"
    return "hard"
