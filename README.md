# 👻 Ghost Chat

Ghost Chat is a modern, feature-rich Python AI Voice Assistant built with CustomTkinter. It leverages local AI to provide a private, fast, and comprehensive daily companion that can help you with productivity, answering questions, controlling your system, and even playing games.

<div align="center">
  <img src="https://via.placeholder.com/800x450.png?text=Ghost+Chat+Dashboard" alt="Ghost Chat UI" width="600"/>
</div>

---

## 🚀 Features

- **Modern UI**: Sleek, scrollable, themable (Custom Light/Dark modes) interface built with CustomTkinter.
- **Local AI Integration**: Powered by [Ollama](https://ollama.com/), running completely offline for maximum privacy.
- **Voice Capabilities**: Wake word detection ("Hey Ghost"), speech-to-text input, and text-to-speech output.
- **File Format Converter & Uploader**: Easily convert between Image formats, Data (CSV/JSON/Excel), and Documents (PDF/Word/Text/PPTX) via an intuitive UI or natural language prompts.
- **Web & YouTube Summarizer**: Paste an article URL or YouTube video link and instantly get a detailed AI-generated summary.
- **Image Studio**: Perform OCR (extract text from images), Image Analysis (using local LLaVA models), and Image Generation.
- **Code Assistant**: Dedicated Code Generator sandbox and Explainer for programming help.
- **Productivity Suite**: Pomodoro Timer, Task Manager (To-Do list), Reminders/Alarms, File Search, Calculator, and Screenshot capture.
- **System Controls**: Directly control system volume, media playback, and lock the computer using natural commands.
- **Mini-Games**: Take a break by playing Snake, Tic-Tac-Toe, 2048, Wordle, Trivia Quiz, and a Typing Speed Test directly in the app.
- **Fun Extras**: Real-time weather updates, daily motivational quotes, random facts, jokes, and more.

---

## 🛠 Requirements

- **Python 3.9+**
- **Ollama** installed on your system with the `llama3.2` model (and `llava` if using image analysis).

### Dependencies

Install the required Python packages using pip:

```bash
pip install customtkinter pillow pyttsx3 SpeechRecognition pyaudio ollama bs4 requests youtube-transcript-api pdfplumber python-docx pandas PyPDF2 pdf2docx docx2pdf python-pptx comtypes
```

*(Note: `pyaudio` may require additional system-level configurations depending on your OS).*

---

## 💻 Usage

1. Start your local Ollama instance. Make sure you have downloaded the base model:
   ```bash
   ollama run llama3.2
   ```

2. Run the main application file:
   ```bash
   python main.py
   ```

3. **Interacting**:
   - Type in the message box manually.
   - Click the microphone icon to speak.
   - Say "Hey Ghost" to activate hands-free listening.
   - Click the attachment icon (📎) to upload files for format conversion or analysis.
   - Open specific tools (Summarizer, games, Code Generator) from the left sidebar.
   - Type `help` within the chat for a full list of commands.

---

## 📂 Project Structure

- `main.py` - Core application and GUI event loop.
- `ai_handler.py` - Manages text generation, speech processing, and communication with Ollama.
- `config.py` - Settings, themes, layout definitions, and persistent data paths.
- `format_converter.py` - Module for converting documents, spreadsheets, and images.
- `summarizer.py` - Module for scraping and summarizing web articles and YouTube videos.
- `games.py` - Houses all the mini-games (Snake, 2048, Wordle, etc.).
- `code_generator.py` - Dedicated UI for the Code Assistant.
- `utils.py` - Helper functions for weather tracking, calc, and file searches.
- `system_control.py` - OS-level hooks to adjust volume and media playback.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to suggest a feature or report a bug, please create an Issue or submit a Pull Request.

---

## 📝 License

This project is licensed under the MIT License.
