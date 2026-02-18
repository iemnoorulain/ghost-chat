# ---- AI (Ollama) ----
try:
    import ollama
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import webbrowser
import random
import os
import re
from datetime import datetime
from PIL import Image, ImageGrab
import pyttsx3
import json
import threading

# Voice Recognition imports
try:
    import speech_recognition as sr
    VOICE_INPUT_AVAILABLE = True
except ImportError:
    VOICE_INPUT_AVAILABLE = False
    print("speech_recognition not installed. Voice input will be disabled.")
    print("Install with: pip install SpeechRecognition pyaudio")

# ----------------------- Data -----------------------
jokes = [
    "Why did the computer show up at work late? It had a hard drive!",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "What do you call 8 hobbits? A hobbyte.",
    "Why did the developer go broke? Because he used up all his cache!",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
    "Why do Java developers wear glasses? Because they can't C#!",
    "I would tell you a UDP joke, but you might not get it.",
    "There are only 10 types of people in the world: those who understand binary and those who don't.",
    "Why did the programmer quit his job? Because he didn't get arrays.",
    "Why was the cell phone wearing glasses? It lost its contacts.",
    "Why did the computer go to therapy? It had too many bytes of anxiety.",
    "Why don't robots ever get scared? They have nerves of steel.",
    "What did the router say to the doctor? 'It hurts when IP.'",
    "Why do programmers hate nature? Too many bugs.",
    "How does a developer announce their engagement? They git commit.",
    "What's a programmer's favorite hangout place? The Foo Bar.",
    "Why was the math book sad? It had too many problems.",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Why don't scientists trust atoms? Because they make up everything.",
    "What do you call fake spaghetti? An impasta.",
    "Why did the tomato turn red? Because it saw the salad dressing.",
    "Why did the coffee file a police report? It got mugged.",
    "What did one ocean say to the other ocean? Nothing, they just waved.",
    "Why was the computer cold? It left its Windows open.",
    "How do you comfort a JavaScript bug? You console it.",
    "Why did the programmer bring a ladder? To reach the high-level language.",
    "Why was the equal sign so humble? Because it realized it wasn't greater or less than anyone else.",
    "Why did the bicycle fall over? It was two-tired.",
    "Why are ghosts bad at lying? Because you can see right through them.",
    "Why did the cookie go to the doctor? It felt crummy.",
    "Why don't programmers like to go outside? The sunlight causes too many glares on their screens.",
    "Why did the physics teacher break up with the biology teacher? There was no chemistry.",
    "Why do cows have hooves instead of feet? Because they lactose.",
    "Why did the computer cross the road? To get to the other site.",
    "What do you call a belt made of watches? A waist of time.",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "Why was the stadium so cool? It was filled with fans.",
    "What did the janitor say when he jumped out of the closet? 'Supplies!'",
    "Why did the cookie cry? Because his mom was a wafer so long.",
    "Why couldn't the leopard play hide and seek? Because he was always spotted.",
    "Why did the computer keep sneezing? It had a bad case of the 'flu'shes (flushes).",
    "How does a penguin build its house? Igloos it together.",
    "Why was six afraid of seven? Because seven eight (ate) nine.",
    "Why don't eggs tell jokes? They'd crack each other up.",
    "What do you call a dinosaur with an extensive vocabulary? A thesaurus.",
    "Why did the scarecrow become a successful neurosurgeon? He was outstanding in his field of study." 
]

facts = [
    "Honey never spoils – archaeologists have eaten 3000-year-old honey and it was still edible.",
    "Bananas are berries, but strawberries aren't.",
    "Octopuses have three hearts.",
    "A group of flamingos is called a 'flamboyance'.",
    "Sharks existed before trees.",
    "The Eiffel Tower can be 15 cm taller during summer due to thermal expansion.",
    "Venus is the only planet that rotates clockwise.",
    "Hot water can freeze faster than cold water under certain conditions (the Mpemba effect).",
    "There are more possible iterations of a game of chess than atoms in the known universe.",
    "Wombat poop is cube-shaped.",
    "A day on Venus is longer than a year on Venus.",
    "Cleopatra lived closer in time to the Moon landing than to the building of the Great Pyramid.",
    "A single strand of spaghetti is called a 'spaghetto'.",
    "Koalas have fingerprints that are almost indistinguishable from human fingerprints.",
    "The longest recorded flight of a chicken is 13 seconds.",
    "Some metals, like potassium, react explosively with water.",
    "The world's deepest postbox is in Susami Bay, Japan – 10 metres underwater.",
    "There are more trees on Earth than stars in the Milky Way galaxy's visible disk.",
    "Oxford University is older than the Aztec Empire.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
    "The inventor of the Pringles can is buried in one.",
    "Rabbits can't vomit.",
    "Scotland's national animal is the unicorn.",
    "A blue whale's heart is about the size of a small car.",
    "Some turtles can breathe through their butts (cloacal respiration).",
    "The world's smallest reptile was only discovered in 2021 and can fit on a fingernail.",
    "The human nose can detect at least one trillion different scents.",
    "Venus flytraps can count – they need two trigger hairs touched to close.",
    "Oxford Dictionary added over 1,000 new words in a single update in recent years.",
    "There are more microorganisms in a teaspoon of soil than people on Earth.",
    "The Pacific Ocean is wider than the moon's diameter.",
    "Alaska is the state with the westernmost and easternmost points in the US (due to Aleutian Islands crossing the 180th meridian).",
    "The first computer 'bug' was an actual moth stuck in a Harvard Mark II computer.",
    "A full NASA space suit costs around $12 million.",
    "The mantis shrimp can see polarized light and has 16 types of color receptors (humans have 3).",
    "Cleopatra was Greek – descended from Ptolemy, one of Alexander the Great's generals.",
    "The Great Wall of China is not visible from the Moon with the naked eye.",
    "There are more stars in the universe than grains of sand on all Earth's beaches.",
    "Some lizards can squirt blood from their eyes as a defense.",
    "Tomatoes were once thought to be poisonous by many Europeans.",
    "The shortest war in history was between Britain and Zanzibar in 1896 and lasted 38 minutes.",
    "A single teaspoon of honey represents the life's work of 12 bees.",
    "Saturn's density is less than water – it would float if you had a big enough bathtub.",
    "The world's oldest known 'your mom' joke is 3,500 years old (found on a Babylonian tablet).",
    "Mammoths were still alive when the Great Pyramid was being built.",
    "The heart of a shrimp is located in its head.",
    "Space is not completely empty – it contains about one atom per cubic centimeter on average.",
    "The fingerprint patterns of koalas are so similar to humans that they can taint crime scenes.",
    "The Sahara was once a lush, green region with lakes and grasslands.",
    "Peanuts are not nuts; they are legumes.",
    "The world's largest organism is a fungus in Oregon covering over 2,000 acres." 
]

