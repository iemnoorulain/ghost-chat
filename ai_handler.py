import threading
import random
import config
import asyncio
import os
import re

try:
    import ollama
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

try:
    import speech_recognition as sr
    VOICE_INPUT_AVAILABLE = True
except ImportError:
    VOICE_INPUT_AVAILABLE = False
    print("Speech recognition packages not installed.")

# ----------------------- TTS Engine -----------------------
try:
    import edge_tts
    import pygame
    pygame.mixer.init()
    EDGE_TTS_AVAILABLE = True
except ImportError as e:
    EDGE_TTS_AVAILABLE = False
    print(f"Edge TTS packages not installed: {e}")

if VOICE_INPUT_AVAILABLE:
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    recognizer.dynamic_energy_threshold = True
else:
    recognizer = None

# ----------------------- Module Integrations -----------------------
from memory_manager import memory_manager
import sandbox
import system_control

try:
    from duckduckgo_search import DDGS
    WEB_SEARCH_AVAILABLE = True
except ImportError:
    WEB_SEARCH_AVAILABLE = False


# ----------------------- Memory -----------------------
ai_history = config.load_ai_history()

def speak_text(text):
    """Speak text using Edge-TTS in a separate thread"""
    if config.settings.get("tts_enabled", True) and EDGE_TTS_AVAILABLE:
        def speak_thread():
            try:
                # Remove emojis and markdown for pure speech
                clean_text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
                clean_text = clean_text.replace('*', '').replace('`', '').strip()
                if not clean_text or clean_text.isspace():
                    return
                
                voice = config.settings.get("edge_voice", "en-US-ChristopherNeural")
                
                sentences = re.split(r'([.!?]+)', clean_text)
                chunks = []
                current = ""
                for part in sentences:
                    if part.strip():
                        current += part
                        if re.search(r'[.!?]', part):
                            chunks.append(current.strip())
                            current = ""
                if current.strip():
                    chunks.append(current.strip())
                if not chunks:
                    chunks = [clean_text]

                for i, chunk in enumerate(chunks):
                    if not chunk.strip(): continue
                    temp_file = f"temp_speech_{i}.mp3"
                    
                    async def generate_speech():
                        communicate = edge_tts.Communicate(chunk, voice)
                        await communicate.save(temp_file)
                    
                    asyncio.run(generate_speech())
                    
                    if os.path.exists(temp_file):
                        pygame.mixer.music.load(temp_file)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                        pygame.mixer.music.unload()
                        try:
                            os.remove(temp_file)
                        except Exception:
                            pass
            except Exception as e:
                print(f"TTS Error: {e}")
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()

def listen_for_voice():
    """Listen for voice input and return recognized text using Whisper"""
    if not VOICE_INPUT_AVAILABLE or not config.settings.get("voice_input_enabled", True):
        return None
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=15)
            # Use Whisper! Native in SpeechRecognition since v3.9+
            try:
                text = recognizer.recognize_whisper(audio, model="base").strip()
            except Exception as whisper_err:
                print(f"Whisper error {whisper_err}, falling back to Google")
                text = recognizer.recognize_google(audio, language=config.settings.get("voice_language", "en-US")).strip()
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

def perform_web_search(query):
    if not WEB_SEARCH_AVAILABLE:
        return "Web search is disabled. Install duckduckgo-search."
    try:
        results = ""
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results += f"- {r['title']}: {r['body']}\n"
        sys_info = "Search Results:\n" + results if results else "No results found."
        return sys_info
    except Exception as e:
        return f"Web search error: {e}"

