import os
import json

# ======================= Data Lists =======================
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
    "How does a developer announce their engagement? They git commit.",
    "What's a programmer's favorite hangout place? The Foo Bar.",
    "Why was the computer cold? It left its Windows open.",
    "How do you comfort a JavaScript bug? You console it.",
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
    "A day on Venus is longer than a year on Venus.",
    "Oxford University is older than the Aztec Empire.",
    "Scotland's national animal is the unicorn.",
    "The first computer 'bug' was an actual moth stuck in a Harvard Mark II computer.",
]

apps = {
    "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "notepad": "notepad.exe",
    "cmd": "cmd.exe",
    "camera": "microsoft.windows.camera:",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
}

websites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "github": "https://www.github.com",
    "reddit": "https://www.reddit.com",
    "stackoverflow": "https://stackoverflow.com",
    "chatgpt": "https://chat.openai.com",
}

quotes = [
    "The only way to do great work is to love what you do. — Steve Jobs",
    "Innovation distinguishes between a leader and a follower. — Steve Jobs",
    "Stay hungry, stay foolish. — Steve Jobs",
    "Code is like humor. When you have to explain it, it's bad. — Cory House",
    "First, solve the problem. Then, write the code. — John Johnson",
    "The best error message is the one that never shows up. — Thomas Fuchs",
    "It's not a bug; it's an undocumented feature. — Anonymous",
    "Simplicity is the soul of efficiency. — Austin Freeman",
    "Talk is cheap. Show me the code. — Linus Torvalds",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. — Martin Fowler",
    "The most disastrous thing you can ever learn is your first programming language. — Alan Kay",
    "Programming isn't about what you know; it's about what you can figure out. — Chris Pine",
    "The function of good software is to make the complex appear to be simple. — Grady Booch",
    "Believe you can and you're halfway there. — Theodore Roosevelt",
    "Success is not final, failure is not fatal: it is the courage to continue that counts. — Winston Churchill",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Don't stop when you're tired. Stop when you're done.",
]

trivia_questions = [
    {"q": "What does CPU stand for?", "options": ["Central Processing Unit", "Computer Personal Unit", "Central Process Utility", "Core Processing Unit"], "answer": 0},
    {"q": "Who created Python?", "options": ["James Gosling", "Guido van Rossum", "Bjarne Stroustrup", "Dennis Ritchie"], "answer": 1},
    {"q": "What year was the first iPhone released?", "options": ["2005", "2006", "2007", "2008"], "answer": 2},
    {"q": "What does HTML stand for?", "options": ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "Home Tool Markup Language"], "answer": 0},
    {"q": "Which company developed JavaScript?", "options": ["Microsoft", "Google", "Netscape", "Apple"], "answer": 2},
    {"q": "How many bits are in a byte?", "options": ["4", "8", "16", "32"], "answer": 1},
    {"q": "What does 'www' stand for?", "options": ["World Wide Web", "World Web Wide", "Wide World Web", "Web World Wide"], "answer": 0},
    {"q": "Which programming language is known as the 'mother of all languages'?", "options": ["Python", "C", "Java", "Assembly"], "answer": 1},
    {"q": "What is the binary representation of the number 10?", "options": ["1010", "1100", "1001", "1110"], "answer": 0},
    {"q": "What does RAM stand for?", "options": ["Random Access Memory", "Read Access Memory", "Run Access Memory", "Rapid Access Memory"], "answer": 0},
    {"q": "Who is known as the father of computers?", "options": ["Alan Turing", "Charles Babbage", "John von Neumann", "Tim Berners-Lee"], "answer": 1},
    {"q": "What does SQL stand for?", "options": ["Structured Query Language", "Simple Query Language", "Standard Query Logic", "System Query Language"], "answer": 0},
    {"q": "Which planet is closest to the Sun?", "options": ["Venus", "Earth", "Mercury", "Mars"], "answer": 2},
    {"q": "What is the speed of light approximately?", "options": ["300,000 km/s", "150,000 km/s", "500,000 km/s", "100,000 km/s"], "answer": 0},
    {"q": "What does GPU stand for?", "options": ["Graphics Processing Unit", "General Processing Unit", "Graphics Power Unit", "General Power Utility"], "answer": 0},
]