apps = {
    "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "notepad": "notepad.exe",
    "cmd": "cmd.exe",
    "camera": "microsoft.windows.camera:",
    "calculator": "calc.exe",
    "paint": "mspaint.exe"
}

websites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "github": "https://www.github.com",
    "reddit": "https://www.reddit.com"
}

game_scores = {"snake": 0, "tic_tac_toe": {"X": 0, "O": 0}}
personalities = ["Funny", "Serious", "Sarcastic"]
current_personality = ["Funny"]

# Settings
settings = {
    "tts_enabled": True,
    "quick_replies_visible": True,
    "animations_enabled": True,
    "font_size": 11,
    "auto_scroll": True,
    "sound_enabled": False,
    "voice_input_enabled": True,
    "continuous_listening": False,
    "tts_rate": 150,
    "tts_volume": 1.0,
    "voice_language": "en-US"
}

# Themes
themes = [
    {
        "name": "Dark Matrix",
        "bg": "#0d1117", 
        "fg": "#c9d1d9",
        "sidebar": "#161b22",
        "btn": "#21262d",
        "btn_hover": "#30363d",
        "msg_user_bg": "#1f6feb",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#238636",
        "msg_ghost_fg": "#ffffff",
        "accent": "#58a6ff",
        "input_bg": "#0d1117",
        "input_border": "#30363d"
    },
    {
        "name": "Light Modern",
        "bg": "#ffffff",
        "fg": "#1f2328",
        "sidebar": "#f6f8fa",
        "btn": "#f6f8fa",
        "btn_hover": "#e8eaed",
        "msg_user_bg": "#0969da",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#1a7f37",
        "msg_ghost_fg": "#ffffff",
        "accent": "#0969da",
        "input_bg": "#ffffff",
        "input_border": "#d0d7de"
    },
    {
        "name": "Ocean Blue",
        "bg": "#0a1929",
        "fg": "#b2bac2",
        "sidebar": "#001e3c",
        "btn": "#003768",
        "btn_hover": "#004c99",
        "msg_user_bg": "#0288d1",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#00acc1",
        "msg_ghost_fg": "#ffffff",
        "accent": "#29b6f6",
        "input_bg": "#0a1929",
        "input_border": "#003768"
    },
    {
        "name": "Purple Haze",
        "bg": "#1a0033",
        "fg": "#e1bee7",
        "sidebar": "#2d0052",
        "btn": "#4a148c",
        "btn_hover": "#6a1b9a",
        "msg_user_bg": "#7b1fa2",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#ab47bc",
        "msg_ghost_fg": "#ffffff",
        "accent": "#ce93d8",
        "input_bg": "#1a0033",
        "input_border": "#4a148c"
    },
    {
        "name": "Sunset Orange",
        "bg": "#1a1a1a",
        "fg": "#ffccbc",
        "sidebar": "#2d1b14",
        "btn": "#bf360c",
        "btn_hover": "#d84315",
        "msg_user_bg": "#ff5722",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#ff9800",
        "msg_ghost_fg": "#000000",
        "accent": "#ffab40",
        "input_bg": "#1a1a1a",
        "input_border": "#bf360c"
    }
]
theme_index = [0]

# Quick replies
quick_replies = [
    {"text": "😄 Tell a joke", "command": "joke"},
    {"text": "🧠 Random fact", "command": "fact"},
    {"text": "🐍 Play Snake", "command": "snake"},
    {"text": "⌛⭕ Tic-Tac-Toe", "command": "tic-tac-toe"},
    {"text": "🔍 Search Google", "command": "search "},
    {"text": "❓ Help", "command": "help"}
]

# Initialize text-to-speech
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', settings["tts_rate"])
    engine.setProperty('volume', settings["tts_volume"])
except:
    engine = None
    settings["tts_enabled"] = False

# Initialize speech recognition
if VOICE_INPUT_AVAILABLE:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    recognizer.dynamic_energy_threshold = True
else:
    recognizer = None

todo_list = []
message_history = []
is_listening = [False]
listening_thread = [None]
# AI chat history for better conversations
ai_history = []

# ----------------------- Data Persistence -----------------------
def load_data():
    try:
        if os.path.exists("ghost_chat_data.json"):
            with open("ghost_chat_data.json", "r") as f:
                data = json.load(f)
                game_scores["snake"] = data.get("snake_score", 0)
                game_scores["tic_tac_toe"] = data.get("ttt_scores", {"X": 0, "O": 0})
                todo_list.extend(data.get("todo_list", []))
                theme_index[0] = data.get("theme", 0)
                current_personality[0] = data.get("personality", "Funny")
                settings.update(data.get("settings", {}))
    except Exception as e:
        print(f"Could not load data: {e}")

def save_data():
    try:
        data = {
            "snake_score": game_scores["snake"],
            "ttt_scores": game_scores["tic_tac_toe"],
            "todo_list": todo_list,
            "theme": theme_index[0],
            "personality": current_personality[0],
            "settings": settings
        }
        with open("ghost_chat_data.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Could not save data: {e}")

# ----------------------- Safe Math Calculator -----------------------
def safe_calculate(expression):
    try:
        expression = expression.replace(" ", "")
        if not re.match(r'^[0-9+\-*/().%\s]+$', expression):
            return None
        if "__" in expression or "import" in expression:
            return None
        expression = expression.replace("^", "**")
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except:
        return None

# ----------------------- Voice Assistant Functions -----------------------
def speak_text(text):
    """Speak text using TTS in a separate thread"""
    if settings["tts_enabled"] and engine:
        def speak_thread():
            try:
                engine.setProperty('rate', settings["tts_rate"])
                engine.setProperty('volume', settings["tts_volume"])
                engine.say(text)
                engine.runAndWait()
            except:
                pass
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()

def listen_for_voice():
    """Listen for voice input and return recognized text"""
    if not VOICE_INPUT_AVAILABLE or not settings["voice_input_enabled"]:
        return None
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language=settings["voice_language"])
            return text
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return "unclear"
    except sr.RequestError:
        return "error"
    except Exception as e:
        print(f"Voice recognition error: {e}")
        return None

