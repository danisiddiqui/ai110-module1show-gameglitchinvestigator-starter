# FIX: All four functions were moved here from app.py using AI (Claude) agent mode.
# I reviewed every change; bug fixes are marked with FIX comments below.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: also reject whitespace-only input like "   " instead of calling it "not a number".
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except ValueError:
        # FIX: catch ValueError specifically instead of a bare Exception.
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: the hint messages were swapped. A guess that is too high should tell the
    # player to go LOWER. The AI suggested the swap; I verified it with pytest.
    # FIX: removed the try/except TypeError fallback that compared numbers as strings
    # ("9" > "50" is True alphabetically). app.py now always passes an int secret.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: was 100 - 10 * (attempt_number + 1), which charged an extra attempt.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # FIX: "Too High" used to ADD 5 points on even attempts. Every wrong guess now costs 5.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