wordle_words = [
    "ghost", "brain", "light", "stone", "water", "flame", "storm",
    "cloud", "dream", "steel", "sharp", "world", "heart", "power",
    "smile", "brave", "quick", "trace", "crane", "slate", "share",
    "spare", "stare", "glare", "flare", "store", "score", "shore",
    "snare", "grape", "drape", "place", "space", "grace", "brace",
    "price", "slice", "spice", "voice", "dance", "lance", "range",
    "angel", "baker", "candy", "daisy", "eagle", "faith", "giant",
    "habit", "ivory", "jolly", "knack", "lemon", "magic", "noble",
]

typing_test_texts = [
    "The quick brown fox jumps over the lazy dog near the riverbank.",
    "Programming is the art of telling a computer what to do step by step.",
    "Ghost Chat is a helpful voice assistant that can play games and answer questions.",
    "Python is a versatile programming language used for web development and AI.",
    "The best way to predict the future is to create it with determination.",
    "Every expert was once a beginner who decided not to give up on their dreams.",
    "Technology is best when it brings people together and solves real problems.",
    "Clean code always looks like it was written by someone who cares deeply.",
]

quick_replies = [
    {"text": "😄 Joke", "command": "joke"},
    {"text": "🧠 Fact", "command": "fact"},
    {"text": "🎮 Games", "command": "help games"},
    {"text": "☁️ Weather", "command": "weather in "},
    {"text": "🔍 Search", "command": "search "},
    {"text": "⏰ Remind", "command": "remind me in "},
    {"text": "❓ Help", "command": "help"},
]

# ======================= State =======================
game_scores = {"snake": 0, "tic_tac_toe": {"X": 0, "O": 0}, "typing_test": 0}
todo_list = []
message_log = []  # For export

settings = {
    "tts_enabled": True,
    "quick_replies_visible": True,
    "animations_enabled": True,
    "font_size": 13,
    "auto_scroll": True,
    "sound_enabled": False,
    "voice_input_enabled": True,
    "continuous_listening": False,
    "tts_rate": 150,
    "tts_volume": 1.0,
    "voice_language": "en-US",
    "theme_index": 0,
    "edge_voice": "en-US-ChristopherNeural",
}