def start_voice_input():
    """Start listening for voice input"""
    if not VOICE_INPUT_AVAILABLE:
        messagebox.showwarning("Voice Input Unavailable", 
            "Voice input requires 'speech_recognition' package.\n\n"
             "Install with: pip install SpeechRecognition pyaudio")
        return
    
    if is_listening[0]:
        stop_voice_input()
        return
    
    is_listening[0] = True
    update_voice_button_state()
    
    def listen_thread():
        while is_listening[0]:
            # Show listening indicator
            root.after(0, lambda: voice_status_label.config(
                text="🎤 Listening...", 
                fg=themes[theme_index[0]]["accent"]))
            
            result = listen_for_voice()
            
            if result and result not in ["unclear", "error"]:
                root.after(0, lambda t=result: [
                    msg_entry.delete(0, tk.END),
                    msg_entry.insert(0, t),
                    voice_status_label.config(text="✅ Recognized", 
                        fg="#28a745")
                ])
                
                if settings["continuous_listening"]:
                    root.after(0, lambda: send_message())
                else:
                    is_listening[0] = False
                    root.after(0, update_voice_button_state)
                
                root.after(2000, lambda: voice_status_label.config(text=""))
                
            elif result == "unclear":
                root.after(0, lambda: [
                    voice_status_label.config(text="❌ Couldn't understand", 
                        fg="#dc3545"),
                    root.after(2000, lambda: voice_status_label.config(text=""))
                ])
                if not settings["continuous_listening"]:
                    is_listening[0] = False
                    root.after(0, update_voice_button_state)
                    
            elif result == "error":
                root.after(0, lambda: [
                    voice_status_label.config(text="⚠️ Connection error", 
                        fg="#ffc107"),
                    root.after(2000, lambda: voice_status_label.config(text=""))
                ])
                is_listening[0] = False
                root.after(0, update_voice_button_state)
                break
            
            if not settings["continuous_listening"]:
                is_listening[0] = False
                root.after(0, update_voice_button_state)
                break
    
    listening_thread[0] = threading.Thread(target=listen_thread, daemon=True)
    listening_thread[0].start()

def stop_voice_input():
    """Stop listening for voice input"""
    is_listening[0] = False
    update_voice_button_state()
    voice_status_label.config(text="")

def update_voice_button_state():
    """Update the voice button appearance based on listening state"""
    if is_listening[0]:
        voice_button.config(
            text="⏹️ Stop",
            bg="#dc3545",
            activebackground="#c82333"
        )
    else:
        voice_button.config(
            text="🎤 Voice",
            bg=themes[theme_index[0]]["btn"],
            activebackground=themes[theme_index[0]]["btn_hover"]
        )

# ----------------------- Root -----------------------
root = tk.Tk()
root.title("👻 Ghost Chat - Voice Assistant")
root.geometry("1100x750")
root.minsize(900, 600)

load_data()
root.configure(bg=themes[theme_index[0]]["bg"])

def on_closing():
    stop_voice_input()
    save_data()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# ----------------------- Settings Panel -----------------------
