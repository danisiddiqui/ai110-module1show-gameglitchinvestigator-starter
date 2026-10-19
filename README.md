# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game's purpose:** A Streamlit number-guessing game. The player picks a difficulty, guesses a secret number, and gets "higher/lower" hints. The score goes down 5 for each wrong guess and up for a win (more points for winning in fewer attempts).
- [x] **Bugs found:**
  1. Hints were backwards: a guess that was too high said "Go HIGHER!"
  2. On every even-numbered attempt the secret was turned into a string, so numbers were compared alphabetically (`"9" > "50"`) and a correct guess could not win.
  3. "New Game" didn't reset `status`, `score`, or `history`, so after a win or loss the game stayed stuck on "Game over."
  4. The score *went up* 5 points for a "Too High" guess on even attempts, and win points charged an extra attempt.
  5. `attempts` started at 1 but reset to 0, so the first game had one fewer guess than allowed. Invalid input like "abc" also used up an attempt.
  6. The range text always said "1 and 100," and New Game always picked from 1–100, whatever the difficulty.
- [x] **Fixes applied:**
  - Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` from `app.py` into `logic_utils.py` and imported them in `app.py`.
  - Swapped the hint messages and removed the string-comparison fallback in `check_guess`.
  - `app.py` now always passes the integer secret to `check_guess`.
  - New Game now resets every piece of session state and uses the difficulty's range.
  - Every wrong guess costs 5 points; win points are `100 - 10 * attempts` (min 10).
  - Attempts start at 0, and invalid input no longer counts as an attempt.
  - Updated the starter tests (they compared a tuple to a string) and added regression tests for each fix.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

Sample game on **Normal** (range 1–100, 8 attempts). The secret number was 57.

1. The game starts with "Guess a number between 1 and 100," a score of 0, and 0 attempts used.
2. User enters `abc`. The game shows "That is not a number." No attempt is used and the score stays 0.
3. User enters `40`. The game shows "📈 Go HIGHER!" (Too Low). Score: -5.
4. User enters `70`. The game shows "📉 Go LOWER!" (Too High). Score: -10. Before the fix, this was the even-attempt case that gave the wrong hint and *added* points.
5. User enters `9`. The game correctly shows "📈 Go HIGHER!" Before the fix, the string comparison `"9" > "50"` could make this say "Too High." Score: -15.
6. User enters `57`. Balloons appear, with "You won! The secret was 57. Final score: 45" (-15 + 60 points for winning on attempt 4).
7. User clicks **New Game 🔁**. Status goes back to "playing," score and attempts reset to 0, history clears, and a new secret is picked in range. The game is playable again.


## 🧪 Test Results

```
============================= test session starts ==============================
platform -- Python 3, pytest
cachedir: .pytest_cache
rootdir: .
plugins: anyio-4.15.1
collecting ... collected 8 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 12%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 25%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 37%]
tests/test_game_logic.py::test_single_digit_guess_vs_two_digit_secret PASSED [ 50%]
tests/test_game_logic.py::test_wrong_guesses_always_lose_points PASSED   [ 62%]
tests/test_game_logic.py::test_win_on_first_attempt_scores_90 PASSED     [ 75%]
tests/test_game_logic.py::test_parse_guess_rejects_bad_input PASSED      [ 87%]
tests/test_game_logic.py::test_difficulty_ranges PASSED                  [100%]

============================== 8 passed in 0.04s ===============================
```

## 🚀 Stretch Features

Not attempted. Only the required features were completed.