# ======================= Themes =======================
themes = [
    # Each theme has a "light" key: True = use CTk light mode, False = dark mode
    {
        "name": "Obsidian", "light": False,
        "bg": "#111118",
        "fg": "#e4e4ed",
        "sidebar": "#18181f",
        "sidebar_hover": "#232330",
        "card": "#1c1c26",
        "btn": "#28283a",
        "btn_hover": "#36364d",
        "msg_user_bg": "#4f6df5",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#22222e",
        "msg_ghost_fg": "#d8d8e8",
        "accent": "#6c7bf7",
        "accent_hover": "#8b97fa",
        "input_bg": "#1c1c26",
        "input_border": "#2e2e42",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "muted": "#6b6b80",
    },
    {
        "name": "Carbon", "light": False,
        "bg": "#161616",
        "fg": "#f4f4f4",
        "sidebar": "#1e1e1e",
        "sidebar_hover": "#2a2a2a",
        "card": "#222222",
        "btn": "#333333",
        "btn_hover": "#444444",
        "msg_user_bg": "#0f62fe",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#262626",
        "msg_ghost_fg": "#e0e0e0",
        "accent": "#78a9ff",
        "accent_hover": "#a6c8ff",
        "input_bg": "#1e1e1e",
        "input_border": "#393939",
        "success": "#42be65",
        "warning": "#f1c21b",
        "danger": "#fa4d56",
        "muted": "#6f6f6f",
    },
    {
        "name": "Emerald", "light": False,
        "bg": "#0c1a14",
        "fg": "#d1fae5",
        "sidebar": "#112920",
        "sidebar_hover": "#163a2c",
        "card": "#153527",
        "btn": "#1c4034",
        "btn_hover": "#25574a",
        "msg_user_bg": "#059669",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#163228",
        "msg_ghost_fg": "#d1fae5",
        "accent": "#10b981",
        "accent_hover": "#34d399",
        "input_bg": "#112920",
        "input_border": "#1c4034",
        "success": "#22c55e",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "muted": "#6b8f80",
    },
    {
        "name": "Rosewood", "light": False,
        "bg": "#1a0f0f",
        "fg": "#fce4ec",
        "sidebar": "#241414",
        "sidebar_hover": "#331c1c",
        "card": "#2a1818",
        "btn": "#3d2222",
        "btn_hover": "#552e2e",
        "msg_user_bg": "#e11d48",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#2a1818",
        "msg_ghost_fg": "#fce4ec",
        "accent": "#fb7185",
        "accent_hover": "#fda4af",
        "input_bg": "#241414",
        "input_border": "#3d2222",
        "success": "#34d399",
        "warning": "#fbbf24",
        "danger": "#f87171",
        "muted": "#8b6b6b",
    },
    {
        "name": "Slate", "light": False,
        "bg": "#0f172a",
        "fg": "#e2e8f0",
        "sidebar": "#1e293b",
        "sidebar_hover": "#273548",
        "card": "#1e293b",
        "btn": "#334155",
        "btn_hover": "#475569",
        "msg_user_bg": "#3b82f6",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#1e293b",
        "msg_ghost_fg": "#e2e8f0",
        "accent": "#60a5fa",
        "accent_hover": "#93c5fd",
        "input_bg": "#1e293b",
        "input_border": "#334155",
        "success": "#4ade80",
        "warning": "#facc15",
        "danger": "#f87171",
        "muted": "#94a3b8",
    },
    {
        "name": "Frost", "light": True,
        "bg": "#f5f7fa",
        "fg": "#1a1a2e",
        "sidebar": "#ebeef2",
        "sidebar_hover": "#dde1e8",
        "card": "#ffffff",
        "btn": "#dde1e8",
        "btn_hover": "#ccd1da",
        "msg_user_bg": "#4f6df5",
        "msg_user_fg": "#ffffff",
        "msg_ghost_bg": "#e8ebf0",
        "msg_ghost_fg": "#1a1a2e",
        "accent": "#4f6df5",
        "accent_hover": "#6c82f7",
        "input_bg": "#ffffff",
        "input_border": "#ccd1da",
        "success": "#16a34a",
        "warning": "#d97706",
        "danger": "#dc2626",
        "muted": "#6b7280",
    },
]

# ======================= File IO =======================
DATA_FILE = "ghost_chat_data.json"
HISTORY_FILE = "ghost_chat_history.json"


def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                game_scores["snake"] = data.get("snake_score", 0)
                game_scores["tic_tac_toe"] = data.get("ttt_scores", {"X": 0, "O": 0})
                game_scores["typing_test"] = data.get("typing_best_wpm", 0)
                todo_list.clear()
                todo_list.extend(data.get("todo_list", []))
                settings["theme_index"] = data.get("theme", 0)
                loaded = data.get("settings", {})
                for k, v in loaded.items():
                    if k in settings:
                        settings[k] = v
    except Exception as e:
        print(f"Could not load data: {e}")


def save_data():
    try:
        data = {
            "snake_score": game_scores["snake"],
            "ttt_scores": game_scores["tic_tac_toe"],
            "typing_best_wpm": game_scores["typing_test"],
            "todo_list": todo_list,
            "theme": settings["theme_index"],
            "settings": settings,
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Could not save data: {e}")


def load_ai_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
    except:
        return []
    return []


def save_ai_history(history):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except:
        pass