def open_settings():
    settings_win = tk.Toplevel(root)
    settings_win.title("⚙️ Settings")
    settings_win.geometry("500x650")
    settings_win.resizable(False, False)
    settings_win.configure(bg=themes[theme_index[0]]["bg"])
    
    header = tk.Frame(settings_win, bg=themes[theme_index[0]]["sidebar"], height=70)
    header.pack(fill="x")
    header.pack_propagate(False)
    
    title = tk.Label(header, text="⚙️ Settings", 
                    font=("Segoe UI", 18, "bold"),
                    bg=themes[theme_index[0]]["sidebar"],
                    fg=themes[theme_index[0]]["accent"])
    title.pack(pady=20)
    
    canvas = tk.Canvas(settings_win, bg=themes[theme_index[0]]["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(settings_win, orient="vertical", command=canvas.yview)
    content_frame = tk.Frame(canvas, bg=themes[theme_index[0]]["bg"])
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    scrollbar.pack(side="right", fill="y")
    
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def add_section(title_text):
        label = tk.Label(content_frame, text=title_text,
                        font=("Segoe UI", 12, "bold"),
                        bg=themes[theme_index[0]]["bg"],
                        fg=themes[theme_index[0]]["accent"],
                        anchor="w")
        label.pack(fill="x", pady=(20, 10))
    
    def add_toggle(text, key):
        frame = tk.Frame(content_frame, bg=themes[theme_index[0]]["bg"])
        frame.pack(fill="x", pady=5)
        
        label = tk.Label(frame, text=text,
                        font=("Segoe UI", 11),
                        bg=themes[theme_index[0]]["bg"],
                        fg=themes[theme_index[0]]["fg"],
                        anchor="w")
        label.pack(side="left")
        
        var = tk.BooleanVar(value=settings[key])
        
        def toggle():
            settings[key] = var.get()
            save_data()
            if key == "quick_replies_visible":
                update_quick_replies()
        
        check = tk.Checkbutton(frame, variable=var, command=toggle,
                              bg=themes[theme_index[0]]["bg"],
                              fg=themes[theme_index[0]]["accent"],
                              selectcolor=themes[theme_index[0]]["btn"],
                              activebackground=themes[theme_index[0]]["bg"])
        check.pack(side="right")
    
    def add_slider(text, key, from_, to):
        frame = tk.Frame(content_frame, bg=themes[theme_index[0]]["bg"])
        frame.pack(fill="x", pady=10)
        
        label = tk.Label(frame, text=f"{text}: {settings[key]}",
                        font=("Segoe UI", 11),
                        bg=themes[theme_index[0]]["bg"],
                        fg=themes[theme_index[0]]["fg"],
                        anchor="w")
        label.pack(fill="x")
        
        def on_change(val):
            settings[key] = int(float(val)) if isinstance(settings[key], int) else float(val)
            label.config(text=f"{text}: {settings[key]}")
            if key == "tts_rate" and engine:
                engine.setProperty('rate', settings[key])
            elif key == "tts_volume" and engine:
                engine.setProperty('volume', settings[key])
            save_data()
        
        slider = tk.Scale(frame, from_=from_, to=to, orient="horizontal",
                         command=on_change, resolution=0.1 if key == "tts_volume" else 1,
                         bg=themes[theme_index[0]]["btn"],
                         fg=themes[theme_index[0]]["fg"],
                         highlightthickness=0,
                         troughcolor=themes[theme_index[0]]["bg"])
        slider.set(settings[key])
        slider.pack(fill="x", pady=5)
    
    add_section("🎤 Voice Input")
    add_toggle("Enable Voice Input", "voice_input_enabled")
    add_toggle("Continuous Listening Mode", "continuous_listening")
    
    add_section("🔊 Audio Settings")
    add_toggle("Enable Text-to-Speech", "tts_enabled")
    add_toggle("Enable Sound Effects", "sound_enabled")
    add_slider("Speech Rate", "tts_rate", 100, 250)
    add_slider("Speech Volume", "tts_volume", 0.0, 1.0)
    
    add_section("🎨 Interface Settings")
    add_toggle("Show Quick Reply Buttons", "quick_replies_visible")
    add_toggle("Enable Animations", "animations_enabled")
    add_toggle("Auto-scroll to Latest Message", "auto_scroll")
    add_slider("Chat Font Size", "font_size", 9, 16)
    
    add_section("💾 Data Management")
    
    def export_settings():
        file_path = filedialog.asksaveasfilename(
            title="Export Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump({
                        "theme": theme_index[0],
                        "personality": current_personality[0],
                        "settings": settings
                    }, f, indent=2)
                messagebox.showinfo("Success", "Settings exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
    
    def import_settings():
        file_path = filedialog.askopenfilename(
            title="Import Settings",
            filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    theme_index[0] = data.get("theme", 0)
                    current_personality[0] = data.get("personality", "Funny")
                    settings.update(data.get("settings", {}))
                    save_data()
                    apply_theme()
                messagebox.showinfo("Success", "Settings imported!")
                settings_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import: {e}")
    
    btn_frame = tk.Frame(content_frame, bg=themes[theme_index[0]]["bg"])
    btn_frame.pack(fill="x", pady=10)
    
    export_btn = tk.Button(btn_frame, text="📤 Export",
                          command=export_settings,
                          bg=themes[theme_index[0]]["btn"],
                          fg=themes[theme_index[0]]["fg"],
                          font=("Segoe UI", 10),
                          relief="flat", padx=15, pady=8)
    export_btn.pack(side="left", padx=5)
    
    import_btn = tk.Button(btn_frame, text="📥 Import",
                          command=import_settings,
                          bg=themes[theme_index[0]]["btn"],
                          fg=themes[theme_index[0]]["fg"],
                          font=("Segoe UI", 10),
                          relief="flat", padx=15, pady=8)
    import_btn.pack(side="left", padx=5)
    
    add_section("ℹ️ About")
    about_text = "Ghost Chat v2.1 - Voice Assistant\nBuilt with Python & Tkinter\n© 2025"
    about_label = tk.Label(content_frame, text=about_text,
                          font=("Segoe UI", 10),
                          bg=themes[theme_index[0]]["bg"],
                          fg=themes[theme_index[0]]["fg"])
    about_label.pack(fill="x", pady=10)
    
    close_btn = tk.Button(content_frame, text="✓ Close",
                         command=settings_win.destroy,
                         bg=themes[theme_index[0]]["accent"],
                         fg="#ffffff",
                         font=("Segoe UI", 11, "bold"),
                         relief="flat", padx=20, pady=10)
    close_btn.pack(pady=20)

# ----------------------- Header -----------------------
header_frame = tk.Frame(root, bg=themes[theme_index[0]]["sidebar"], height=70)
header_frame.pack(side="top", fill="x")
header_frame.pack_propagate(False)

left_header = tk.Frame(header_frame, bg=themes[theme_index[0]]["sidebar"])
left_header.pack(side="left", fill="y", padx=20)

header_label = tk.Label(left_header, text="👻 Ghost Chat", 
                        font=("Segoe UI", 20, "bold"), 
                        bg=themes[theme_index[0]]["sidebar"], 
                        fg=themes[theme_index[0]]["accent"])
header_label.pack(side="left", pady=15)

version_label = tk.Label(left_header, text="v2.1", 
                        font=("Segoe UI", 9), 
                        bg=themes[theme_index[0]]["sidebar"], 
                        fg=themes[theme_index[0]]["fg"])
version_label.pack(side="left", padx=10, pady=18)

right_header = tk.Frame(header_frame, bg=themes[theme_index[0]]["sidebar"])
right_header.pack(side="right", fill="y", padx=20)

settings_btn = tk.Button(right_header, text="⚙️",
                        command=open_settings,
                        bg=themes[theme_index[0]]["sidebar"],
                        fg=themes[theme_index[0]]["accent"],
                        font=("Segoe UI", 16),
                        bd=0, relief="flat", cursor="hand2", padx=10)
settings_btn.pack(side="right", padx=5, pady=15)

personality_label = tk.Label(right_header, 
                            text=f"🎭 {current_personality[0]}", 
                            font=("Segoe UI", 11), 
                            bg=themes[theme_index[0]]["sidebar"], 
                            fg=themes[theme_index[0]]["fg"])
personality_label.pack(side="right", padx=10, pady=15)

theme_name_label = tk.Label(right_header,
                           text=f"🎨 {themes[theme_index[0]]['name']}",
                           font=("Segoe UI", 11),
                           bg=themes[theme_index[0]]["sidebar"],
                           fg=themes[theme_index[0]]["fg"])
theme_name_label.pack(side="right", padx=10, pady=15)

separator = tk.Frame(root, height=1, bg=themes[theme_index[0]]["accent"])
separator.pack(fill="x")

# ----------------------- Main Container -----------------------
main_container = tk.Frame(root, bg=themes[theme_index[0]]["bg"])
main_container.pack(side="top", fill="both", expand=True)

# ----------------------- Sidebar -----------------------
sidebar_frame = tk.Frame(main_container, width=220, bg=themes[theme_index[0]]["sidebar"])
sidebar_frame.pack(side="left", fill="y", padx=5, pady=5)
sidebar_frame.pack_propagate(False)

sidebar_header = tk.Frame(sidebar_frame, bg=themes[theme_index[0]]["sidebar"])
sidebar_header.pack(fill="x", pady=10)

sidebar_title = tk.Label(sidebar_header, text="⚡ Quick Actions", 
                        font=("Segoe UI", 12, "bold"),
                        bg=themes[theme_index[0]]["sidebar"],
                        fg=themes[theme_index[0]]["accent"])
sidebar_title.pack(pady=5)

sidebar_canvas = tk.Canvas(sidebar_frame, bg=themes[theme_index[0]]["sidebar"], highlightthickness=0)
sidebar_scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=sidebar_canvas.yview)
sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)

sidebar_content = tk.Frame(sidebar_canvas, bg=themes[theme_index[0]]["sidebar"])
sidebar_canvas.create_window((0, 0), window=sidebar_content, anchor="nw")
sidebar_content.bind("<Configure>", 
                    lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all")))

sidebar_canvas.pack(side="left", fill="both", expand=True)
sidebar_scrollbar.pack(side="right", fill="y")

# ----------------------- Chat Area -----------------------
chat_container = tk.Frame(main_container, bg=themes[theme_index[0]]["bg"])
chat_container.pack(side="right", expand=True, fill="both", padx=5, pady=5)

chat_frame = tk.Frame(chat_container, bg=themes[theme_index[0]]["bg"])
chat_frame.pack(side="top", expand=True, fill="both")

chat_canvas = tk.Canvas(chat_frame, bg=themes[theme_index[0]]["bg"], highlightthickness=0)
chat_scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=chat_canvas.yview, width=12)
chat_canvas.configure(yscrollcommand=chat_scrollbar.set)
chat_canvas.pack(side="left", fill="both", expand=True)
chat_scrollbar.pack(side="right", fill="y")

chat_inner_frame = tk.Frame(chat_canvas, bg=themes[theme_index[0]]["bg"])
chat_canvas.create_window((0, 0), window=chat_inner_frame, anchor="nw")
chat_inner_frame.bind("<Configure>", 
                     lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))

