from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

# Starter tests, updated: check_guess returns (outcome, message), not just outcome. 

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message  # bug fix: used to say "Go HIGHER!"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message  # bug fix: used to say "Go LOWER!"

# New tests targeting the bugs I fixed

def test_single_digit_guess_vs_two_digit_secret():
    # Regression: comparing as strings made "9" > "50" -> wrongly "Too High"
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"

def test_wrong_guesses_always_lose_points():
    # Regression: "Too High" used to ADD 5 points on even attempts
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too High", 3) == -5
    assert update_score(0, "Too Low", 2) == -5

def test_win_on_first_attempt_scores_90():
    assert update_score(0, "Win", 1) == 90

def test_parse_guess_rejects_bad_input():
    assert parse_guess("")[0] is False
    assert parse_guess("   ")[0] is False
    assert parse_guess("abc")[0] is False
    assert parse_guess("42") == (True, 42, None)

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
