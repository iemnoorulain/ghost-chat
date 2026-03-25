import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import threading
import os
import re
import random
import webbrowser
from datetime import datetime
from PIL import ImageGrab

import config
import utils
import ai_handler
import games
import code_generator
import format_converter
import summarizer

# ─── Appearance ───
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GhostChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        config.load_data()

        self.title("Ghost Chat")
        self.geometry("1150x780")
        self.minsize(950, 650)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # State
        self.is_listening = False
        self.pomodoro_running = False
        self.pomodoro_time = 25 * 60
        self.listening_thread = None
        self.msg_count = 0
        self.reminders = []  # List of (after_id, description)
        self.uploaded_file: str | None = None # Current attached file for prompts

        self._build_ui()
        self.apply_theme()
        self._welcome()
        
        self._start_wake_word_listener()

    def _start_wake_word_listener(self):
        if not ai_handler.VOICE_INPUT_AVAILABLE:
            return
            
        def _wake_word_loop():
            import speech_recognition as sr
            import time
            bg_recognizer = sr.Recognizer()
            bg_recognizer.energy_threshold = 4000
            bg_recognizer.dynamic_energy_threshold = True
            
            while True:
                if config.settings.get("wake_word_enabled", True) and not self.is_listening:
                    try:
                        with sr.Microphone() as source:
                            bg_recognizer.adjust_for_ambient_noise(source, duration=0.5)
                            audio = bg_recognizer.listen(source, timeout=1, phrase_time_limit=3)
                            
                        try:
                            text = bg_recognizer.recognize_whisper(audio, model="base.en", language="english").lower()
                        except:
                            text = ""
                            
                        clean_text = re.sub(r'[^\w\s]', '', text)
                        if "heyghost" in clean_text or "hey ghost" in text:
                            self.after(0, self.toggle_voice)
                    except sr.WaitTimeoutError:
                        pass
                    except Exception:
                        pass
                else:
                    time.sleep(1)
                    
        threading.Thread(target=_wake_word_loop, daemon=True).start()

    # ══════════════════════════ UI BUILD ══════════════════════════
    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ── HEADER ──
        self.header = ctk.CTkFrame(self, height=56, corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_columnconfigure(1, weight=1)

        self.logo = ctk.CTkLabel(
            self.header, text="  👻  Ghost Chat",
            font=("Segoe UI Semibold", 22),
        )
        self.logo.grid(row=0, column=0, padx=18, pady=12, sticky="w")

        # right‑side header controls
        hdr_right = ctk.CTkFrame(self.header, fg_color="transparent")
        hdr_right.grid(row=0, column=2, padx=14, sticky="e")

        self.theme_pill = ctk.CTkButton(
            hdr_right, text=f"🎨 {config.themes[config.settings['theme_index']]['name']}",
            width=120, height=30, corner_radius=15,
            command=self.cycle_theme,
            font=("Segoe UI", 12),
        )
        self.theme_pill.pack(side="left", padx=4)

        self.settings_pill = ctk.CTkButton(
            hdr_right, text="⚙️", width=36, height=30,
            corner_radius=15, command=self.open_settings,
            font=("Segoe UI", 16),
        )
        self.settings_pill.pack(side="left", padx=4)

        # thin accent divider
        self.divider = ctk.CTkFrame(self, height=2, corner_radius=0)
        self.divider.grid(row=0, column=0, columnspan=2, sticky="sew")

        # ── SIDEBAR ──
        self.sidebar = ctk.CTkFrame(self, width=230, corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # sidebar inner (scrollable)
        self.sidebar_inner = ctk.CTkScrollableFrame(
            self.sidebar, fg_color="transparent",
        )
        self.sidebar_inner.pack(fill="both", expand=True, padx=6, pady=8)

        self._sidebar_section("ACTIONS")
        self._sidebar_btn("📋  View Tasks", self.view_tasks)
        self._sidebar_btn("➕  Add Task", self.add_task)
        self._sidebar_btn("🗑️  Delete Task", self.delete_task)
        self._sidebar_btn("📸  Screenshot", self.take_screenshot)
        self._sidebar_btn("💾  Export Chat", self.export_chat)
        self._sidebar_btn("🧹  Clear Chat", self.clear_chat)
        self._sidebar_btn("🔍  File Search", self.prompt_file_search)
        self._sidebar_btn("💻  Code Generator", lambda: code_generator.launch_code_generator(self))
        self._sidebar_btn("🔄  Format Converter", lambda: format_converter.launch_format_converter(self))
        self._sidebar_btn("🌐  Summarizer", lambda: summarizer.launch_summarizer(self))

        self._sidebar_section("GAMES")
        self._sidebar_btn("🐍  Snake", lambda: [games.launch_snake(self)])
        self._sidebar_btn("⭕  Tic-Tac-Toe", lambda: [games.launch_tictactoe(self)])
        self._sidebar_btn("🔢  2048", lambda: [games.launch_2048(self)])
        self._sidebar_btn("🟩  Wordle", lambda: [games.launch_wordle(self)])
        self._sidebar_btn("🧠  Quiz", lambda: [games.launch_quiz(self)])
        self._sidebar_btn("⌨️  Typing Test", lambda: [games.launch_typing_test(self)])

        # ── POMODORO ──
        self._sidebar_section("FOCUS TIMER")

        self.pomo_display = ctk.CTkLabel(
            self.sidebar_inner, text="25 : 00",
            font=("Consolas", 32, "bold"),
        )
        self.pomo_display.pack(pady=(2, 4))

        pomo_row = ctk.CTkFrame(self.sidebar_inner, fg_color="transparent")
        pomo_row.pack()
        self.pomo_btn = ctk.CTkButton(
            pomo_row, text="▶  Start", width=90, height=30,
            corner_radius=8, command=self.toggle_pomodoro,
        )
        self.pomo_btn.pack(side="left", padx=4)
        self.pomo_reset = ctk.CTkButton(
            pomo_row, text="↺  Reset", width=90, height=30,
            corner_radius=8, command=self.reset_pomodoro,
        )
        self.pomo_reset.pack(side="left", padx=4)

        # ── CHAT AREA ──
        self.chat_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.chat_area.grid(row=1, column=1, sticky="nsew")
        self.chat_area.grid_rowconfigure(0, weight=1)
        self.chat_area.grid_columnconfigure(0, weight=1)

        self.chat_scroll = ctk.CTkScrollableFrame(
            self.chat_area, fg_color="transparent",
        )
        self.chat_scroll.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 0))

        # Quick Replies
        self.qr_frame = ctk.CTkFrame(self.chat_area, fg_color="transparent", height=38)
        if config.settings["quick_replies_visible"]:
            self.qr_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
            self._build_quick_replies()

        # ── INPUT BAR ──
        self.input_bar = ctk.CTkFrame(self.chat_area, height=54, corner_radius=12)
        self.input_bar.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 10))
        self.input_bar.grid_columnconfigure(0, weight=1)

        self.msg_entry = ctk.CTkEntry(
            self.input_bar, font=("Segoe UI", 13),
            placeholder_text="Type a message, command, or ask anything…",
            border_width=0, corner_radius=10, height=40,
        )
        self.msg_entry.grid(row=0, column=0, sticky="ew", padx=(12, 6), pady=7)
        self.msg_entry.bind("<Return>", self.send_message)

        self.btn_voice = ctk.CTkButton(
            self.input_bar, text="🎤", width=40, height=40,
            corner_radius=20, command=self.toggle_voice,
            font=("Segoe UI", 16),
        )
        self.btn_voice.grid(row=0, column=1, padx=2, pady=7)

        self.btn_send = ctk.CTkButton(
            self.input_bar, text="➤", width=40, height=40,
            corner_radius=20, command=self.send_message,
            font=("Segoe UI", 18),
        )
        self.btn_send.grid(row=0, column=2, padx=(2, 6), pady=7)
        
        self.btn_upload = ctk.CTkButton(
            self.input_bar, text="📎", width=40, height=40,
            corner_radius=20, command=self.handle_upload,
            font=("Segoe UI", 16), fg_color="transparent", hover_color="#333", text_color="#ccc"
        )
        self.btn_upload.grid(row=0, column=3, padx=(2, 12), pady=7)

        # ── STATUS BAR ──
        self.status_bar = ctk.CTkFrame(self, height=24, corner_radius=0)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.status_left = ctk.CTkLabel(
            self.status_bar, text="Ready", font=("Segoe UI", 10),
        )
        self.status_left.pack(side="left", padx=12)

        self.status_right = ctk.CTkLabel(
            self.status_bar, text="Messages: 0",
            font=("Segoe UI", 10),
        )
        self.status_right.pack(side="right", padx=12)

    # ── helpers ──
    def _sidebar_section(self, label):
        ctk.CTkLabel(
            self.sidebar_inner, text=label,
            font=("Segoe UI Semibold", 11),
            anchor="w",
        ).pack(fill="x", padx=8, pady=(14, 4))

    def _sidebar_btn(self, text, command):
        btn = ctk.CTkButton(
            self.sidebar_inner, text=text, command=command,
            fg_color="transparent", anchor="w",
            height=34, corner_radius=8,
            font=("Segoe UI", 12),
        )
        btn.pack(fill="x", pady=1, padx=4)

    def _build_quick_replies(self):
        for w in self.qr_frame.winfo_children():
            w.destroy()
        for r in config.quick_replies:
            ctk.CTkButton(
                self.qr_frame, text=r["text"], width=0, height=28,
                corner_radius=14, font=("Segoe UI", 11),
                command=lambda c=r["command"]: self._qr_click(c),
            ).pack(side="left", padx=3)

    def _qr_click(self, cmd):
        if cmd.endswith(" "):
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.insert(0, cmd)
            self.msg_entry.focus()
        else:
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.insert(0, cmd)
            self.send_message()

    def _welcome(self):
        quote = random.choice(config.quotes)
        self.add_bubble(
            "Ghost",
            f"👋 Welcome to **Ghost Chat**!\n\n"
            f"💡 _{quote}_\n\n"
            f"Type **help** to see all commands.",
        )

    # ══════════════════════════ THEME ══════════════════════════
    def apply_theme(self):
        t = config.themes[config.settings["theme_index"]]

        # Root window
        self.configure(fg_color=t["bg"])

        # ── Header ──
        self.header.configure(fg_color=t["sidebar"])
        self.logo.configure(text_color=t["accent"])
        self.divider.configure(fg_color=t["accent"])

        self.theme_pill.configure(
            fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"],
            text=f"🎨 {t['name']}")
        self.settings_pill.configure(
            fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"])

        # ── Sidebar ──
        self.sidebar.configure(fg_color=t["sidebar"])
        self.sidebar_inner.configure(fg_color=t["sidebar"])
        # Walk ALL sidebar children
        for child in self.sidebar_inner.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.configure(
                    fg_color="transparent",
                    hover_color=t["sidebar_hover"],
                    text_color=t["fg"])
            elif isinstance(child, ctk.CTkLabel):
                child.configure(text_color=t["muted"])
            elif isinstance(child, ctk.CTkFrame):
                child.configure(fg_color="transparent")
                for sub in child.winfo_children():
                    if isinstance(sub, ctk.CTkButton):
                        sub.configure(
                            fg_color=t["btn"], hover_color=t["btn_hover"],
                            text_color=t["fg"])

        # Pomodoro specifics
        self.pomo_display.configure(text_color=t["accent"])
        if not self.pomodoro_running:
            self.pomo_btn.configure(fg_color=t["accent"], hover_color=t["accent_hover"])
        else:
            self.pomo_btn.configure(fg_color=t["danger"], hover_color="#c82333")
        self.pomo_reset.configure(fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"])

        # ── Chat area ──
        self.chat_area.configure(fg_color=t["bg"])
        self.chat_scroll.configure(fg_color=t["bg"])

        # Deep-walk existing chat bubbles to re-color them
        self._theme_children(self.chat_scroll, t)

        # ── Quick reply buttons ──
        self.qr_frame.configure(fg_color=t["bg"])
        for child in self.qr_frame.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.configure(
                    fg_color=t["btn"], hover_color=t["btn_hover"],
                    text_color=t["fg"])

        # ── Input bar ──
        self.input_bar.configure(fg_color=t["card"])
        self.msg_entry.configure(
            fg_color=t["input_bg"], text_color=t["fg"],
            border_color=t["input_border"])
        self.btn_send.configure(
            fg_color=t["accent"], hover_color=t["accent_hover"], text_color="#fff")
        if not self.is_listening:
            self.btn_voice.configure(
                fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"])
        else:
            self.btn_voice.configure(
                fg_color=t["danger"], hover_color="#c82333", text_color="#fff")

        # ── Status bar ──
        self.status_bar.configure(fg_color=t["sidebar"])
        self.status_left.configure(text_color=t["muted"])
        self.status_right.configure(text_color=t["muted"])

    def _theme_children(self, parent, t):
        """Recursively re-color all children of a widget."""
        try:
            children = parent.winfo_children()
        except:
            return
        for child in children:
            try:
                if isinstance(child, ctk.CTkFrame):
                    # Bubble frames have a color set; transparent ones stay transparent
                    current = child.cget("fg_color")
                    if current == "transparent" or current == ("transparent",):
                        child.configure(fg_color="transparent")
                    # Don't override bubble colors — they are set per-message
                elif isinstance(child, ctk.CTkLabel):
                    # Only update timestamp labels (small font) and avatars
                    font = child.cget("font")
                    # Timestamp labels use size 9
                    if hasattr(font, "cget"):
                        pass  # CTkFont object
                    # We'll just update muted-colored labels
                    try:
                        current_color = child.cget("text_color")
                        # If it was using a muted color from any old theme, update it
                        if current_color not in ("#ffffff", "#fff"):
                            # Check if this is a timestamp (small) or avatar (emoji)
                            text = child.cget("text")
                            if text == "👻":
                                pass  # Leave avatar alone
                            elif len(text) <= 5:  # Timestamps like "12:34"
                                child.configure(text_color=t["muted"])
                    except:
                        pass
            except:
                pass
            # Recurse
            self._theme_children(child, t)

    # ══════════════════════════ CHAT ══════════════════════════
    def add_bubble(self, sender, text, is_user=False):
        t = config.themes[config.settings["theme_index"]]

        row = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        row.pack(fill="x", pady=4, padx=6)

        anchor = "e" if is_user else "w"
        inner = ctk.CTkFrame(row, fg_color="transparent")
        inner.pack(anchor=anchor, padx=4)

        if not is_user:
            ctk.CTkLabel(inner, text="👻", font=("Segoe UI", 22)).pack(
                side="left", padx=(0, 8))

        bubble_bg = t["msg_user_bg"] if is_user else t["msg_ghost_bg"]
        bubble_fg = t["msg_user_fg"] if is_user else t["msg_ghost_fg"]

        bubble = ctk.CTkFrame(inner, fg_color=bubble_bg, corner_radius=16)
        bubble.pack(side="left" if not is_user else "right")

        self._render_markdown(bubble, text, bubble_fg)
        label = bubble.winfo_children()[0] if bubble.winfo_children() else ctk.CTkLabel(bubble, text="")

        ts = ctk.CTkLabel(
            row, text=datetime.now().strftime("%H:%M"),
            font=("Segoe UI", 9), text_color=t["muted"],
        )
        ts.pack(anchor=anchor, padx=14)

        self.msg_count += 1
        self.status_right.configure(text=f"Messages: {self.msg_count}")
        config.message_log.append({
            "sender": sender, "text": text,
            "time": datetime.now().strftime("%H:%M:%S"),
        })

        if config.settings["auto_scroll"]:
            self.chat_scroll.update_idletasks()
            self.after(50, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))

        return label, bubble

    def _render_markdown(self, bubble, text, text_color):
        for widget in bubble.winfo_children():
            widget.destroy()

        t = config.themes[config.settings["theme_index"]]
        parts = re.split(r'(```.*?```)', text, flags=re.DOTALL)
        
        for part in parts:
            if not part: continue
            if part.startswith('```') and part.endswith('```'):
                code_text = part.strip()[3:-3].strip()
                lines = code_text.split('\n')
                if lines and len(lines[0].split()) == 1 and not (' ' in lines[0] and '.' in lines[0]):
                    lang = lines[0]
                    code_text = '\n'.join(lines[1:]).strip()
                else:
                    lang = "Code"
                    
                code_frame = ctk.CTkFrame(bubble, fg_color="#1e1e1e", corner_radius=8)
                code_frame.pack(padx=10, pady=5, fill="x")
                
                header = ctk.CTkLabel(code_frame, text=lang.upper(), font=("Segoe UI", 10, "bold"), text_color="#aaaaaa")
                header.pack(anchor="w", padx=8, pady=(4, 0))
                
                num_lines = len(code_text.split('\n'))
                textbox = ctk.CTkTextbox(code_frame, font=("Consolas", config.settings["font_size"]), 
                                         fg_color="#1e1e1e", text_color="#d4d4d4",
                                         wrap="word", height=min(400, max(60, num_lines*22)))
                textbox.insert("1.0", code_text)
                textbox.configure(state="disabled")
                textbox.pack(padx=8, pady=(0, 8), fill="both", expand=True)
            else:
                if part.strip():
                    # Parse custom commands like [CMD: open_folder | path]
                    segments = re.split(r'(\[CMD:\s*open_folder\s*\|\s*(.*?)\])', part)
                    for i in range(0, len(segments), 3):
                        txt = segments[i]
                        if txt.strip():
                            label = ctk.CTkLabel(
                                bubble, text=txt.strip(), text_color=text_color,
                                font=("Segoe UI", config.settings["font_size"]),
                                justify="left", wraplength=500,
                            )
                            label.pack(padx=16, pady=4, anchor="w")
                        
                        if i + 2 < len(segments):
                            folder_path = segments[i+2].strip()
                            btn = ctk.CTkButton(
                                bubble, text="📂 Open Folder",
                                width=120, height=28, fg_color=t["accent"],
                                hover_color=t["accent_hover"],
                                command=lambda p=folder_path: os.startfile(p) if os.path.exists(p) else None
                            )
                            btn.pack(padx=16, pady=2, anchor="w")

        # Right-click context menu
        def _show_copy_menu(event):
            menu = tk.Menu(self, tearoff=0, bg=t["card"], fg=t["fg"],
                           activebackground=t["accent"], activeforeground="#fff",
                           font=("Segoe UI", 11))
            menu.add_command(label="📋 Copy Message", command=lambda: self._copy_to_clipboard(text))
            menu.tk_popup(event.x_root, event.y_root)

        bubble.bind("<Button-3>", _show_copy_menu)
        for child in bubble.winfo_children():
            child.bind("<Button-3>", _show_copy_menu)

    def _copy_to_clipboard(self, text):
        """Copy text to clipboard and show feedback."""
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_left.configure(text="✅ Copied to clipboard!")
        self.after(2000, lambda: self.status_left.configure(text="Ready"))

    def stream_cb(self, chunk, done, label, buf, bubble=None):
        if not done:
            buf[0] += chunk
            label.configure(text=buf[0])
            if config.settings["auto_scroll"]:
                self.chat_scroll._parent_canvas.yview_moveto(1.0)
        else:
            if chunk:
                self.add_bubble("Ghost", chunk)
            else:
                self.status_left.configure(text="Ready")
                ai_handler.speak_text(buf[0])
                if bubble:
                    bubble_fg = config.themes[config.settings["theme_index"]]["msg_ghost_fg"]
                    self._render_markdown(bubble, buf[0], bubble_fg)
                    if config.settings["auto_scroll"]:
                        self.chat_scroll.update_idletasks()
                        self.after(50, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        self.add_bubble("You", msg, is_user=True)
        self.msg_entry.delete(0, tk.END)
        self._process(msg)

    def _process(self, msg):
        lo = msg.lower()

        # ── help ──
        if lo == "help":
            self.add_bubble("Ghost",
                "📋 **Commands:**\n"
                "  🎮 **Games:** snake, tic-tac-toe, 2048, wordle, quiz, typing test\n"
                "  🧮 **Math:** type equations (e.g. 5+3*2)\n"
                "  🔍 **Search:** search [query]\n"
                "  🔎 **File:** find [filename]\n"
                "  ☁️ **Weather:** weather in [city]\n"
                "  📱 **Apps:** open chrome/notepad/calculator\n"
                "  🌐 **Web:** open youtube/google/github\n"
                "  ✅ **Tasks:** add/view/delete task\n"
                "  ⏰ **Reminder:** remind me in [X] min [text]\n"
                "  💻 **Code Gen:** code / codegen / generate code\n"
                "  💡 **Explain:** explain [paste code]\n"
                "  🎤 **Voice:** click mic or say 'Hey Ghost'\n"
                "  💡 **Quote:** type 'quote' for motivation\n"
                "  ⏯️ **Media:** pause/play/next/prev music\n"
                "  🔊 **Volume:** volume [0-100] / mute / volume up/down\n"
                "  🔒 **Lock:** lock screen")
            return

        if lo == "help games":
            self.add_bubble("Ghost",
                "🎮 **Available Games:**\n"
                "  🐍 **Snake** — classic snake game\n"
                "  ⭕ **Tic-Tac-Toe** — play X vs O\n"
                "  🔢 **2048** — slide tiles to merge\n"
                "  🟩 **Wordle** — guess the 5-letter word\n"
                "  🧠 **Quiz** — trivia questions\n"
                "  ⌨️ **Typing Test** — test your speed\n\n"
                "Just type the game name to play!")
            return

        # ── open app / site ──
        if lo.startswith("open "):
            target = lo.split("open ", 1)[1]
            if target in config.apps:
                try:
                    os.startfile(config.apps[target])
                    self.add_bubble("Ghost", f"🖥️ Opening **{target}**…")
                except:
                    self.add_bubble("Ghost", f"❌ Could not open {target}.")
                return
            if target in config.websites:
                webbrowser.open(config.websites[target])
                self.add_bubble("Ghost", f"🌐 Opening **{target}**…")
                return

        # ── search ──
        if lo.startswith("search "):
            q = lo.split("search ", 1)[1]
            webbrowser.open(f"https://www.google.com/search?q={q}")
            self.add_bubble("Ghost", f"🔍 Searching for '**{q}**'…")
            return

        # ── system controls (direct, no AI needed) ──
        if any(kw in lo for kw in ["pause music", "play music", "resume music",
                                    "pause my music", "play my music", "resume my music",
                                    "play/pause", "play pause", "pause song", "play song",
                                    "media pause", "media play"]):
            import system_control
            system_control.media_play_pause()
            self.add_bubble("Ghost", "⏯️ Toggled media play/pause!")
            return

        if any(kw in lo for kw in ["next track", "next song", "skip song", "skip track"]):
            import system_control
            system_control.media_next()
            self.add_bubble("Ghost", "⏭️ Skipped to next track!")
            return

        if any(kw in lo for kw in ["previous track", "previous song", "prev song", "prev track"]):
            import system_control
            system_control.media_prev()
            self.add_bubble("Ghost", "⏮️ Went to previous track!")
            return

        if "mute" in lo and ("volume" in lo or "sound" in lo or lo.strip() == "mute"):
            import system_control
            system_control.mute_volume()
            self.add_bubble("Ghost", "🔇 System volume muted!")
            return

        volume_match = re.match(r'.*(?:set|change|make|put)?\s*(?:the\s+)?volume\s*(?:to|at)?\s*(\d+)\s*%?', lo)
        if volume_match:
            import system_control
            level = int(volume_match.group(1))
            system_control.set_volume(level / 100.0)
            self.add_bubble("Ghost", f"🔊 Volume set to **{level}%**!")
            return

        if any(kw in lo for kw in ["volume up", "increase volume", "louder"]):
            import system_control
            current = system_control.get_volume()
            system_control.set_volume(min(1.0, current + 0.1))
            self.add_bubble("Ghost", f"🔊 Volume increased to **{int(min(1.0, current + 0.1) * 100)}%**!")
            return

        if any(kw in lo for kw in ["volume down", "decrease volume", "quieter", "lower volume"]):
            import system_control
            current = system_control.get_volume()
            system_control.set_volume(max(0.0, current - 0.1))
            self.add_bubble("Ghost", f"🔉 Volume decreased to **{int(max(0.0, current - 0.1) * 100)}%**!")
            return

        if any(kw in lo for kw in ["lock screen", "lock my screen", "lock computer", "lock my computer", "lock pc", "lock my pc"]):
            import system_control
            self.add_bubble("Ghost", "🔒 Locking screen…")
            self.after(500, system_control.lock_screen)
            return

        # ── file search ──
        if lo.startswith("find "):
            query = lo.split("find ", 1)[1]
            self.status_left.configure(text=f"Searching for '{query}'…")
            self.update()
            results = utils.file_search(query)
            self.status_left.configure(text="Ready")
            if results:
                lines = []
                for f, size, root in results:
                    lines.append(f"📄 **{f}** ({size})\n   📁 `{root}`\n   *[CMD: open_folder | {root}]*")
                result_text = f"🔎 Found **{len(results)}** file(s):\n\n" + "\n\n".join(lines)
            else:
                result_text = f"🔎 No files found matching '**{query}**'"
            self.add_bubble("Ghost", result_text)
            return

        # ── weather ──
        if lo.startswith("weather in "):
            city = lo.split("weather in ", 1)[1]
            self.status_left.configure(text=f"Fetching weather for {city}…")
            self.add_bubble("Ghost", utils.fetch_weather(city))
            self.status_left.configure(text="Ready")
            return

        # ── reminder ──
        reminder_match = re.match(r'remind me in (\d+)\s*(min|minute|minutes|sec|second|seconds|s|m)?\s*(.*)', lo)
        if reminder_match:
            amount = int(reminder_match.group(1))
            unit = reminder_match.group(2) or "min"
            text = reminder_match.group(3) or "Time's up!"
            if unit.startswith("s"):
                delay_ms = amount * 1000
                unit_str = f"{amount} second(s)"
            else:
                delay_ms = amount * 60 * 1000
                unit_str = f"{amount} minute(s)"
            after_id = self.after(delay_ms, lambda t=text: self._fire_reminder(t))
            self.reminders.append((after_id, text))
            self.add_bubble("Ghost", f"⏰ Reminder set for **{unit_str}**: {text}")
            return

        # ── quote ──
        if lo in ("quote", "motivation", "motivate", "inspire"):
            self.add_bubble("Ghost", f"💡 _{random.choice(config.quotes)}_")
            return

        # ── joke ──
        if lo in ("joke", "tell me a joke"):
            self.add_bubble("Ghost", f"😄 {random.choice(config.jokes)}")
            return

        # ── fact ──
        if lo in ("fact", "tell me a fact", "random fact"):
            self.add_bubble("Ghost", f"🧠 {random.choice(config.facts)}")
            return

        # ── games ──
        if "snake" in lo:
            games.launch_snake(self)
            self.add_bubble("Ghost", "🐍 Launching Snake!")
            return
        if "tic" in lo:
            games.launch_tictactoe(self)
            self.add_bubble("Ghost", "⭕ Launching Tic‑Tac‑Toe!")
            return
        if "2048" in lo:
            games.launch_2048(self)
            self.add_bubble("Ghost", "🔢 Launching 2048!")
            return
        if "wordle" in lo:
            games.launch_wordle(self)
            self.add_bubble("Ghost", "🟩 Launching Wordle!")
            return
        if lo in ("quiz", "trivia"):
            games.launch_quiz(self)
            self.add_bubble("Ghost", "🧠 Launching Trivia Quiz!")
            return
        if "typing" in lo:
            games.launch_typing_test(self)
            self.add_bubble("Ghost", "⌨️ Launching Typing Speed Test!")
            return

        # ── code generator ──
        if lo in ("code", "codegen", "generate code", "code generator"):
            code_generator.launch_code_generator(self)
            self.add_bubble("Ghost", "💻 Opening Code Generator!")
            return

        # ── code explainer ──
        if lo.startswith("explain "):
            code = msg[8:]  # preserve original casing
            self.status_left.configure(text="Analyzing code…")
            label, bubble = self.add_bubble("Ghost", "●●●")
            buf = ["●●●"] if "●●●" == "" else [""]
            threading.Thread(
                target=ai_handler.code_explain_stream,
                args=(code, lambda c, f: self.after(0, self.stream_cb, c, f, label, buf, bubble)),
                daemon=True,
            ).start()
            return

        # ── date/time ──
        if lo in ("time", "date", "what time", "what's the time"):
            self.add_bubble("Ghost", f"🕐 It's **{datetime.now().strftime('%A, %d %B %Y — %H:%M')}**")
            return

        # ── calculator ──
        if any(op in lo for op in "+-*/%"):
            result = utils.safe_calculate(lo)
            if result is not None:
                self.add_bubble("Ghost", f"🧮 **{result}**")
                return

        # ── format converter prompt integration ──
        if self.uploaded_file and any(kw in lo for kw in ["convert", "format", "change to"]):
            self.status_left.configure(text="Converting file…")
            label, bubble = self.add_bubble("Ghost", "●●●")
            
            # Use ai stream callback style to update UI
            def _cb(chunk, done):
                if done:
                    self.status_left.configure(text="Ready")
                self.after(0, self.stream_cb, chunk, done, label, [""], bubble)
                
            format_converter.handle_prompt_conversion(self.uploaded_file, lo, _cb)
            
            # Clear upload after command
            self.uploaded_file = None
            self.msg_entry.configure(placeholder_text="Type a message, command, or ask anything…")
            self.btn_upload.configure(fg_color="transparent")
            return

        # ── AI fallback with streaming ──
        self.status_left.configure(text="Ghost is thinking…")
        label, bubble = self.add_bubble("Ghost", "●●●")
        buf = [""]
        threading.Thread(
            target=ai_handler.ai_reply_stream,
            args=(msg, lambda c, f: self.after(0, self.stream_cb, c, f, label, buf, bubble)),
            daemon=True,
        ).start()

    def _fire_reminder(self, text):
        """Called when a reminder timer fires."""
        self.add_bubble("Ghost", f"⏰ **Reminder:** {text}")
        self.deiconify()  # Bring window to front
        self.lift()
        self.focus_force()
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except:
            pass

    # ══════════════════════════ VOICE ══════════════════════════
    def toggle_voice(self):
        if not ai_handler.VOICE_INPUT_AVAILABLE:
            messagebox.showwarning("Unavailable", "Install SpeechRecognition + pyaudio.")
            return
        if self.is_listening:
            self.is_listening = False
            self.status_left.configure(text="Ready")
            self.apply_theme()
            return

        self.is_listening = True
        self.status_left.configure(text="🎤 Listening…")
        self.apply_theme()

        def _listen():
            while self.is_listening:
                text = ai_handler.listen_for_voice()
                if text and text not in ("unclear", "error"):
                    # aggressively strip hey ghost and punctuation from the start of the command
                    clean = re.sub(r'^(hey\s*ghost|hello\s*ghost)[\s,]*', '', text, flags=re.IGNORECASE).strip()
                    if clean:
                        self.after(0, lambda t=clean: [
                            self.msg_entry.delete(0, tk.END),
                            self.msg_entry.insert(0, t),
                            self.send_message(),
                        ])
                    if not config.settings["continuous_listening"]:
                        self.is_listening = False
                        self.after(0, lambda: [
                            self.status_left.configure(text="Ready"),
                            self.apply_theme(),
                        ])
                        break
                elif not config.settings["continuous_listening"]:
                    self.is_listening = False
                    self.after(0, lambda: [
                        self.status_left.configure(text="Ready"),
                        self.apply_theme(),
                    ])
                    break

        self.listening_thread = threading.Thread(target=_listen, daemon=True)
        self.listening_thread.start()

    # ══════════════════════════ THEME ══════════════════════════
    def cycle_theme(self):
        config.settings["theme_index"] = (config.settings["theme_index"] + 1) % len(config.themes)
        config.save_data()
        self.apply_theme()

    def toggle_tts(self):
        if ai_handler.engine:
            config.settings["tts_enabled"] = not config.settings["tts_enabled"]
            config.save_data()
            st = "enabled ✅" if config.settings["tts_enabled"] else "disabled 🔇"
            self.add_bubble("Ghost", f"🔊 Text‑to‑speech {st}")
        else:
            messagebox.showwarning("TTS", "TTS engine failed to load.")

    # ══════════════════════════ POMODORO ══════════════════════════
    def toggle_pomodoro(self):
        if self.pomodoro_running:
            self.pomodoro_running = False
            t = config.themes[config.settings["theme_index"]]
            self.pomo_btn.configure(text="▶  Start", fg_color=t["accent"])
        else:
            self.pomodoro_running = True
            self.pomo_btn.configure(text="⏸  Pause", fg_color=config.themes[config.settings["theme_index"]]["danger"])
            self._tick_pomo()

    def _tick_pomo(self):
        if self.pomodoro_running and self.pomodoro_time > 0:
            m, s = divmod(self.pomodoro_time, 60)
            self.pomo_display.configure(text=f"{m:02d} : {s:02d}")
            self.pomodoro_time -= 1
            self.after(1000, self._tick_pomo)
        elif self.pomodoro_time <= 0:
            self.pomo_display.configure(text="00 : 00")
            self.pomodoro_running = False
            self.reset_pomodoro()
            messagebox.showinfo("Focus Timer", "⏰ Time's up! Take a break. ☕")

    def reset_pomodoro(self):
        self.pomodoro_running = False
        self.pomodoro_time = 25 * 60
        self.pomo_display.configure(text="25 : 00")
        t = config.themes[config.settings["theme_index"]]
        self.pomo_btn.configure(text="▶  Start", fg_color=t["accent"])

    # ══════════════════════════ TASKS ══════════════════════════
    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter a new task:", parent=self)
        if task and task.strip():
            config.todo_list.append(task.strip())
            config.save_data()
            self.add_bubble("Ghost", f"✅ Task added: **{task.strip()}**")

    def view_tasks(self):
        if not config.todo_list:
            self.add_bubble("Ghost", "📋 Your to‑do list is empty.")
            return
        lines = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(config.todo_list))
        self.add_bubble("Ghost", f"📋 **Your Tasks:**\n{lines}")

    def delete_task(self):
        if not config.todo_list:
            return
        n = simpledialog.askinteger(
            "Delete Task", f"Enter task number (1‑{len(config.todo_list)}):", parent=self)
        if n and 1 <= n <= len(config.todo_list):
            removed = config.todo_list.pop(n - 1)
            config.save_data()
            self.add_bubble("Ghost", f"🗑️ Deleted: ~~{removed}~~")

    def clear_tasks(self):
        if config.todo_list and messagebox.askyesno("Clear All", "Delete all tasks?"):
            config.todo_list.clear()
            config.save_data()
            self.add_bubble("Ghost", "🗑️ All tasks cleared.")

    # ══════════════════════════ UTILITIES ══════════════════════════
    def handle_upload(self):
        if self.uploaded_file:
            # Click again to clear attachment
            self.uploaded_file = None
            self.msg_entry.configure(placeholder_text="Type a message, command, or ask anything…")
            self.btn_upload.configure(fg_color="transparent")
            self.add_bubble("Ghost", "📎 Attachment cleared.")
            return
            
        path = filedialog.askopenfilename(title="Select a file to attach")
        if path:
            self.uploaded_file = path
            filename = os.path.basename(path)
            self.msg_entry.configure(placeholder_text=f"Attached: {filename}")
            
            t = config.themes[config.settings["theme_index"]]
            self.btn_upload.configure(fg_color=t["accent"])
            
            self.add_bubble("You", f"📎 Attached file: `{filename}`", is_user=True)
            self.add_bubble("Ghost", f"I've attached **{filename}**! You can ask me to convert it by saying something like:\n- _\"Convert this to pdf\"_\n- _\"Change format to png\"_")
            
    def clear_chat(self):
        for w in self.chat_scroll.winfo_children():
            w.destroy()
        self.msg_count = 0
        self.status_right.configure(text="Messages: 0")
        self.add_bubble("Ghost", "💬 Chat cleared.")

    def take_screenshot(self):
        try:
            self.update()
            x, y = self.winfo_rootx(), self.winfo_rooty()
            img = ImageGrab.grab(bbox=(x, y, x + self.winfo_width(), y + self.winfo_height()))
            path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
            if path:
                img.save(path)
                self.add_bubble("Ghost", "📸 Screenshot saved!")
        except Exception as e:
            self.add_bubble("Ghost", f"⚠️ Screenshot failed: {e}")

    def export_chat(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt", initialfile="ghost_chat_export.txt",
            filetypes=[("Text", "*.txt"), ("Markdown", "*.md")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("# Ghost Chat Export\n")
                    f.write(f"# {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                    for entry in config.message_log:
                        f.write(f"[{entry['time']}] {entry['sender']}:\n{entry['text']}\n\n")
                self.add_bubble("Ghost", "💾 Chat exported!")
            except Exception as e:
                self.add_bubble("Ghost", f"⚠️ Export failed: {e}")

    def prompt_file_search(self):
        """Show a dialog to search for files."""
        query = simpledialog.askstring("File Search", "Enter filename to search for:", parent=self)
        if query and query.strip():
            self.msg_entry.delete(0, tk.END)
            self.msg_entry.insert(0, f"find {query.strip()}")
            self.send_message()

    # ══════════════════════════ SETTINGS ══════════════════════════
    def open_settings(self):
        t = config.themes[config.settings["theme_index"]]
        win = ctk.CTkToplevel(self)
        win.title("Settings")
        win.geometry("420x520")
        win.attributes("-topmost", True)
        win.configure(fg_color=t["bg"])

        ctk.CTkLabel(
            win, text="⚙️  Settings",
            font=("Segoe UI Semibold", 20), text_color=t["accent"],
        ).pack(pady=(24, 16))

        # ── Switches ──
        def _switch(parent, label, key):
            fr = ctk.CTkFrame(parent, fg_color="transparent")
            fr.pack(fill="x", padx=24, pady=6)
            ctk.CTkLabel(fr, text=label, font=("Segoe UI", 13), text_color=t["fg"]).pack(side="left")
            var = ctk.BooleanVar(value=config.settings[key])

            def cb():
                config.settings[key] = var.get()
                config.save_data()
                if key == "quick_replies_visible":
                    if var.get():
                        self.qr_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=4)
                        self._build_quick_replies()
                    else:
                        self.qr_frame.grid_forget()

            ctk.CTkSwitch(fr, text="", variable=var, command=cb, width=44).pack(side="right")

        _switch(win, "Text‑to‑Speech", "tts_enabled")
        _switch(win, "Quick Replies", "quick_replies_visible")
        _switch(win, "Continuous Listening", "continuous_listening")
        _switch(win, "Auto‑scroll", "auto_scroll")
        _switch(win, "Animations", "animations_enabled")

        # ── Sliders ──
        def _slider(parent, label, key, lo, hi, res):
            fr = ctk.CTkFrame(parent, fg_color="transparent")
            fr.pack(fill="x", padx=24, pady=6)
            lbl = ctk.CTkLabel(fr, text=f"{label}: {config.settings[key]}", font=("Segoe UI", 13), text_color=t["fg"])
            lbl.pack(anchor="w")

            def cb(val):
                config.settings[key] = int(float(val)) if isinstance(config.settings[key], int) else float(val)
                lbl.configure(text=f"{label}: {config.settings[key]}")
                config.save_data()

            ctk.CTkSlider(fr, from_=lo, to=hi, number_of_steps=int((hi - lo) / res),
                          command=cb).pack(fill="x", pady=2)

        _slider(win, "Font Size", "font_size", 10, 18, 1)
        _slider(win, "TTS Speed", "tts_rate", 100, 250, 10)

        # ── Danger zone ──
        ctk.CTkButton(
            win, text="🧹  Clear AI Memory", fg_color=t["danger"],
            hover_color="#c82333", text_color="#fff",
            command=lambda: [ai_handler.clear_memory(), messagebox.showinfo("Done", "AI memory cleared.")],
        ).pack(pady=(20, 8))

        ctk.CTkButton(
            win, text="Close", fg_color=t["btn"], hover_color=t["btn_hover"],
            text_color=t["fg"], command=win.destroy,
        ).pack(pady=8)

    # ══════════════════════════ LIFECYCLE ══════════════════════════
    def on_closing(self):
        config.save_data()
        self.quit()


if __name__ == "__main__":
    app = GhostChatApp()
    app.mainloop()