def on_mousewheel(event):
    chat_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

chat_canvas.bind_all("<MouseWheel>", on_mousewheel)

# ----------------------- Quick Reply Buttons -----------------------
quick_reply_frame = tk.Frame(chat_container, bg=themes[theme_index[0]]["bg"], height=60)

def update_quick_replies():
    if settings["quick_replies_visible"]:
        quick_reply_frame.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
    else:
        quick_reply_frame.pack_forget()

def create_quick_reply_button(reply_data):
    def on_click():
        if reply_data["command"] == "search ":
            msg_entry.delete(0, tk.END)
            msg_entry.insert(0, "search ")
            msg_entry.focus()
        else:
            process_message(reply_data["command"])
    
    btn = tk.Button(quick_reply_frame, 
                   text=reply_data["text"],
                   command=on_click,
                   bg=themes[theme_index[0]]["btn"],
                   fg=themes[theme_index[0]]["fg"],
                   font=("Segoe UI", 9),
                   relief="flat", padx=10, pady=6, cursor="hand2", bd=0)
    
    def on_enter(e):
        btn.config(bg=themes[theme_index[0]]["btn_hover"])
    
    def on_leave(e):
        btn.config(bg=themes[theme_index[0]]["btn"])
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.pack(side="left", padx=3, pady=5)

for reply in quick_replies:
    create_quick_reply_button(reply)

update_quick_replies()

# ----------------------- Chat Functions -----------------------
def add_message(sender, msg, speak=True):
    is_user = sender.startswith("🧑")
    t = themes[theme_index[0]]
    
    message_history.append({"sender": sender, "message": msg, "time": datetime.now().strftime("%H:%M")})
    
    msg_container = tk.Frame(chat_inner_frame, bg=t["bg"])
    msg_container.pack(fill="x", pady=8, padx=15)
    
    if is_user:
        inner_frame = tk.Frame(msg_container, bg=t["bg"])
        inner_frame.pack(anchor="e")
        
        bubble = tk.Frame(inner_frame, bg=t["msg_user_bg"], padx=15, pady=10)
        bubble.pack(side="right", anchor="e")
        
        msg_label = tk.Label(bubble, text=msg, bg=t["msg_user_bg"], 
                           fg=t["msg_user_fg"], wraplength=450,
                           justify="left", font=("Segoe UI", settings["font_size"]))
        msg_label.pack()
        
        time_label = tk.Label(inner_frame, 
                            text=datetime.now().strftime("%H:%M"),
                            font=("Segoe UI", 8),
                            bg=t["bg"], fg=t["fg"])
        time_label.pack(side="right", padx=5)
    else:
        inner_frame = tk.Frame(msg_container, bg=t["bg"])
        inner_frame.pack(anchor="w")
        
        avatar = tk.Label(inner_frame, text="👻", font=("Segoe UI", 20), bg=t["bg"])
        avatar.pack(side="left", padx=(0, 10))
        
        content_frame = tk.Frame(inner_frame, bg=t["bg"])
        content_frame.pack(side="left", anchor="w")
        
        bubble = tk.Frame(content_frame, bg=t["msg_ghost_bg"], padx=15, pady=10)
        bubble.pack(anchor="w")
        
        msg_label = tk.Label(bubble, text=msg, bg=t["msg_ghost_bg"],
                           fg=t["msg_ghost_fg"], wraplength=450,
                           justify="left", font=("Segoe UI", settings["font_size"]))
        msg_label.pack()
        
        time_label = tk.Label(content_frame,
                            text=datetime.now().strftime("%H:%M"),
                            font=("Segoe UI", 8),
                            bg=t["bg"], fg=t["fg"])
        time_label.pack(anchor="w", pady=2)
    
    if settings["auto_scroll"]:
        chat_canvas.update_idletasks()        chat_canvas.yview_moveto(1.0)
    
    if not is_user and speak:
        speak_text(msg)

def show_typing_indicator():
    if not settings["animations_enabled"]:
        return None
        
    t = themes[theme_index[0]]
    typing_frame = tk.Frame(chat_inner_frame, bg=t["bg"], name="typing_indicator")
    typing_frame.pack(anchor="w", pady=5, padx=15)
    
    avatar = tk.Label(typing_frame, text="👻", font=("Segoe UI", 20), bg=t["bg"])
    avatar.pack(side="left", padx=(0, 10))
    
    bubble = tk.Frame(typing_frame, bg=t["msg_ghost_bg"], padx=15, pady=10)
    bubble.pack(side="left")
    
    typing_label = tk.Label(bubble, text="●●● typing...", 
                           bg=t["msg_ghost_bg"], fg=t["msg_ghost_fg"],
                           font=("Segoe UI", 11, "italic"))
    typing_label.pack()
    
    if settings["auto_scroll"]:
        chat_canvas.update_idletasks()
        chat_canvas.yview_moveto(1.0)
    return typing_frame

def remove_typing_indicator():
    for widget in chat_inner_frame.winfo_children():
        if str(widget).endswith("typing_indicator"):
            widget.destroy()

def ghost_typing(msg):
    if settings["animations_enabled"]:
        indicator = show_typing_indicator()
        root.after(800, lambda: [remove_typing_indicator(), add_message("👻 Ghost", msg)])
    else:
        add_message("👻 Ghost", msg)

