# Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it looked finished: a title, a difficulty sidebar, a guess box, and a Developer Debug Info panel that showed the secret number. Once I started guessing, it fell apart. The hints pointed the wrong way: a guess above the secret told me to "Go HIGHER!" On some turns I typed the exact secret shown in the debug panel and still didn't win. After a game ended, clicking "New Game" left me stuck on "Game over. Start a new game to try again." The score also behaved strangely and sometimes went *up* after a wrong guess.

Concrete bugs I noticed at the start:
- **The hints were backwards.** `check_guess` returned "Go HIGHER!" for "Too High" and "Go LOWER!" for "Too Low."
- **The secret became a string on even attempts.** `app.py` did `secret = str(st.session_state.secret)` when `attempts % 2 == 0`, so `check_guess` fell into its `except TypeError` branch and compared strings alphabetically.
- **New Game was broken.** It reset `attempts` and `secret` but not `status`, `score`, or `history`.
- **Scoring was wrong.** `update_score` added 5 points for "Too High" on even attempts.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location |
|-------|-------------------|-----------------|------------------------|-------------------------|
| Guess 60, secret 50 | "Too High" hint telling me to go lower | Hint says "📈 Go HIGHER!" | none | `app.py`, `check_guess` (messages swapped) |
| Guess 9 on the 2nd attempt, secret 50 | "Too Low" / "Go HIGHER" | "Too High" hint | none (no crash, the `TypeError` is caught silently) | `app.py`, `if st.session_state.attempts % 2 == 0: secret = str(...)` plus the `except TypeError` branch in `check_guess` |
| Guess the exact secret (50) on an even attempt | "Correct!" and the game is won | No win; a higher/lower hint is shown | none | Same string-secret block: `50 == "50"` is `False` |
| Win or lose a game, then click "New Game" | Fresh playable game | Still says "Game over. Start a new game to try again." | none | `app.py`, `if new_game:` block doesn't reset `status` |
| Guess too high on attempt 2 | Score goes down 5 | Score goes **up** 5 | none | `app.py`, `update_score`, "Too High" branch |
| Start a Normal game (8 attempts) | "Attempts left: 8" | "Attempts left: 7" | none | `app.py`, `st.session_state.attempts = 1` on first load |

---

## 2. How did you use AI as a teammate?

I used Claude as my AI coding assistant for this project. I gave it the starter repo and asked it to find the bugs, refactor the logic into `logic_utils.py`, fix it, and write pytest cases. I reviewed each change before keeping it.

**A suggestion that was correct:** Claude spotted that the hint messages in `check_guess` were swapped. It also found that the "every other guess is wrong" bug came from `app.py` turning the secret into a string on even attempts. It suggested swapping the messages, deleting the `try/except TypeError` string fallback, and always passing `st.session_state.secret` as an int. This was correct because `"9" > "50"` is `True` in Python string comparison, which explains why small guesses got "Too High," and `50 == "50"` is `False`, which explains why I couldn't win on even turns. I verified it with `test_single_digit_guess_vs_two_digit_secret` and `test_guess_too_high` in pytest, and by playing a game where guesses of 40, 70, 9, and 57 all gave the right hints and the final guess won.

**A suggestion I did not accept as written:** In its first draft of `logic_utils.py`, Claude also changed the difficulty ranges, making Normal 1–50 and Hard 1–100, because Hard (1–50) being a smaller range than Normal (1–100) looked like a bug. I didn't keep that change. It wasn't one of the bugs I had reproduced and logged, and changing the game's design was out of scope for fixing glitches. Hard also gives fewer attempts (5), so the smaller range can be intentional. I kept the original ranges and wrote `test_difficulty_ranges` to lock them in. I also noticed that the original AI-generated starter tests compared `check_guess(...)` directly to `"Win"`, even though the function returns a tuple. That means all 3 starter tests would fail even with correct code. I fixed the tests to unpack `outcome, message` instead of "fixing" the function to return a single string.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when two things were true: a pytest test targeting that exact bug passed, and the behavior was correct when I actually played the game in Streamlit. The tests alone weren't enough, because some bugs (the string secret, New Game) lived in `app.py`'s state handling, not in the pure functions. For example, `test_single_digit_guess_vs_two_digit_secret` checks that `check_guess(9, 50)` returns "Too Low," and `test_wrong_guesses_always_lose_points` checks that "Too High" costs 5 points on both even and odd attempts. The tests also showed that the starter tests were wrong: they compared a tuple to a string, so they failed even after the logic was fixed. In the end all 8 tests passed (output is in `README.md` and `test_results.txt`). AI helped by writing regression tests that reproduce each bug's exact trigger, like the 9-vs-50 case, instead of only testing obvious inputs.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns your entire Python script from top to bottom every time you interact with the page, like clicking a button or typing in a box. That means normal variables get wiped out and recreated on every click. `st.session_state` is like a backpack that survives the reruns: anything you put in it (the secret number, score, attempts) is still there next time. That's why the starter code wraps setup in `if "secret" not in st.session_state:`, so the secret is only picked once. It's also why the New Game bug happened: the button reset some values in the backpack but left `status` as "won" or "lost," so every rerun hit the "Game over" check and stopped.

---

## 5. Looking ahead: your developer habits

- **A habit I want to reuse:** Writing a regression test for the exact input that triggered a bug (like guessing 9 against 50) before calling it fixed. It turns "I think it works" into proof, and it keeps the bug from coming back. I also want to keep making small commits: one after logging the bugs, one after the fixes, and one after the docs.
- **What I'd do differently:** Ask the AI to fix one bug at a time and review each diff, instead of letting it change several files at once. When it changed the difficulty ranges along with the real fixes, that change was easy to miss in a big diff.
- **How this changed my thinking:** AI-generated code can look polished and even claim to be "production-ready" while hiding bugs like silent `try/except` blocks and type mix-ups. I now treat AI code as a first draft that needs human-in-the-loop verification with tests and real use, not as something to trust because it runs without crashing.
