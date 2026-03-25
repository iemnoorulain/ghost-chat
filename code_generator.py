import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import config
import ai_handler


# Language options with file extensions
LANGUAGES = [
    ("Python", ".py"),
    ("JavaScript", ".js"),
    ("HTML", ".html"),
    ("CSS", ".css"),
    ("Java", ".java"),
    ("C++", ".cpp"),
    ("C#", ".cs"),
    ("C", ".c"),
    ("TypeScript", ".ts"),
    ("Go", ".go"),
    ("Rust", ".rs"),
    ("Ruby", ".rb"),
    ("PHP", ".php"),
    ("Swift", ".swift"),
    ("Kotlin", ".kt"),
    ("SQL", ".sql"),
    ("Bash / Shell", ".sh"),
    ("PowerShell", ".ps1"),
    ("Lua", ".lua"),
    ("R", ".r"),
]


def launch_code_generator(root):
    t = config.themes[config.settings["theme_index"]]

    win = ctk.CTkToplevel(root)
    win.title("💻 Code Generator")
    win.geometry("800x700")
    win.minsize(700, 550)
    win.configure(fg_color=t["bg"])
    win.attributes("-topmost", True)

    generating = [False]

    # ══════════════════════ HEADER ══════════════════════
    header = ctk.CTkFrame(win, fg_color=t["sidebar"], height=50, corner_radius=0)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="💻  Code Generator", font=("Segoe UI", 18, "bold"),
                 text_color=t["accent"]).pack(side="left", padx=20, pady=12)

    status_label = ctk.CTkLabel(header, text="Ready", font=("Segoe UI", 11),
                                text_color=t["muted"])
    status_label.pack(side="right", padx=20)

    # ══════════════════════ TOP CONTROLS ══════════════════════
    controls = ctk.CTkFrame(win, fg_color="transparent")
    controls.pack(fill="x", padx=20, pady=(14, 6))

    # Language selector
    lang_frame = ctk.CTkFrame(controls, fg_color="transparent")
    lang_frame.pack(side="left")
    ctk.CTkLabel(lang_frame, text="Language:", font=("Segoe UI", 12, "bold"),
                 text_color=t["fg"]).pack(side="left", padx=(0, 8))

    lang_names = [l[0] for l in LANGUAGES]
    lang_var = ctk.StringVar(value="Python")
    lang_dropdown = ctk.CTkOptionMenu(
        lang_frame, values=lang_names, variable=lang_var,
        width=160, height=32, corner_radius=8,
        fg_color=t["btn"], button_color=t["accent"],
        button_hover_color=t["accent_hover"],
        dropdown_fg_color=t["card"], dropdown_hover_color=t["sidebar_hover"],
        text_color=t["fg"], font=("Segoe UI", 12),
    )
    lang_dropdown.pack(side="left")

    # Generate button
    generate_btn = ctk.CTkButton(
        controls, text="⚡ Generate", height=34, width=130,
        corner_radius=10, font=("Segoe UI", 13, "bold"),
        fg_color=t["accent"], hover_color=t["accent_hover"], text_color="#fff",
        command=lambda: start_generate(),
    )
    generate_btn.pack(side="right", padx=(8, 0))

    # Clear button
    clear_btn = ctk.CTkButton(
        controls, text="🗑️ Clear", height=34, width=90,
        corner_radius=10, font=("Segoe UI", 12),
        fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"],
        command=lambda: clear_all(),
    )
    clear_btn.pack(side="right", padx=(8, 0))

    # ══════════════════════ PROMPT INPUT ══════════════════════
    prompt_label = ctk.CTkLabel(win, text="📝  Describe the code you want:",
                                font=("Segoe UI", 12, "bold"), text_color=t["fg"])
    prompt_label.pack(anchor="w", padx=22, pady=(10, 4))

    prompt_box = ctk.CTkTextbox(
        win, height=100, corner_radius=10,
        fg_color=t["input_bg"], text_color=t["fg"],
        border_color=t["input_border"], border_width=2,
        font=("Segoe UI", 13),
        wrap="word",
    )
    prompt_box.pack(fill="x", padx=20, pady=(0, 8))

    # Placeholder hint
    prompt_box.insert("1.0", "e.g. Create a function that sorts a list using quicksort algorithm")
    prompt_box.configure(text_color=t["muted"])

    def on_prompt_focus_in(e):
        current = prompt_box.get("1.0", "end-1c")
        if current.startswith("e.g."):
            prompt_box.delete("1.0", "end")
            prompt_box.configure(text_color=t["fg"])

    def on_prompt_focus_out(e):
        current = prompt_box.get("1.0", "end-1c").strip()
        if not current:
            prompt_box.insert("1.0", "e.g. Create a function that sorts a list using quicksort algorithm")
            prompt_box.configure(text_color=t["muted"])

    prompt_box.bind("<FocusIn>", on_prompt_focus_in)
    prompt_box.bind("<FocusOut>", on_prompt_focus_out)

    # ══════════════════════ OUTPUT AREA ══════════════════════
    output_header = ctk.CTkFrame(win, fg_color="transparent")
    output_header.pack(fill="x", padx=22, pady=(4, 4))

    ctk.CTkLabel(output_header, text="📄  Generated Code:",
                 font=("Segoe UI", 12, "bold"), text_color=t["fg"]).pack(side="left")

    # Action buttons for the output
    btn_row = ctk.CTkFrame(output_header, fg_color="transparent")
    btn_row.pack(side="right")

    copy_btn = ctk.CTkButton(
        btn_row, text="📋 Copy", height=28, width=80,
        corner_radius=8, font=("Segoe UI", 11),
        fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"],
        command=lambda: copy_code(),
    )
    copy_btn.pack(side="left", padx=3)

    save_btn = ctk.CTkButton(
        btn_row, text="💾 Save", height=28, width=80,
        corner_radius=8, font=("Segoe UI", 11),
        fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"],
        command=lambda: save_code(),
    )
    save_btn.pack(side="left", padx=3)

    code_output = ctk.CTkTextbox(
        win, corner_radius=10,
        fg_color=t["card"], text_color=t.get("success", "#22c55e"),
        border_color=t["input_border"], border_width=2,
        font=("Consolas", 13),
        wrap="word",
    )
    code_output.pack(fill="both", expand=True, padx=20, pady=(0, 8))

    # ══════════════════════ BOTTOM BAR ══════════════════════
    bottom = ctk.CTkFrame(win, fg_color=t["sidebar"], height=36, corner_radius=0)
    bottom.pack(fill="x", side="bottom")

    char_count = ctk.CTkLabel(bottom, text="0 characters", font=("Segoe UI", 10),
                              text_color=t["muted"])
    char_count.pack(side="left", padx=14, pady=6)

    line_count = ctk.CTkLabel(bottom, text="0 lines", font=("Segoe UI", 10),
                              text_color=t["muted"])
    line_count.pack(side="right", padx=14, pady=6)

    # ══════════════════════ FUNCTIONS ══════════════════════

    def update_counts():
        code = code_output.get("1.0", "end-1c")
        chars = len(code)
        lines = code.count("\n") + 1 if code.strip() else 0
        char_count.configure(text=f"{chars} characters")
        line_count.configure(text=f"{lines} lines")

    def copy_code():
        code = code_output.get("1.0", "end-1c")
        if code.strip():
            win.clipboard_clear()
            win.clipboard_append(code)
            status_label.configure(text="✅ Copied to clipboard!", text_color=t.get("success", "#22c55e"))
            win.after(2000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))
        else:
            status_label.configure(text="Nothing to copy", text_color=t.get("warning", "#fbbf24"))
            win.after(2000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))

    def save_code():
        code = code_output.get("1.0", "end-1c")
        if not code.strip():
            status_label.configure(text="Nothing to save", text_color=t.get("warning", "#fbbf24"))
            win.after(2000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))
            return

        # Get the correct file extension
        lang = lang_var.get()
        ext = ".txt"
        for name, e in LANGUAGES:
            if name == lang:
                ext = e
                break

        path = filedialog.asksaveasfilename(
            defaultextension=ext,
            initialfile=f"generated_code{ext}",
            filetypes=[(f"{lang} files", f"*{ext}"), ("All files", "*.*")],
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(code)
                status_label.configure(text=f"✅ Saved to {path}", text_color=t.get("success", "#22c55e"))
                win.after(3000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))
            except Exception as e:
                status_label.configure(text=f"⚠️ Save failed: {e}", text_color=t.get("danger", "#f87171"))

    def clear_all():
        prompt_box.delete("1.0", "end")
        code_output.configure(state="normal")
        code_output.delete("1.0", "end")
        update_counts()
        status_label.configure(text="Ready", text_color=t["muted"])
        on_prompt_focus_out(None)

    def start_generate():
        if generating[0]:
            return

        prompt = prompt_box.get("1.0", "end-1c").strip()
        if not prompt or prompt.startswith("e.g."):
            status_label.configure(text="⚠️ Enter a prompt first!", text_color=t.get("warning", "#fbbf24"))
            win.after(2000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))
            return

        generating[0] = True
        language = lang_var.get()

        # Clear output
        code_output.configure(state="normal")
        code_output.delete("1.0", "end")
        update_counts()

        # Update UI state
        generate_btn.configure(text="⏳ Generating...", state="disabled",
                               fg_color=t["btn"])
        status_label.configure(text=f"Generating {language} code...", text_color=t["accent"])

        def stream_callback(chunk, is_done):
            """ Called from the AI thread — schedule UI update on main thread """
            win.after(0, lambda: _handle_stream(chunk, is_done))

        def _handle_stream(chunk, is_done):
            if not is_done:
                code_output.insert("end", chunk)
                code_output.see("end")
                update_counts()
            else:
                if chunk:  # Error message
                    code_output.insert("end", chunk)
                generating[0] = False
                generate_btn.configure(text="⚡ Generate", state="normal",
                                       fg_color=t["accent"])
                status_label.configure(text="✅ Done!", text_color=t.get("success", "#22c55e"))
                update_counts()
                win.after(3000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))

        threading.Thread(
            target=ai_handler.code_generate_stream,
            args=(prompt, language, stream_callback),
            daemon=True,
        ).start()

    # Bind Ctrl+Enter to generate
    def on_ctrl_enter(e):
        start_generate()
        return "break"

    prompt_box.bind("<Control-Return>", on_ctrl_enter)
    win.after(100, lambda: prompt_box.focus())
