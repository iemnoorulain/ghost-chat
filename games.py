import customtkinter as ctk
import tkinter as tk
import random
import time
from tkinter import messagebox
import config


# ══════════════════════════ SNAKE ══════════════════════════
def launch_snake(root):
    t = config.themes[config.settings["theme_index"]]

    snake_win = ctk.CTkToplevel(root)
    snake_win.title("🐍 Snake Game")
    snake_win.geometry("440x520")
    snake_win.resizable(False, False)
    snake_win.configure(fg_color=t["bg"])
    snake_win.attributes("-topmost", True)

    header = ctk.CTkFrame(snake_win, fg_color=t["sidebar"], height=50, corner_radius=0)
    header.pack(fill="x")

    score_label = ctk.CTkLabel(
        header, text=f"Score: 0  |  🏆 Best: {config.game_scores['snake']}",
        font=("Segoe UI", 15, "bold"), text_color=t["accent"])
    score_label.pack(pady=12)

    canvas = tk.Canvas(snake_win, bg="#0d1117", width=400, height=400,
                       highlightthickness=2, highlightbackground=t["accent"])
    canvas.pack(pady=10)

    snake = [[200, 200]]
    direction = ["Right"]
    food = [random.randint(0, 19) * 20, random.randint(0, 19) * 20]
    game_over = [False]
    current_score = [0]

    def move_snake():
        if game_over[0]: return
        head = snake[-1][:]
        if direction[0] == "Up": head[1] -= 20
        elif direction[0] == "Down": head[1] += 20
        elif direction[0] == "Left": head[0] -= 20
        elif direction[0] == "Right": head[0] += 20

        if head in snake or head[0] < 0 or head[1] < 0 or head[0] >= 400 or head[1] >= 400:
            game_over[0] = True
            if current_score[0] > config.game_scores["snake"]:
                config.game_scores["snake"] = current_score[0]
                config.save_data()
            if messagebox.askyesno("Game Over",
                f"🐍 Snake crashed!\n\n🎯 Score: {current_score[0]}\n"
                f"🏆 Best: {config.game_scores['snake']}\n\nPlay again?"):
                restart_game()
            else:
                snake_win.destroy()
            return

        snake.append(head)
        if head == food:
            food[0], food[1] = random.randint(0, 19) * 20, random.randint(0, 19) * 20
            current_score[0] += 1
            score_label.configure(text=f"Score: {current_score[0]}  |  🏆 Best: {config.game_scores['snake']}")
        else:
            snake.pop(0)
        draw()
        snake_win.after(120, move_snake)

    def draw():
        canvas.delete("all")
        n = max(len(snake), 1)
        for i, seg in enumerate(snake):
            g = 255 - int((i / n) * 100)
            color = f"#00{g:02x}00"
            canvas.create_rectangle(seg[0], seg[1], seg[0] + 20, seg[1] + 20,
                                    fill=color, outline="#00ff00", width=2)
        canvas.create_oval(food[0] + 2, food[1] + 2, food[0] + 18, food[1] + 18,
                           fill="#ff4444", outline="#ff8888", width=2)

    def change_direction(e):
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if e.keysym in opposites and direction[0] != opposites[e.keysym]:
            direction[0] = e.keysym

    def restart_game():
        snake.clear()
        snake.append([200, 200])
        direction[0] = "Right"
        food[0], food[1] = random.randint(0, 19) * 20, random.randint(0, 19) * 20
        game_over[0] = False
        current_score[0] = 0
        score_label.configure(text=f"Score: 0  |  🏆 Best: {config.game_scores['snake']}")
        move_snake()

    snake_win.bind("<KeyPress>", change_direction)
    canvas.bind("<KeyPress>", change_direction)
    canvas.focus_set()
    snake_win.after(100, lambda: snake_win.focus_force())
    snake_win.after(150, lambda: canvas.focus_set())
    move_snake()


