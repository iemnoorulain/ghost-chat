import customtkinter as ctk
import tkinter as tk
import threading
import urllib.parse
from bs4 import BeautifulSoup
import requests
from youtube_transcript_api import YouTubeTranscriptApi

import config
import ai_handler

def extract_youtube_video_id(url):
    """Extract the video ID from various forms of YouTube URLs."""
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            qs = urllib.parse.parse_qs(parsed_url.query)
            return qs.get('v', [None])[0]
        if parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        if parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]
    return None

def fetch_content(url):
    """Fetch and return text content from either a YouTube URL or a standard webpage."""
    yt_id = extract_youtube_video_id(url)
    if yt_id:
        try:
            api = YouTubeTranscriptApi()
            transcript = api.fetch(yt_id)
            text = " ".join([snippet.text for snippet in transcript.snippets])
            
            # Remove excessive blank spaces/newlines that might come from captions
            import re
            text = re.sub(r'\s+', ' ', text)
            
            return text, "YouTube Video"
        except Exception as e:
            return None, f"Could not fetch YouTube transcript. Ensure the video has closed captions. Error: {e}"
    
    # Generic Web Page Scraper
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove noisy elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text(separator=' ', strip=True)
        # remove excessive blank spaces
        import re
        text = re.sub(r'\s+', ' ', text)
        return text, soup.title.string if soup.title else "Web Article"
    except Exception as e:
        return None, f"Error fetching webpage: {e}"