def personality_reply(msg_lower):
    p = current_personality[0]
    
    if "hello" in msg_lower or "hi" in msg_lower or "hey" in msg_lower:
        return {"Funny": "Hey there! Ready to have some fun? 😄",
                "Serious": "Hello. How may I assist you?",
                "Sarcastic": "Oh look, another human. How exciting."}[p]
    elif "how are you" in msg_lower:
        return {"Funny": "I'm fine, sipping my virtual coffee ☕",
                "Serious": "I am operational and functioning normally.",
                "Sarcastic": "Surviving this digital existence, obviously."}[p]
    elif "who made you" in msg_lower or "who created you" in msg_lower:
        return {"Funny": "A genius developer with too much free time! 😎",
                "Serious": "I was programmed by a software developer.",
                "Sarcastic": "Someone who clearly had nothing better to do."}[p]
    elif "your name" in msg_lower or "who are you" in msg_lower:
        return {"Funny": "I'm Ghost! Your friendly neighborhood chatbot! 👻",
                "Serious": "I am Ghost, an AI assistant application.",
                "Sarcastic": "Ghost. Because 'Annoying Chatbot' was taken."}[p]
    elif "joke" in msg_lower:
        return random.choice(jokes) if p != "Serious" else "I don't tell jokes in serious mode."
    elif "fact" in msg_lower or "tell me something" in msg_lower:
        return random.choice(facts)
    elif "help" in msg_lower or "commands" in msg_lower:
        return """📋 Available Commands:
🎮 Games: 'snake', 'tic-tac-toe'
🧮 Math: Type equations (e.g., '5+3*2')
🔍 Search: 'search [query]'
📱 Apps: 'open chrome/notepad/calculator'
🌐 Web: 'open youtube/google/github'
🖼️ Images: 'image to pdf', 'compress image'
✅ Tasks: 'add/view/delete/clear tasks'
🎤 Voice: Click microphone button to speak
⚙️ Settings: Click gear icon in header"""
    elif "what can you do" in msg_lower or "features" in msg_lower:
        return {"Funny": "I chat, joke, play games, and boss around apps! Plus I'm great company! 😊",
                "Serious": "I can chat, calculate, play games, open applications/websites, manage tasks, process images, and respond to voice commands.",
                "Sarcastic": "Oh, everything. I'm basically magic. Ask for help if you need details."}[p]
    elif "thank" in msg_lower:
        return {"Funny": "You're welcome! Happy to help! 😊",
                "Serious": "You're welcome.",
                "Sarcastic": "Yeah yeah, I know I'm amazing."}[p]
    elif "bye" in msg_lower or "goodbye" in msg_lower:
        return {"Funny": "See you later! Don't be a stranger! 👋",
                "Serious": "Goodbye.",
                "Sarcastic": "Finally. I mean... bye!"}[p]
    else:
        defaults = {
            "Funny": ["Let me think about that... 🤔", "Interesting question!", "That's a good one!", "Hmm, tell me more!"],
            "Serious": ["I don't have information on that.", "Please rephrase your question.", "I cannot answer that."],
            "Sarcastic": ["Wow, deep question.", "Let me consult my crystal ball... nope, nothing.", "That's... specific."]
        }
        return random.choice(defaults[p])
    

def ai_reply(user_message: str) -> str:
    """
    Get a response from a local AI model (Ollama).
    Falls back to personality_reply if AI isn't available.
    """
    # If Ollama or the library isn't available, keep old behaviour
    if not AI_AVAILABLE:
        return personality_reply(user_message.lower())

    # Add user message to AI history
    ai_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        # Ask the local model
        response = ollama.chat(
            model="llama3.2",  # same name you pulled in Step 1
            messages=ai_history
        )

        assistant_message = response["message"]["content"]

        # Save assistant reply in history too
        ai_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    except Exception as e:
        # If something goes wrong, don’t crash the app
        return f"⚠️ AI error: {e}"


# ----------------------- Games -----------------------
def launch_snake():
    snake_win = tk.Toplevel(root)
    snake_win.title("🐍 Snake Game")
    snake_win.geometry("420x480")
    snake_win.resizable(False, False)
    snake_win.configure(bg=themes[theme_index[0]]["bg"])
    
    header = tk.Frame(snake_win, bg=themes[theme_index[0]]["sidebar"], height=50)
    header.pack(fill="x")
    
    canvas = tk.Canvas(snake_win, bg="#0d1117", width=400, height=400, 
                      highlightthickness=2, highlightbackground=themes[theme_index[0]]["accent"])
    canvas.pack(pady=10)
    
    score_label = tk.Label(header, text=f"Score: 0 | 🏆 {game_scores['snake']}", 
                          font=("Segoe UI", 13, "bold"), 
                          bg=themes[theme_index[0]]["sidebar"], 
                          fg=themes[theme_index[0]]["accent"])
    score_label.pack(pady=10)
    
    snake = [[200, 200]]
    direction = ["Right"]
    food = [random.randint(0,19)*20, random.randint(0,19)*20]
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
            if current_score[0] > game_scores['snake']:
                game_scores['snake'] = current_score[0]
                save_data()
            if messagebox.askyesno("Game Over", 
                                  f"🐍 Snake crashed!\n\n🎯 Score: {current_score[0]}\n🏆 High: {game_scores['snake']}\n\nPlay again?"):
                restart_game()
            else:
                snake_win.destroy()
            return
        
        snake.append(head)
        if head == food:
            food[0], food[1] = random.randint(0,19)*20, random.randint(0,19)*20
            current_score[0] += 1
            score_label.config(text=f"Score: {current_score[0]} | 🏆 {game_scores['snake']}")
        else:
            snake.pop(0)
        draw()
        snake_win.after(120, move_snake)

    def draw():
        canvas.delete("all")
        for i, segment in enumerate(snake):
            shade = 255 - int((i / len(snake)) * 100)
            color = f"#{0:02x}{shade:02x}{0:02x}"
            canvas.create_rectangle(segment[0], segment[1], 
                                  segment[0]+20, segment[1]+20, 
                                  fill=color, outline="#00ff00", width=2)
        canvas.create_oval(food[0]+2, food[1]+2, 
                         food[0]+18, food[1]+18, 
                         fill="#ff0000", outline="#ff6666", width=2)

    def change_direction(e):
        if e.keysym in ["Up", "Down", "Left", "Right"]:
            if (direction[0] in ["Up", "Down"] and e.keysym in ["Left", "Right"]) or \
               (direction[0] in ["Left", "Right"] and e.keysym in ["Up", "Down"]):
                direction[0] = e.keysym

    def restart_game():
        snake.clear()
        snake.append([200,200])
        direction[0] = "Right"
        food[0], food[1] = random.randint(0,19)*20, random.randint(0,19)*20
        game_over[0] = False
        current_score[0] = 0
        score_label.config(text=f"Score: 0 | 🏆 {game_scores['snake']}")
        move_snake()

    snake_win.bind("<KeyPress>", change_direction)
    snake_win.focus_set()
    move_snake()