def fallback_reply(msg_lower):
    """Simple fallback when AI is not available"""
    if "hello" in msg_lower or "hi" in msg_lower or "hey" in msg_lower:
        return "Hey there! How can I help you? 😊"
    elif "joke" in msg_lower:
        return random.choice(config.jokes)
    elif "fact" in msg_lower or "tell me something" in msg_lower:
        return random.choice(config.facts)
    elif "help" in msg_lower or "commands" in msg_lower:
        return """📋 Available Commands:
🎮 Games: 'snake', 'tic-tac-toe'
🧮 Math: Type equations (e.g., '5+3*2')
🔍 Search: 'search [query]'
☁️ Weather: 'weather in [city]'
📱 Apps: 'open chrome/notepad/calculator'
🌐 Web: 'open youtube/google/github'
✅ Tasks: 'add/view/delete/clear tasks'
🎤 Voice: Click microphone or say 'Hey Ghost'"""
    elif "thank" in msg_lower:
        return "You're welcome! 😊"
    elif "bye" in msg_lower or "goodbye" in msg_lower:
        return "See you later! 👋"
    else:
        fallbacks = [
            "Hmm, I'm not sure about that. Try asking differently! 🤔",
            "Interesting question! I'd need AI to answer that properly.",
            "I can help with games, tasks, weather, and more. Type 'help'!",
        ]
        return random.choice(fallbacks)


# Agent thinking system prompt
AGENT_SYSTEM_PROMPT = """You are Ghost Chat, a highly capable local AI assistant with FULL access to the user's system and the internet.
You have tools to accomplish tasks. Do NOT say you cannot do something if you have a tool for it.

TOOLS:
1. WEB SEARCH: If you need real-time info or to search the web, start your response EXACTLY with:
[SEARCH: your query here]
The system will inject the results.

2. SYSTEM & CODE EXECUTION: You can control the PC, change volume, pause/play music, lock screen, or write any python script. TO EXECUTE CODE, start your response EXACTLY with:
[EXECUTE: python code here]
For example, to pause music:
[EXECUTE: import system_control; system_control.media_play_pause()]
To change volume:
[EXECUTE: import system_control; system_control.set_volume(0.5)]

If the user asks you to do a system action, you MUST use the [EXECUTE: ...] tool. Do not say you are just a text AI."""

def ai_reply_stream(user_message: str, callback):
    """
    Get a streaming response from a local AI model (Ollama) with Agent capabilities (RAG, Web Search, Exec).
    Calls callback(chunk_text, is_final)
    """
    if not AI_AVAILABLE:
        reply = fallback_reply(user_message.lower())
        callback(reply, True)
        return

    # Check RAG memory for context
    rag_context = memory_manager.query_memory(user_message)
    augmented_message = user_message
    if rag_context:
        augmented_message += f"\n\n[System Context from Memory: {rag_context}]"

    # Add message to history
    ai_history.append({"role": "user", "content": augmented_message})
    
    # Store plain message in memory manager for future
    memory_manager.add_memory(user_message)

    try:
        # Prepend system prompt to inject agent instructions
        messages_to_send = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}] + ai_history
        
        response_stream = ollama.chat(
            model="llama3.2",
            messages=messages_to_send,
            stream=True
        )
        
        full_reply = ""
        is_tool_call = False
        buffer_flushed = False
        
        for chunk in response_stream:
            content = chunk['message']['content']
            full_reply += content
            
            # Simple interception of tool calls with buffering
            if not is_tool_call and not buffer_flushed:
                if full_reply.startswith("[SEARCH:") or full_reply.startswith("[EXECUTE:"):
                    is_tool_call = True
                    continue
                elif "[SEARCH:".startswith(full_reply) or "[EXECUTE:".startswith(full_reply):
                    # Still building the tag, wait
                    continue
                else:
                    # Confirmed not a tool call, flush buffer
                    callback(full_reply, False)
                    buffer_flushed = True
                    continue

            if is_tool_call:
                continue # Do not stream tool calls to UI
            
            callback(content, False)
                
        # If it was a tool call, execute it and recurse once
        if is_tool_call:
            if full_reply.startswith("[SEARCH:"):
                query = full_reply.replace("[SEARCH:", "").replace("]", "").strip()
                search_results = perform_web_search(query)
                ai_history.append({"role": "assistant", "content": f"I need to search the web for {query}."})
                callback(f"🔍 Searching the web for: {query}...\n\n", False)
                
                # Recurse with system result
                ai_reply_stream(f"System Web Search Result:\n{search_results}\n\nBased on this, answer the original prompt.", callback)
                return
                
            elif full_reply.startswith("[EXECUTE:"):
                code = full_reply.replace("[EXECUTE:", "").replace("]", "").strip()
                result = sandbox.execute_code(code)
                ai_history.append({"role": "assistant", "content": f"I executed code: {code}"})
                callback(f"⚡ Executed code. Result:\n```text\n{result}\n```\n\n", False)
                
                # Recurse
                ai_reply_stream(f"System Execution Result:\n{result}\n\nBased on this, provide the next step or final answer.", callback)
                return

        # Finalize message
        ai_history.append({"role": "assistant", "content": full_reply})
        config.save_ai_history(ai_history)
        callback("", True) # Signal end of stream

    except Exception as e:
        callback(f"⚠️ AI error: {e}", True)