def launch_summarizer(root):
    t = config.themes[config.settings["theme_index"]]

    win = ctk.CTkToplevel(root)
    win.title("🌐 Web & YouTube Summarizer")
    win.geometry("750x650")
    win.minsize(600, 500)
    win.configure(fg_color=t["bg"])
    win.attributes("-topmost", True)

    generating = [False]

    # ══════════════════════ HEADER ══════════════════════
    header = ctk.CTkFrame(win, fg_color=t["sidebar"], height=50, corner_radius=0)
    header.pack(fill="x")
    ctk.CTkLabel(header, text="🌐  URL Summarizer", font=("Segoe UI", 18, "bold"),
                 text_color=t["accent"]).pack(side="left", padx=20, pady=12)

    status_label = ctk.CTkLabel(header, text="Ready", font=("Segoe UI", 11),
                                text_color=t["muted"])
    status_label.pack(side="right", padx=20)

    # ══════════════════════ INPUT AREA ══════════════════════
    controls = ctk.CTkFrame(win, fg_color="transparent")
    controls.pack(fill="x", padx=20, pady=(15, 5))
    
    url_input = ctk.CTkEntry(
        controls, placeholder_text="Paste a YouTube or Article link here...",
        height=40, font=("Segoe UI", 13),
        fg_color=t["input_bg"], text_color=t["fg"],
        border_color=t["input_border"]
    )
    url_input.pack(side="left", fill="x", expand=True, padx=(0, 10))

    summarize_btn = ctk.CTkButton(
        controls, text="✨ Summarize", height=40, width=120,
        corner_radius=8, font=("Segoe UI", 13, "bold"),
        fg_color=t["accent"], hover_color=t["accent_hover"], text_color="#fff",
        command=lambda: start_summary(),
    )
    summarize_btn.pack(side="right")

    # ══════════════════════ OPTIONS AREA ══════════════════════
    options_frame = ctk.CTkFrame(win, fg_color="transparent")
    options_frame.pack(fill="x", padx=20, pady=5)
    
    ctk.CTkLabel(options_frame, text="Format:", font=("Segoe UI", 12, "bold"),
                 text_color=t["fg"]).pack(side="left", padx=(0, 10))
                 
    style_var = ctk.StringVar(value="Detailed Summary")
    styles = ["Detailed Summary", "Bullet Points", "Executive Summary", "Key Takeaways"]
    
    for s in styles:
        rb = ctk.CTkRadioButton(
            options_frame, text=s, variable=style_var, value=s,
            font=("Segoe UI", 12), text_color=t["fg"],
            fg_color=t["accent"], hover_color=t["accent_hover"]
        )
        rb.pack(side="left", padx=(0, 15))


    # ══════════════════════ OUTPUT AREA ══════════════════════
    output_container = ctk.CTkFrame(win, fg_color="transparent")
    output_container.pack(fill="both", expand=True, padx=20, pady=10)
    
    output_header = ctk.CTkFrame(output_container, fg_color="transparent")
    output_header.pack(fill="x", pady=(0, 5))
    
    title_label = ctk.CTkLabel(output_header, text="📄 Summary Output", font=("Segoe UI", 12, "bold"), text_color=t["fg"])
    title_label.pack(side="left")
    
    copy_btn = ctk.CTkButton(
        output_header, text="📋 Copy", height=28, width=80,
        corner_radius=8, font=("Segoe UI", 11),
        fg_color=t["btn"], hover_color=t["btn_hover"], text_color=t["fg"],
        command=lambda: copy_output(),
    )
    copy_btn.pack(side="right")

    summary_box = ctk.CTkTextbox(
        output_container, corner_radius=10,
        fg_color=t["card"], text_color=t["fg"],
        border_color=t["input_border"], border_width=2,
        font=("Segoe UI", 14),
        wrap="word",
    )
    summary_box.pack(fill="both", expand=True)

    # ══════════════════════ LOGIC ══════════════════════

    def copy_output():
        text = summary_box.get("1.0", "end-1c")
        if text.strip():
            win.clipboard_clear()
            win.clipboard_append(text)
            status_label.configure(text="✅ Copied to clipboard!", text_color=t.get("success", "#22c55e"))
            win.after(2000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))

    def start_summary():
        if generating[0]:
            return
            
        url = url_input.get().strip()
        if not url:
            status_label.configure(text="⚠️ Enter a URL first!", text_color=t.get("warning", "#fbbf24"))
            win.after(2000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))
            return

        # Prepare UI
        generating[0] = True
        summary_box.configure(state="normal")
        summary_box.delete("1.0", "end")
        summarize_btn.configure(text="⏳ Fetching...", state="disabled", fg_color=t["btn"])
        status_label.configure(text="Downloading content...", text_color=t["accent"])
        title_label.configure(text="📄 Fetching Content...")
        win.update()

        def _worker():
            # 1. Fetch content
            content, source_title = fetch_content(url)
            
            if not content:
                # content is None, source_title holds the error
                win.after(0, lambda: _handle_error(source_title))
                return
                
            # 2. Limit content length to prevent completely blowing out context window
            MAX_CHARS = 40000 
            if len(content) > MAX_CHARS:
                content = content[:MAX_CHARS] + "... [Content truncated for length]"
                
            win.after(0, lambda: _start_ai_stream(content, source_title))

        threading.Thread(target=_worker, daemon=True).start()

    def _handle_error(err_msg):
        generating[0] = False
        summarize_btn.configure(text="✨ Summarize", state="normal", fg_color=t["accent"])
        status_label.configure(text="⚠️ Error fetching URL", text_color=t.get("danger", "#f87171"))
        summary_box.insert("end", err_msg)
        title_label.configure(text="📄 Summary Output")

    def _start_ai_stream(content, source_title):
        title_label.configure(text=f"📄 {source_title}")
        summarize_btn.configure(text="⏳ Generating...")
        status_label.configure(text="AI is summarizing...")
        
        style = style_var.get()
        prompt = f"Please provide a {style} of the following content. Make it clear and easy to read. Do NOT add filler conversation at the beginning, just output the facts directly.\n\nCONTENT:\n{content}"
        
        # Use the dedicated summarization AI stream
        threading.Thread(
            target=ai_handler.summarize_stream,
            args=(prompt, _stream_cb),
            daemon=True,
        ).start()

    def _stream_cb(chunk, is_done):
        win.after(0, lambda: _update_stream_ui(chunk, is_done))
        
    def _update_stream_ui(chunk, is_done):
        if not is_done:
            summary_box.insert("end", chunk)
            summary_box.see("end")
        else:
            if chunk: 
                summary_box.insert("end", chunk)
            generating[0] = False
            summarize_btn.configure(text="✨ Summarize", state="normal", fg_color=t["accent"])
            status_label.configure(text="✅ Done!", text_color=t.get("success", "#22c55e"))
            win.after(3000, lambda: status_label.configure(text="Ready", text_color=t["muted"]))

    # Bind Enter
    def on_enter(e):
        start_summary()
        return "break"
    
    url_input.bind("<Return>", on_enter)
    win.after(100, lambda: url_input.focus())