def launch_tictactoe():
    tt_win = tk.Toplevel(root)
    tt_win.title("⌛⭕ Tic-Tac-Toe")
    tt_win.geometry("350x400")
    tt_win.resizable(False, False)
    tt_win.configure(bg=themes[theme_index[0]]["bg"])
    
    header = tk.Frame(tt_win, bg=themes[theme_index[0]]["sidebar"], height=60)
    header.pack(fill="x")
    
    canvas = tk.Canvas(tt_win, bg="#ffffff", width=320, height=320,
                      highlightthickness=2, highlightbackground=themes[theme_index[0]]["accent"])
    canvas.pack(pady=10)
    
    score_label = tk.Label(header, 
                          text=f"⌛ {game_scores['tic_tac_toe']['X']}  •  ⭕ {game_scores['tic_tac_toe']['O']}", 
                          font=("Segoe UI", 14, "bold"),
                          bg=themes[theme_index[0]]["sidebar"],
                          fg=themes[theme_index[0]]["accent"])
    score_label.pack(pady=15)

    board = [["" for _ in range(3)] for _ in range(3)]
    turn = ["X"]

    def draw_board():
        canvas.delete("all")
        for i in range(1,3):
            canvas.create_line(i*106.67, 0, i*106.67, 320, width=4, fill="#333333")
            canvas.create_line(0, i*106.67, 320, i*106.67, width=4, fill="#333333")
        for r in range(3):
            for c in range(3):
                if board[r][c] == "X":
                    x1, y1 = c*106.67+20, r*106.67+20
                    x2, y2 = c*106.67+86.67, r*106.67+86.67
                    canvas.create_line(x1, y1, x2, y2, width=8, fill="#0969da")
                    canvas.create_line(x2, y1, x1, y2, width=8, fill="#0969da")
                elif board[r][c] == "O":
                    cx, cy = c*106.67+53.33, r*106.67+53.33
                    canvas.create_oval(cx-33, cy-33, cx+33, cy+33, 
                                     width=8, outline="#dc3545", fill="")

    def check_winner():
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != "": return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != "": return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != "": return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "": return board[0][2]
        return None

    def click(event):
        r, c = min(event.y//107, 2), min(event.x//107, 2)
        if board[r][c] == "":
            board[r][c] = turn[0]
            turn[0] = "O" if turn[0] == "X" else "X"
            draw_board()
            winner = check_winner()
            if winner:
                game_scores['tic_tac_toe'][winner] += 1
                save_data()
                score_label.config(text=f"⌛ {game_scores['tic_tac_toe']['X']}  •  ⭕ {game_scores['tic_tac_toe']['O']}")
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

# ----------------------- Tasks -----------------------
def add_task():
    task = simpledialog.askstring("➕ Add Task", "Enter a new task:")
    if task and task.strip():
        todo_list.append(task.strip())
        save_data()
        ghost_typing(f"✅ Task added: {task}")

def view_tasks():
    if not todo_list:
        ghost_typing("📋 Your to-do list is empty.")
        return
    
    task_win = tk.Toplevel(root)
    task_win.title("📋 My Tasks")
    task_win.geometry("400x500")
    task_win.configure(bg=themes[theme_index[0]]["bg"])
    
    header = tk.Frame(task_win, bg=themes[theme_index[0]]["sidebar"], height=60)
    header.pack(fill="x")
    
    title = tk.Label(header, text=f"📋 {len(todo_list)} Task(s)",
                    font=("Segoe UI", 16, "bold"),
                    bg=themes[theme_index[0]]["sidebar"],
                    fg=themes[theme_index[0]]["accent"])
    title.pack(pady=15)
    
    task_frame = tk.Frame(task_win, bg=themes[theme_index[0]]["bg"])
    task_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    for i, task in enumerate(todo_list, 1):
        item_frame = tk.Frame(task_frame, bg=themes[theme_index[0]]["btn"], relief="flat", bd=1)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        number = tk.Label(item_frame, text=f"{i}.", font=("Segoe UI", 12, "bold"),
                         bg=themes[theme_index[0]]["btn"], fg=themes[theme_index[0]]["accent"], width=3)
        number.pack(side="left", padx=5, pady=10)
        
        task_label = tk.Label(item_frame, text=task, font=("Segoe UI", 11),
                             bg=themes[theme_index[0]]["btn"], fg=themes[theme_index[0]]["fg"], anchor="w")
        task_label.pack(side="left", fill="x", expand=True, padx=5, pady=10)

def delete_task():
    if not todo_list:
        ghost_typing("⌛ No tasks to delete.")
        return
    task_num = simpledialog.askinteger("🗑️ Delete Task", f"Enter task number (1-{len(todo_list)}):")
    if task_num and 1 <= task_num <= len(todo_list):
        removed = todo_list.pop(task_num - 1)
        save_data()
        ghost_typing(f"🗑️ Deleted: {removed}")
    else:
        ghost_typing("⌛ Invalid task number.")

def clear_tasks():
    if todo_list:
        if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?"):
            todo_list.clear()
            save_data()
            ghost_typing("🗑️ All tasks cleared!")
    else:
        ghost_typing("📋 Task list is already empty.")

def take_screenshot():
    try:
        root.update()
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width() + x
        h = root.winfo_height() + y
        img = ImageGrab.grab(bbox=(x, y, w, h))
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if save_path:
            img.save(save_path)
            ghost_typing(f"📸 Screenshot saved!")
    except Exception as e:
        ghost_typing(f"⌛ Screenshot failed: {str(e)}")

# ----------------------- Theme & Personality -----------------------
def toggle_personality():
    idx = (personalities.index(current_personality[0]) + 1) % len(personalities)
    current_personality[0] = personalities[idx]
    personality_label.config(text=f"🎭 {current_personality[0]}")
    save_data()
    ghost_typing(f"🎭 Personality set to {current_personality[0]}")

def toggle_tts():
    if engine:
        settings["tts_enabled"] = not settings["tts_enabled"]
        save_data()
        status = "enabled" if settings["tts_enabled"] else "disabled"
        ghost_typing(f"🔊 Text-to-speech {status}")
    else:
        messagebox.showwarning("TTS Unavailable", "Text-to-speech is not available.")

def cycle_theme():
    theme_index[0] = (theme_index[0] + 1) % len(themes)
    save_data()
    apply_theme()
    theme_name_label.config(text=f"🎨 {themes[theme_index[0]]['name']}")
    ghost_typing(f"🎨 Theme changed to {themes[theme_index[0]]['name']}")

def apply_theme():
    t = themes[theme_index[0]]
    
    # Main frames
    root.configure(bg=t["bg"])
    main_container.configure(bg=t["bg"])
    chat_container.configure(bg=t["bg"])
    chat_frame.configure(bg=t["bg"])
    chat_canvas.configure(bg=t["bg"])
    chat_inner_frame.configure(bg=t["bg"])
    bottom_frame.configure(bg=t["bg"])
    quick_reply_frame.configure(bg=t["bg"])
    
    # Sidebar frames
    sidebar_frame.configure(bg=t["sidebar"])
    sidebar_header.configure(bg=t["sidebar"])
    sidebar_title.configure(bg=t["sidebar"], fg=t["accent"])
    sidebar_canvas.configure(bg=t["sidebar"])
    sidebar_content.configure(bg=t["sidebar"])
    
    # Header frames
    header_frame.configure(bg=t["sidebar"])
    left_header.configure(bg=t["sidebar"])
    right_header.configure(bg=t["sidebar"])
    header_label.configure(bg=t["sidebar"], fg=t["accent"])
    version_label.configure(bg=t["sidebar"], fg=t["fg"])
    personality_label.configure(bg=t["sidebar"], fg=t["fg"])
    theme_name_label.configure(bg=t["sidebar"], fg=t["fg"])
    settings_btn.configure(bg=t["sidebar"], fg=t["accent"])
    
    # Entry and buttons
    msg_entry.configure(
        bg=t["input_bg"], fg=t["fg"], insertbackground=t["accent"],
        highlightbackground=t["input_border"], highlightcolor=t["accent"]
    )
    send_button.configure(bg=t["accent"])
    voice_button.configure(bg=t["btn"] if not is_listening[0] else "#dc3545")
    separator.configure(bg=t["accent"])
    voice_status_label.configure(bg=t["bg"])
    
    # Sidebar child widgets
    for widget in sidebar_content.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(
                bg=t["btn"],
                fg=t["fg"],
                activebackground=t["btn_hover"],
                activeforeground=t["accent"]
            )
        elif isinstance(widget, tk.Label):
            widget.configure(bg=t["sidebar"], fg=t["fg"])
    
    # Chat inner frame widgets
    for widget in chat_inner_frame.winfo_children():
        widget.configure(bg=t["bg"])
    
    # Update quick replies
    update_quick_replies()

# ----------------------- Sidebar Buttons -----------------------
def add_sidebar_button(text, command):
    btn = tk.Button(sidebar_content, text=text, command=command,
                    bg=themes[theme_index[0]]["btn"],
                    fg=themes[theme_index[0]]["fg"],
                    font=("Segoe UI", 10),
                    relief="flat", bd=0, padx=10, pady=8, cursor="hand2")
    btn.pack(fill="x", pady=3, padx=5)
    def on_enter(e): btn.config(bg=themes[theme_index[0]]["btn_hover"])
    def on_leave(e): btn.config(bg=themes[theme_index[0]]["btn"])
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

add_sidebar_button("🎭 Change Personality", toggle_personality)
add_sidebar_button("🎨 Change Theme", cycle_theme)
add_sidebar_button("🗣️ Toggle TTS", toggle_tts)
add_sidebar_button("📋 View Tasks", view_tasks)
add_sidebar_button("➕ Add Task", add_task)
add_sidebar_button("🗑️ Delete Task", delete_task)
add_sidebar_button("🧹 Clear Tasks", clear_tasks)
add_sidebar_button("📸 Screenshot", take_screenshot)

# ----------------------- Bottom Input -----------------------
bottom_frame = tk.Frame(root, bg=themes[theme_index[0]]["bg"], height=60)
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

msg_entry = tk.Entry(bottom_frame, font=("Segoe UI", 11),
                     bg=themes[theme_index[0]]["input_bg"],
                     fg=themes[theme_index[0]]["fg"],
                     insertbackground=themes[theme_index[0]]["accent"], 
                     relief="flat", highlightthickness=1,
                     highlightbackground=themes[theme_index[0]]["input_border"])
msg_entry.bind("<Return>", lambda event: send_message())
msg_entry.bind("<Return>", lambda event: send_message())
msg_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

send_button = tk.Button(bottom_frame, text="📤 Send", font=("Segoe UI", 10, "bold"),
                        bg=themes[theme_index[0]]["accent"], fg="#ffffff",
                        relief="flat", padx=15, pady=8, cursor="hand2")
send_button.pack(side="left", padx=5, pady=10)

voice_button = tk.Button(bottom_frame, text="🎤 Voice", font=("Segoe UI", 10, "bold"),
                         command=start_voice_input,
                         bg=themes[theme_index[0]]["btn"],
                         fg=themes[theme_index[0]]["fg"],
                         relief="flat", padx=15, pady=8, cursor="hand2")
voice_button.pack(side="left", padx=5, pady=10)

voice_status_label = tk.Label(bottom_frame, text="", font=("Segoe UI", 9, "italic"),
                              bg=themes[theme_index[0]]["bg"],
                              fg=themes[theme_index[0]]["accent"])
voice_status_label.pack(side="left", padx=10)

def send_message():
    msg = msg_entry.get().strip()
    if not msg:
        return

    add_message("🧑 You", msg)
    msg_entry.delete(0, tk.END)

    response = process_message(msg)

    # Commands (jaise snake, search, tasks, calculator) turant reply denge
    # AI waali branch ab background thread mein answer bhej rahi hai, 
    # waha se None return hoga.
    if response is not None:
        ghost_typing(response)


send_button.config(command=send_message)

def process_message(msg):
    msg_lower = msg.lower()

    # Voice commands
    if "open " in msg_lower:
        target = msg_lower.split("open ", 1)[1]
        if target in apps:
            os.startfile(apps[target])
            return f"🖥️ Opening {target}..."
        elif target in websites:
            webbrowser.open(websites[target])
            return f"🌐 Opening {target}..."
        else:
            return "❌ App or site not recognized."
    elif msg_lower.startswith("search "):
        query = msg_lower.split("search ", 1)[1]
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"🔍 Searching Google for '{query}'..."
    elif msg_lower in ["snake", "play snake"]:
        launch_snake()
        return "🐍 Starting Snake game!"
    elif "tic" in msg_lower:
        launch_tictactoe()
        return "⌛ Starting Tic-Tac-Toe!"
    elif "add task" in msg_lower:
        add_task()
        return "Added task!"
    elif "view task" in msg_lower:
        view_tasks()
        return "Opening your tasks..."
    elif "delete task" in msg_lower:
        delete_task()
        return "Deleting task..."
    elif "clear task" in msg_lower:
        clear_tasks()
        return "Clearing all tasks..."
    elif any(op in msg_lower for op in "+-*/%"):
        result = safe_calculate(msg_lower)
        return f"🧮 Result: {result}" if result is not None else "⚠️ I can’t calculate that."
    else:
        def run_ai():
            response = ai_reply(msg)
            root.after(0, lambda: ghost_typing(response))
        threading.Thread(target=run_ai, daemon=True).start()
        return None


apply_theme()
root.mainloop()