def clear_memory():
    """Clear AI history"""
    global ai_history
    ai_history = []
    config.save_ai_history(ai_history)

def code_explain_stream(code: str, callback):
    """Explain code using AI with a specialized system prompt."""
    if not AI_AVAILABLE:
        callback("⚠️ AI is not available. Install ollama to use code explanation.", True)
        return

    messages = [
        {"role": "system", "content": "You are a helpful code tutor. Explain the given code clearly and concisely. "
         "Break down what each part does. Use simple language. Keep it brief."},
        {"role": "user", "content": f"Explain this code:\n\n```\n{code}\n```"}
    ]

    try:
        stream = ollama.chat(model="llama3.2", messages=messages, stream=True)
        full = ""
        for chunk in stream:
            content = chunk["message"]["content"]
            full += content
            callback(content, False)
        callback("", True)
    except Exception as e:
        callback(f"⚠️ AI error: {e}", True)


def code_generate_stream(prompt: str, language: str, callback):
    """
    Generate code from a natural language prompt using AI.
    Calls callback(chunk_text, is_final) for streaming output.
    """
    if not AI_AVAILABLE:
        callback("⚠️ AI is not available. Install ollama to use code generation.\n\n"
                 "Run: pip install ollama\nThen: ollama pull llama3.2", True)
        return

    system_prompt = (
        f"You are an expert programmer and code generator. "
        f"The user will describe what they want and you must generate clean, "
        f"well-commented, production-ready {language} code.\n\n"
        f"Rules:\n"
        f"1. Output ONLY the code — no explanations before or after unless the user asks.\n"
        f"2. Use proper {language} conventions, idioms, and best practices.\n"
        f"3. Add clear, concise comments explaining key logic.\n"
        f"4. Include necessary imports/headers.\n"
        f"5. Make the code complete and runnable.\n"
        f"6. If the request is ambiguous, make reasonable assumptions and note them in comments."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    try:
        stream = ollama.chat(model="llama3.2", messages=messages, stream=True)
        full = ""
        for chunk in stream:
            content = chunk["message"]["content"]
            full += content
            callback(content, False)
        callback("", True)
    except Exception as e:
        callback(f"⚠️ Code generation error: {e}", True)

def summarize_stream(prompt: str, callback):
    """
    Generate a summary from a natural language prompt and content block.
    Calls callback(chunk_text, is_final) for streaming output.
    """
    if not AI_AVAILABLE:
        callback("⚠️ AI is not available. Install ollama to use the summarizer.\n\n"
                 "Run: pip install ollama\nThen: ollama pull llama3.2", True)
        return

    system_prompt = (
        "You are an expert executive assistant and data summarizer. "
        "The user will provide you with a long block of text (often from a website or a video transcript). "
        "Your task is to summarize the text precisely according to their requested format. "
        "Rules:\n"
        "1. Do NOT add filler conversation at the beginning (e.g. 'Here is your summary:').\n"
        "2. Do NOT hallucinate facts that are not present in the text.\n"
        "3. Output ONLY the summary.\n"
        "4. Be concise and prioritize the most critical information."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    try:
        stream = ollama.chat(model="llama3.2", messages=messages, stream=True)
        for chunk in stream:
            content = chunk["message"]["content"]
            callback(content, False)
        callback("", True)
    except Exception as e:
        callback(f"⚠️ Summarization error: {e}", True)