# ══════════════════════════ TIC-TAC-TOE ══════════════════════════
def launch_tictactoe(root):
    t = config.themes[config.settings["theme_index"]]

    tt_win = ctk.CTkToplevel(root)
    tt_win.title("⭕ Tic-Tac-Toe")
    tt_win.geometry("350x420")
    tt_win.resizable(False, False)
    tt_win.configure(fg_color=t["bg"])
    tt_win.attributes("-topmost", True)

    header = ctk.CTkFrame(tt_win, fg_color=t["sidebar"], height=60, corner_radius=0)
    header.pack(fill="x")

    score_label = ctk.CTkLabel(
        header, text=f"✕ {config.game_scores['tic_tac_toe']['X']}  •  ⭕ {config.game_scores['tic_tac_toe']['O']}",
        font=("Segoe UI", 16, "bold"), text_color=t["accent"])
    score_label.pack(pady=15)

    canvas = tk.Canvas(tt_win, bg="#ffffff", width=320, height=320,
                       highlightthickness=2, highlightbackground=t["accent"])
    canvas.pack(pady=10)

    board = [["" for _ in range(3)] for _ in range(3)]
    turn = ["X"]

    def draw_board():
        canvas.delete("all")
        for i in range(1, 3):
            x = i * 106.67
            canvas.create_line(x, 0, x, 320, width=4, fill="#333333")
            canvas.create_line(0, x, 320, x, width=4, fill="#333333")
        for r in range(3):
            for c in range(3):
                cx, cy = c * 106.67 + 53.33, r * 106.67 + 53.33
                if board[r][c] == "X":
                    off = 33
                    canvas.create_line(cx - off, cy - off, cx + off, cy + off, width=8, fill="#3b82f6")
                    canvas.create_line(cx + off, cy - off, cx - off, cy + off, width=8, fill="#3b82f6")
                elif board[r][c] == "O":
                    canvas.create_oval(cx - 33, cy - 33, cx + 33, cy + 33, width=8, outline="#ef4444", fill="")

    def check_winner():
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "": return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != "": return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != "": return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "": return board[0][2]
        return None

    def click(event):
        r, c = min(event.y // 107, 2), min(event.x // 107, 2)
        if board[r][c] == "":
            board[r][c] = turn[0]
            turn[0] = "O" if turn[0] == "X" else "X"
            draw_board()
            winner = check_winner()
            if winner:
                config.game_scores["tic_tac_toe"][winner] += 1
                config.save_data()
                score_label.configure(
                    text=f"✕ {config.game_scores['tic_tac_toe']['X']}  •  ⭕ {config.game_scores['tic_tac_toe']['O']}")
                messagebox.showinfo("Winner!", f"🎉 {winner} wins!")
                restart_game()
            elif all(board[r][c] != "" for r in range(3) for c in range(3)):
                messagebox.showinfo("Draw", "🤝 It's a draw!")
                restart_game()

    def restart_game():
        for r in range(3):
            for c in range(3):
                board[r][c] = ""
        turn[0] = "X"
        draw_board()

    canvas.bind("<Button-1>", click)
    draw_board()


# ══════════════════════════ 2048 ══════════════════════════
def launch_2048(root):
    t = config.themes[config.settings["theme_index"]]

    win = ctk.CTkToplevel(root)
    win.title("2048")
    win.geometry("440x520")
    win.resizable(False, False)
    win.configure(fg_color=t["bg"])
    win.attributes("-topmost", True)

    header = ctk.CTkFrame(win, fg_color=t["sidebar"], height=50, corner_radius=0)
    header.pack(fill="x")

    score_label = ctk.CTkLabel(header, text="Score: 0", font=("Segoe UI", 16, "bold"),
                               text_color=t["accent"])
    score_label.pack(pady=12)

    CELL = 95
    GAP = 6
    SIZE = 4
    canvas_size = SIZE * CELL + (SIZE + 1) * GAP

    canvas = tk.Canvas(win, width=canvas_size, height=canvas_size, bg="#bbada0",
                       highlightthickness=0)
    canvas.pack(pady=10)

    TILE_COLORS = {
        0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
        256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e",
    }
    TEXT_COLORS = {0: "#cdc1b4", 2: "#776e65", 4: "#776e65"}

    grid_data = [[0] * SIZE for _ in range(SIZE)]
    score = [0]

    def add_tile():
        empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if grid_data[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            grid_data[r][c] = 4 if random.random() < 0.1 else 2

    def draw_grid():
        canvas.delete("all")
        for r in range(SIZE):
            for c in range(SIZE):
                x = GAP + c * (CELL + GAP)
                y = GAP + r * (CELL + GAP)
                val = grid_data[r][c]
                bg = TILE_COLORS.get(val, "#3c3a32")
                fg = TEXT_COLORS.get(val, "#f9f6f2")
                canvas.create_rectangle(x, y, x + CELL, y + CELL, fill=bg, outline="", width=0)
                if val:
                    fsize = 28 if val < 100 else 22 if val < 1000 else 18
                    canvas.create_text(x + CELL // 2, y + CELL // 2, text=str(val),
                                       font=("Segoe UI", fsize, "bold"), fill=fg)
        score_label.configure(text=f"Score: {score[0]}")

    def compress(row):
        new = [x for x in row if x != 0]
        new += [0] * (SIZE - len(new))
        return new

    def merge(row):
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                score[0] += row[i]
                row[i + 1] = 0
        return row

    def move_left():
        changed = False
        for r in range(SIZE):
            old = grid_data[r][:]
            grid_data[r] = compress(merge(compress(grid_data[r])))
            if grid_data[r] != old:
                changed = True
        return changed

    def rotate_cw():
        n = SIZE
        grid_data[:] = [[grid_data[n - 1 - c][r] for c in range(n)] for r in range(n)]

    def move(direction):
        rotations = {"Left": 0, "Up": 1, "Right": 2, "Down": 3}
        for _ in range(rotations[direction]):
            rotate_cw()
        changed = move_left()
        for _ in range((4 - rotations[direction]) % 4):
            rotate_cw()
        if changed:
            add_tile()
            draw_grid()
            if is_game_over():
                messagebox.showinfo("Game Over", f"🎮 Game Over!\n\nScore: {score[0]}")
                win.destroy()

    def is_game_over():
        for r in range(SIZE):
            for c in range(SIZE):
                if grid_data[r][c] == 0: return False
                if c < SIZE - 1 and grid_data[r][c] == grid_data[r][c + 1]: return False
                if r < SIZE - 1 and grid_data[r][c] == grid_data[r + 1][c]: return False
        return True

    def on_key(e):
        if e.keysym in ("Up", "Down", "Left", "Right"):
            move(e.keysym)

    add_tile()
    add_tile()
    draw_grid()

    win.bind("<KeyPress>", on_key)
    canvas.focus_set()
    win.after(100, lambda: win.focus_force())
    win.after(150, lambda: canvas.focus_set())


# ══════════════════════════ WORDLE ══════════════════════════
def launch_wordle(root):
    t = config.themes[config.settings["theme_index"]]

    win = ctk.CTkToplevel(root)
    win.title("Wordle")
    win.geometry("420x550")
    win.resizable(False, False)
    win.configure(fg_color=t["bg"])
    win.attributes("-topmost", True)

    target = random.choice(config.wordle_words).upper()
    guesses = []
    current_guess = [""]
    max_guesses = 6

    header = ctk.CTkFrame(win, fg_color=t["sidebar"], height=50, corner_radius=0)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="WORDLE", font=("Segoe UI", 18, "bold"),
                 text_color=t["accent"]).pack(pady=12)

    CELL = 58
    GAP = 6
    ROWS = 6
    COLS = 5
    canvas_w = COLS * (CELL + GAP) + GAP
    canvas_h = ROWS * (CELL + GAP) + GAP

    canvas = tk.Canvas(win, width=canvas_w, height=canvas_h, bg=t["bg"],
                       highlightthickness=0)
    canvas.pack(pady=10)

    info_label = ctk.CTkLabel(win, text="Type a 5-letter word, press Enter",
                              font=("Segoe UI", 12), text_color=t["muted"])
    info_label.pack(pady=5)

    def draw_grid():
        canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                x = GAP + col * (CELL + GAP)
                y = GAP + row * (CELL + GAP)
                bg = "#3a3a3c"
                fg = "#ffffff"
                letter = ""

                if row < len(guesses):
                    letter = guesses[row][col]
                    if letter == target[col]:
                        bg = "#538d4e"  # green
                    elif letter in target:
                        bg = "#b59f3b"  # yellow
                    else:
                        bg = "#3a3a3c"  # gray
                elif row == len(guesses):
                    if col < len(current_guess[0]):
                        letter = current_guess[0][col]
                    bg = "#272729"

                canvas.create_rectangle(x, y, x + CELL, y + CELL, fill=bg, outline="#565656", width=2)
                if letter:
                    canvas.create_text(x + CELL // 2, y + CELL // 2, text=letter,
                                       font=("Segoe UI", 22, "bold"), fill=fg)

    def on_key(e):
        if len(guesses) >= max_guesses:
            return

        key = e.keysym.upper()
        char = e.char.upper() if e.char else ""

        if key == "RETURN":
            if len(current_guess[0]) == 5:
                guess = current_guess[0]
                guesses.append(guess)
                current_guess[0] = ""
                draw_grid()
                if guess == target:
                    info_label.configure(text=f"🎉 You got it in {len(guesses)} tries!")
                elif len(guesses) >= max_guesses:
                    info_label.configure(text=f"The word was: {target}")
        elif key == "BACKSPACE":
            current_guess[0] = current_guess[0][:-1]
            draw_grid()
        elif char.isalpha() and len(char) == 1 and len(current_guess[0]) < 5:
            current_guess[0] += char
            draw_grid()

    draw_grid()
    win.bind("<KeyPress>", on_key)
    win.after(100, lambda: win.focus_force())


# ══════════════════════════ QUIZ ══════════════════════════
def launch_quiz(root):
    t = config.themes[config.settings["theme_index"]]

    win = ctk.CTkToplevel(root)
    win.title("🧠 Trivia Quiz")
    win.geometry("500x450")
    win.resizable(False, False)
    win.configure(fg_color=t["bg"])
    win.attributes("-topmost", True)

    questions = random.sample(config.trivia_questions, min(10, len(config.trivia_questions)))
    q_idx = [0]
    score = [0]
    answered = [False]

    header = ctk.CTkFrame(win, fg_color=t["sidebar"], height=50, corner_radius=0)
    header.pack(fill="x")

    score_label = ctk.CTkLabel(header, text="Score: 0 / 0",
                               font=("Segoe UI", 15, "bold"), text_color=t["accent"])
    score_label.pack(pady=12)

    body = ctk.CTkFrame(win, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=20, pady=20)

    q_label = ctk.CTkLabel(body, text="", font=("Segoe UI", 15, "bold"),
                           text_color=t["fg"], wraplength=440, justify="left")
    q_label.pack(pady=(0, 20))

    progress_label = ctk.CTkLabel(body, text="", font=("Segoe UI", 11),
                                  text_color=t["muted"])
    progress_label.pack(pady=(0, 10))

    btn_frame = ctk.CTkFrame(body, fg_color="transparent")
    btn_frame.pack(fill="x")

    option_btns = []
    for i in range(4):
        btn = ctk.CTkButton(btn_frame, text="", height=42, corner_radius=10,
                            font=("Segoe UI", 13), fg_color=t["card"],
                            hover_color=t["btn_hover"], text_color=t["fg"],
                            command=lambda idx=i: check_answer(idx))
        btn.pack(fill="x", pady=4)
        option_btns.append(btn)

    next_btn = ctk.CTkButton(body, text="Next →", height=38, corner_radius=10,
                             fg_color=t["accent"], hover_color=t["accent_hover"],
                             text_color="#fff", command=lambda: next_question(),
                             font=("Segoe UI", 13, "bold"))

    def load_question():
        if q_idx[0] >= len(questions):
            q_label.configure(text=f"🏆 Quiz Complete!\n\nYou scored {score[0]} out of {len(questions)}!")
            for b in option_btns:
                b.pack_forget()
            next_btn.pack_forget()
            progress_label.configure(text="")
            return

        answered[0] = False
        q = questions[q_idx[0]]
        q_label.configure(text=f"Q{q_idx[0] + 1}: {q['q']}")
        progress_label.configure(text=f"Question {q_idx[0] + 1} of {len(questions)}")
        for i, btn in enumerate(option_btns):
            btn.configure(text=f"  {chr(65 + i)}.  {q['options'][i]}",
                          fg_color=t["card"], text_color=t["fg"])
            btn.pack(fill="x", pady=4)
        next_btn.pack_forget()

    def check_answer(idx):
        if answered[0]:
            return
        answered[0] = True
        q = questions[q_idx[0]]
        correct = q["answer"]
        if idx == correct:
            score[0] += 1
            option_btns[idx].configure(fg_color="#22c55e", text_color="#fff")
        else:
            option_btns[idx].configure(fg_color="#ef4444", text_color="#fff")
            option_btns[correct].configure(fg_color="#22c55e", text_color="#fff")

        score_label.configure(text=f"Score: {score[0]} / {q_idx[0] + 1}")
        next_btn.pack(pady=(15, 0))

    def next_question():
        q_idx[0] += 1
        load_question()

    load_question()


# ══════════════════════════ TYPING TEST ══════════════════════════
def launch_typing_test(root):
    t = config.themes[config.settings["theme_index"]]

    win = ctk.CTkToplevel(root)
    win.title("⌨️ Typing Speed Test")
    win.geometry("680x580")
    win.resizable(False, False)
    win.configure(fg_color=t["bg"])
    win.attributes("-topmost", True)

    target_text = [random.choice(config.typing_test_texts)]
    start_time = [None]
    finished = [False]
    timer_id = [None]
    total_keystrokes = [0]
    error_keystrokes = [0]

    # ── Header ──
    header = ctk.CTkFrame(win, fg_color=t["sidebar"], height=50, corner_radius=0)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="⌨️ Typing Speed Test", font=("Segoe UI", 16, "bold"),
                 text_color=t["accent"]).pack(pady=12)

    # ── Live Stats Bar ──
    stats_frame = ctk.CTkFrame(win, fg_color=t["card"], height=60, corner_radius=0)
    stats_frame.pack(fill="x", padx=0)
    stats_inner = ctk.CTkFrame(stats_frame, fg_color="transparent")
    stats_inner.pack(pady=10)

    def _stat_box(parent, icon, label_text, value_text):
        box = ctk.CTkFrame(parent, fg_color="transparent", width=110)
        box.pack(side="left", padx=14)
        ctk.CTkLabel(box, text=icon, font=("Segoe UI", 18)).pack()
        val = ctk.CTkLabel(box, text=value_text, font=("Consolas", 20, "bold"),
                           text_color=t["accent"])
        val.pack()
        ctk.CTkLabel(box, text=label_text, font=("Segoe UI", 9),
                     text_color=t["muted"]).pack()
        return val

    wpm_val = _stat_box(stats_inner, "📝", "WPM", "0")
    acc_val = _stat_box(stats_inner, "🎯", "ACCURACY", "100%")
    time_val = _stat_box(stats_inner, "⏱️", "TIME", "0.0s")
    best_val = _stat_box(stats_inner, "🏆", "BEST WPM", str(config.game_scores["typing_test"]))
    speed_val = _stat_box(stats_inner, "⚡", "CHARS/S", "0.0")

    # ── Body ──
    body = ctk.CTkFrame(win, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=25, pady=(12, 10))

    ctk.CTkLabel(body, text="Type the text below as fast as you can:",
                 font=("Segoe UI", 12), text_color=t["muted"]).pack(anchor="w")

    # Canvas for character-by-character colored text display
    text_canvas_frame = ctk.CTkFrame(body, fg_color=t["card"], corner_radius=10)
    text_canvas_frame.pack(fill="x", pady=(8, 10))
    text_canvas = tk.Canvas(text_canvas_frame, bg=t["card"], highlightthickness=0,
                            height=100, width=610)
    text_canvas.pack(padx=10, pady=10)

    def draw_text_colored(typed=""):
        text_canvas.delete("all")
        x = 8
        y = 8
        max_w = 600
        font_spec = ("Consolas", 13)
        line_height = 22
        for i, ch in enumerate(target_text[0]):
            if i < len(typed):
                if typed[i] == ch:
                    color = t.get("success", "#22c55e")  # green
                else:
                    color = t.get("danger", "#f87171")   # red
            elif i == len(typed):
                color = t["accent"]  # cursor position
            else:
                color = t.get("muted", "#6b6b80")  # untyped

            # Measure char width before placing
            tmp = text_canvas.create_text(0, 0, text=ch, anchor="nw", font=font_spec)
            tmp_bbox = text_canvas.bbox(tmp)
            text_canvas.delete(tmp)
            char_w = (tmp_bbox[2] - tmp_bbox[0]) if tmp_bbox else 10

            # Word wrap: if we'd exceed max width on a space, move to next line
            if x + char_w > max_w:
                x = 8
                y += line_height

            tid = text_canvas.create_text(x, y, text=ch, anchor="nw",
                                          font=font_spec, fill=color)
            # Underline cursor position
            if i == len(typed):
                bbox = text_canvas.bbox(tid)
                if bbox:
                    text_canvas.create_line(bbox[0], bbox[3] + 1, bbox[2], bbox[3] + 1,
                                            fill=t["accent"], width=2)
            x += char_w + 1

        # Auto-resize canvas height to fit all text
        needed_h = y + line_height + 8
        if needed_h > 100:
            text_canvas.configure(height=needed_h)
        else:
            text_canvas.configure(height=100)

    draw_text_colored()

    entry = ctk.CTkEntry(body, font=("Consolas", 14), height=42,
                         fg_color=t["input_bg"], text_color=t["fg"],
                         border_color=t["input_border"],
                         placeholder_text="Start typing here...")
    entry.pack(fill="x")

    # ── Results label ──
    result_label = ctk.CTkLabel(body, text="Press Enter to finish early",
                                font=("Segoe UI", 12), text_color=t["muted"])
    result_label.pack(pady=(8, 0))

    # ── Restart button (always visible) ──
    restart_btn = ctk.CTkButton(body, text="🔄 Restart / New Test", height=38,
                                corner_radius=10, fg_color=t["btn"],
                                hover_color=t["btn_hover"], text_color=t["fg"],
                                font=("Segoe UI", 13, "bold"),
                                command=lambda: restart_test())
    restart_btn.pack(pady=(8, 0))

    def update_live_stats():
        if finished[0] or start_time[0] is None:
            return
        elapsed = time.time() - start_time[0]
        typed = entry.get()
        typed_len = len(typed)

        # WPM: standard formula (chars / 5) / minutes
        if elapsed > 0:
            wpm = (typed_len / 5.0) / (elapsed / 60.0)
        else:
            wpm = 0

        # Accuracy
        if typed_len > 0:
            correct = sum(1 for a, b in zip(typed, target_text[0]) if a == b)
            accuracy = (correct / typed_len) * 100
        else:
            accuracy = 100

        # Chars per second
        cps = typed_len / elapsed if elapsed > 0 else 0

        wpm_val.configure(text=f"{wpm:.0f}")
        acc_val.configure(text=f"{accuracy:.0f}%")
        time_val.configure(text=f"{elapsed:.1f}s")
        speed_val.configure(text=f"{cps:.1f}")

        timer_id[0] = win.after(200, update_live_stats)

    def finish_test():
        """Stop the test and show final results based on what was typed so far."""
        if finished[0] or start_time[0] is None:
            return
        finished[0] = True
        elapsed = time.time() - start_time[0]
        if timer_id[0]:
            win.after_cancel(timer_id[0])

        typed = entry.get()
        typed_len = len(typed)

        # Final WPM (standard: chars/5 / minutes)
        wpm = (typed_len / 5.0) / (elapsed / 60.0) if elapsed > 0 else 0

        # Accuracy (correct chars vs target)
        correct = sum(1 for a, b in zip(typed, target_text[0]) if a == b)
        compared_len = min(typed_len, len(target_text[0]))
        accuracy = (correct / compared_len) * 100 if compared_len > 0 else 0

        # Completion percentage
        completion = (typed_len / len(target_text[0])) * 100

        # Chars per second
        cps = typed_len / elapsed if elapsed > 0 else 0

        # Update final stats
        wpm_val.configure(text=f"{wpm:.0f}")
        acc_val.configure(text=f"{accuracy:.0f}%")
        time_val.configure(text=f"{elapsed:.1f}s")
        speed_val.configure(text=f"{cps:.1f}")

        # Check best score
        wpm_int = int(wpm)
        new_best = ""
        if wpm_int > config.game_scores["typing_test"]:
            config.game_scores["typing_test"] = wpm_int
            config.save_data()
            best_val.configure(text=str(wpm_int))
            new_best = "  🎉 New Best!"

        if completion >= 100:
            msg = f"✅ Complete! {wpm:.0f} WPM • {accuracy:.0f}% • {elapsed:.1f}s{new_best}"
        else:
            msg = f"🏁 Finished! {wpm:.0f} WPM • {accuracy:.0f}% • {completion:.0f}% typed • {elapsed:.1f}s{new_best}"

        result_label.configure(text=msg, font=("Segoe UI", 13, "bold"), text_color=t["accent"])
        entry.configure(state="disabled")

    def on_enter(e):
        """Handle Enter key to stop the test."""
        if not finished[0] and start_time[0] is not None:
            finish_test()
        return "break"  # Prevent newline/default behavior

    def on_key(e):
        if finished[0]:
            return
        if start_time[0] is None and entry.get():
            start_time[0] = time.time()
            update_live_stats()

        typed = entry.get()
        total_keystrokes[0] += 1

        # Track errors
        if typed:
            idx = len(typed) - 1
            if idx < len(target_text[0]) and typed[idx] != target_text[0][idx]:
                error_keystrokes[0] += 1

        # Update colored display
        draw_text_colored(typed)

        # Auto-finish when fully typed
        if typed == target_text[0]:
            finish_test()

    def restart_test():
        # Reset all state
        target_text[0] = random.choice(config.typing_test_texts)
        start_time[0] = None
        finished[0] = False
        total_keystrokes[0] = 0
        error_keystrokes[0] = 0
        if timer_id[0]:
            win.after_cancel(timer_id[0])
        timer_id[0] = None

        # Reset UI
        entry.configure(state="normal")
        entry.delete(0, tk.END)
        draw_text_colored()
        wpm_val.configure(text="0")
        acc_val.configure(text="100%")
        time_val.configure(text="0.0s")
        speed_val.configure(text="0.0")
        best_val.configure(text=str(config.game_scores["typing_test"]))
        result_label.configure(text="Press Enter to finish early",
                               font=("Segoe UI", 12), text_color=t["muted"])
        entry.focus()

    entry.bind("<KeyRelease>", on_key)
    entry.bind("<Return>", on_enter)
    win.after(100, lambda: entry.focus())
