import streamlit as st
import requests
import re
from collections import Counter
import time
import traceback

API_URL = "https://developergenz-voxira-backend.hf.space/auth"        # change to your backend url after deployment
BASE_API = "https://developergenz-voxira-backend.hf.space" 

st.set_page_config(
    page_title="Voxira AI",
    page_icon="icon.webp",  # Optional: Emoji as favicon
    layout="centered",
    initial_sidebar_state="expanded"
)

# ✅ HIDE STREAMLIT DEFAULT HEADER
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {height:0px;}
</style>
""", unsafe_allow_html=True)

#------------- REFRESH LOGIC ---------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
       
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "transcript" not in st.session_state:
    st.session_state.transcript = ""
    
if "show_history" not in st.session_state:
    st.session_state.show_history = False 
    
if "delete_confirm_id" not in st.session_state:
    st.session_state.delete_confirm_id = None 
    
if "generated_titles" not in st.session_state:
    st.session_state.generated_titles = {}          

# ---------- UI POLISH ----------
st.markdown("""
<style>

.block-container{
    padding-left:2rem;
}

/* ===== PAGE BACKGROUND ===== */
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#020617);
}

/* ===== LOGIN / SIGNUP CARD ===== */

.login-card{

    max-width:430px;
    margin:auto;
    margin-top:12vh;

    padding:40px 36px;

    border-radius:18px;

    /* subtle gradient panel */
    background:linear-gradient(
        160deg,
        rgba(30,41,59,0.95),
        rgba(15,23,42,0.95)
    );

    /* soft border highlight */
    border:1px solid rgba(148,163,184,0.18);

    /* premium depth */
    box-shadow:
        0 20px 45px rgba(0,0,0,0.6),
        0 0 0 1px rgba(59,130,246,0.08);

}

/* title */
.login-title{
    text-align:center;
    font-size:26px;
    font-weight:700;
    margin-bottom:28px;
    color:#f1f5f9;
}

/* inputs */
.login-card div[data-baseweb="input"] input{
    background:#020617 !important;
    border:1px solid #334155 !important;
    border-radius:8px !important;
    color:#e2e8f0 !important;
}

/* labels */
.login-card label{
    color:#cbd5f5 !important;
    font-weight:500;
}

/* buttons */
.login-card button{
    width:100%;
    margin-top:12px;
    border-radius:8px;
}

/* hover effect */
.login-card button:hover{
    transform:translateY(-1px);
    box-shadow:0 6px 16px rgba(59,130,246,0.35);
}

/* ===== PREMIUM AI GLOW BORDER ===== */

.login-card{
    position:relative;
    overflow:hidden;
}

/* glow layer */
.login-card::before{
    content:"";
    position:absolute;
    inset:-1px;

    border-radius:18px;

    background:linear-gradient(
        120deg,
        transparent,
        rgba(59,130,246,0.35),
        transparent
    );

    opacity:0.35;
    z-index:0;

    animation:cardGlow 6s linear infinite;
}

/* keep card content above glow */
.login-card > *{
    position:relative;
    z-index:1;
}

/* animation */
@keyframes cardGlow{
    0%{
        transform:translateX(-100%);
    }
    100%{
        transform:translateX(100%);
    }
}

/* HEADER */
.simple-header{
    background: linear-gradient(90deg,#3b82f6,#06b6d4);
    padding:18px;
    border-radius:14px;
    margin-bottom:30px;
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:700;
    box-shadow:0 6px 18px rgba(0,0,0,0.35);
}

/* REMOVE DARK STREAMLIT HEADER */
header[data-testid="stHeader"]{
    background:transparent;
}

h1, h2, h3, h4 {
    color: #f1f5f9 !important;
}

.stMarkdown {
    color:#e2e8f0;
}   

/* ---------- MODERN BUTTON ---------- */
div.stButton > button{
    width:100%;
    background:linear-gradient(90deg,#2563EB,#3b82f6);
    color:white;
    border:none;
    height:42px;
    border-radius:10px;
    font-weight:600;
    transition:all .25s ease;
}

div.stButton > button{
    width:100%;
    background:linear-gradient(90deg,#2563EB,#3b82f6);
    color:white;
    border:none;
    height:42px;
    border-radius:10px;
    font-weight:600;
    transition:all .25s ease;
}

div.stButton > button:hover{
    transform:translateY(-2px);
    box-shadow:0 8px 20px rgba(59,130,246,0.5);
}

/* ---- CLICK EFFECT ---- */
div.stButton > button:active {
    transform: scale(0.97);
}

/* ===== SIGNUP BUTTON ===== */
.signup-btn{
    text-align:center;
    margin-top:18px;
}

/* ===== TEXT COLOR ===== */
label{
    color:#e2e8f0 !important;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#0f172a,#020617);
    border-right:3px solid #3b82f6;
    box-shadow:4px 0 18px rgba(0,0,0,0.6);
    padding-top:20px;
    position:relative;
    z-index:100;
}

/* sidebar text */
section[data-testid="stSidebar"] *{
    color:#E5E7EB !important;
}

/* toggle button */
button[data-testid="collapsedControl"]{
    background:#3b82f6 !important;
    border-radius:10px !important;
    padding:8px !important;
    position:fixed;
    left:12px;
    top:14px;
    border:1px solid white;
    box-shadow:0 4px 12px rgba(0,0,0,0.7);
}

button[data-testid="collapsedControl"] svg{
    color:white !important;
    width:24px !important;
    height:24px !important;
}

/* hover */
button[data-testid="collapsedControl"]:hover{
    background:#2563eb !important;
}

/* ===== SIDEBAR BUTTON STYLE ===== */
section[data-testid="stSidebar"] button{
    background:#020617 !important;
    border:1px solid #1f2937 !important;
    border-radius:8px;
}

/* sidebar icons spacing */
section[data-testid="stSidebar"] button p{
    display:flex;
    align-items:center;
    gap:10px;
}

/* icon visibility */
button[data-testid="collapsedControl"] svg{
    color:white !important;
    width:24px; !important;
    height:24px; !important;
}

/* icon highlight */
section[data-testid="stSidebar"] button p::first-letter{
    background:#111827;
    padding:4px 6px;
    border-radius:6px;
    margin-right:6px;
    box-shadow:0 0 6px rgba(59,130,246,0.5);
}

/* ---------- HISTORY BUTTON ---------- */
section[data-testid="stSidebar"] button{
    background:#020617 !important;
    border:1px solid #1f2937 !important;
}

/* FOOTER */
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 52px;

    background: linear-gradient(90deg,#2563EB,#3b82f6);

    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 36px;
    font-size: 14px;
    z-index: 1000;

    box-shadow:0 -3px 12px rgba(0,0,0,0.35);
}

/* Links */
.footer a {
    margin:0 15px;
    text-decoration: none;
    font-weight: 500;
    color:white !important;
}

.footer a:hover {
    color:#facc15 !important;
}

/* MAKE ICON CLEAR */
.footer img{
    width:26px;
    height:26px;
    transition:0.2s;
}

.footer img:hover{
    transform:scale(1.15);
}

/* ===== FILE UPLOADER BOX FIX ===== */
[data-testid="stFileUploader"]{
    background:rgba(15,23,42,0.85);
    border:2px dashed #3b82f6;
    padding:18px;
    border-radius:12px;
}

/* upload text */
[data-testid="stFileUploader"] label{
    color:white !important;
    font-weight:600;
}

/* ===== SPINNER FIX ===== */
div[data-testid="stSpinner"]{
    background:rgba(15,23,42,0.9);
    padding:14px 20px;
    border-radius:10px;
    border:1px solid #334155;
    display:inline-flex;
    align-items:center;
    gap:10px;
}

/* spinner text */
div[data-testid="stSpinner"] span{
    color:#f1f5f9 !important;
    font-weight:500;
}

/* ===== STATUS TEXT BOX ===== */
.element-container:has(div[data-testid="stMarkdownContainer"]){
    color:#e2e8f0;
}

/* progress bar stronger */
div[data-testid="stProgress"] > div > div{
    background:#3b82f6 !important;
}

/* ===== UPLOAD CONTAINER CARD ===== */
div[data-testid="stVerticalBlock"]:has([data-testid="stFileUploader"]){
    background:rgba(255,255,255,0.04);
    padding:20px;
    border-radius:14px;
    border:1px solid #1f2937;
}

/* header action buttons */
div[data-testid="stHorizontalBlock"] button{
    margin-top:6px;
} 

</style>
""", unsafe_allow_html=True)
 
#------------------------ LOGIN PAGE ------------------------------
def login_page():

    left, center, right = st.columns([1,2,1])

    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-title">🎙 Voxira AI</div>', unsafe_allow_html=True)

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("🔐 Login", key="login_btn"):
            res = requests.post(
                f"{API_URL}/login",
                data={
                    "email": email.strip(),
                    "password": password.strip()
                }
            )

            if res.status_code == 200:
                st.session_state.token = res.json()['token']
                st.session_state.page = "dashboard"
                st.session_state.user_id = email.split("@")[0]
                st.rerun()
            else:
                st.error("Invalid login")

        if st.button("No account? Sign Up", key="goto_signup"):
            st.session_state.page = "signup"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.sidebar.empty()

#----------------------------- SIGNUP PAGE ------------------------------------
def signup_page():

    left, center, right = st.columns([1,2,1])

    with center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-title">Create Account</div>', unsafe_allow_html=True)

        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("📝Create Account", key="create_account_btn"):

            res = requests.post(
                f"{API_URL}/signup",
                data={
                    "email": email.strip(),
                    "password": password.strip()
                }
            )

            if res.status_code == 200:
                st.success("Account created. Please login.")
            else:
                st.error(res.text)

        if st.button("⇦ Back to Login", key="back_login_btn"):
            st.session_state.page = "login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.sidebar.empty()
                
# ----------------- TITLE GENERATION --------------------
def generate_history_title(text: str):

    if not text:
        return "Audio Transcript"

    # clean text
    text = re.sub(r"\s+", " ", text).strip()

    # split sentences
    sentences = re.split(r'[.!?]', text)

    # remove very short / useless sentences
    sentences = [
        s.strip() for s in sentences
        if len(s.split()) > 4
    ]

    if not sentences:
        return "Audio Transcript"

    # prefer early meaningful sentence (like ChatGPT)
    main_sentence = sentences[0][:120].lower()

    # remove filler speech words
    fillers = {
        "hello","hi","okay","yeah","um","uh","so",
        "actually","basically","like","you know"
    }

    words = [
        w for w in re.findall(r"\b[a-zA-Z]{4,}\b", main_sentence)
        if w.lower() not in fillers
    ]

    if not words:
        return "Audio Transcript"

    # take first strong keywords (not most frequent)
    keywords = words[:6]

    # professional formatting
    title = " ".join(word.capitalize() for word in keywords)

    return title           

# ================= DASHBOARD =================
def dashboard():

    # ---------- HEADER ----------
    st.markdown(
        '<div class="simple-header">🎙 Voxira AI Dashboard</div>',
        unsafe_allow_html=True
    )

    # ---------- HEADER ACTION BUTTONS ----------
    col_space, col_new, col_logout = st.columns([6,1.5,1.5])

    with col_new:
        if st.button("➕ New"):
            st.session_state.transcript = ""
            st.session_state.youtube_url = ""
            st.session_state.uploader_key += 1
            st.rerun()

    with col_logout:
        if st.button("⏻ Logout"):
            st.session_state.clear()
            st.session_state.page = "login"
            st.rerun()

    # ================= SIDEBAR HISTORY =================
    st.sidebar.title("📜 History")

    user_id = st.session_state.get("user_id", "test-user")

    try:
        response = requests.get(
            f"{BASE_API}/history",
            params={"user_id": user_id}
        )

        data = response.json()
        transcripts = data.get("transcripts", {})

    except Exception:
        transcripts = {}

    # ---------- SHOW HISTORY ----------
    if transcripts:

        # ✅ SORT BY TIMESTAMP (NEWEST FIRST)
        sorted_history = sorted(
            transcripts.items(),
            key=lambda x: x[1].get("timestamp", 0),
            reverse=True
        )

        for history_id, entry in sorted_history:

            if not isinstance(entry, dict):
                continue

            raw_text = entry.get("transcript") or ""
            clean_text = re.sub("<.*?>", "", raw_text)

            title = entry.get("title")

            # ✅ check locally generated titles
            if not title:
                title = st.session_state.generated_titles.get(history_id)

            # ✅ GENERATE TITLE ONLY ONCE
            if (
                not title
                and history_id not in st.session_state.generated_titles
                and clean_text
                and len(clean_text) > 20
            ):
                title = generate_history_title(clean_text)

                # store locally immediately
                st.session_state.generated_titles[history_id] = title

                # save to backend once
                requests.post(
                    f"{BASE_API}/history/set-title",
                    data={
                        "user_id": user_id,
                        "history_id": history_id,
                        "title": title
                    }
                )

            # ✅ FINAL SAFETY FALLBACK
            if not title:
                title = "Audio Transcript"

            with st.sidebar.container():

                col1, col2 = st.sidebar.columns([4,1])
    

                # ---------- OPEN TRANSCRIPT ----------
                with col1:
                    if st.button(
                        f"🎧 {title}",
                        key=f"open_{history_id}",
                        use_container_width=True
                    ):
                        st.session_state.transcript = clean_text
                        st.rerun()

                # ---------- DELETE ----------
                with col2:

                    # FIRST CLICK → ask confirmation inline
                    if st.session_state.get("delete_confirm_id") == history_id:

                        st.markdown("Confirm?")

                        c1, c2 = st.columns([1,1])

                        if c1.button("✅", key=f"yes_{history_id}", use_container_width=True):
                            requests.delete(
                                f"{BASE_API}/history/delete",
                                params={
                                    "user_id": user_id,
                                    "history_id": history_id
                                }
                            )
                            st.session_state.delete_confirm_id = None
                            st.toast("Deleted ✅")
                            st.rerun()

                        if c2.button("❌", key=f"no_{history_id}", use_container_width=True):
                            st.session_state.delete_confirm_id = None
                            st.rerun()

                    else:
                        if st.button("🗑", key=f"side_del_{history_id}", use_container_width=True):
                            st.session_state.delete_confirm_id = history_id
                            st.rerun()
    else:
        st.sidebar.info("No history yet")

    # -------- UPLOAD --------
    with st.container(border=True):

        uploaded_file = st.file_uploader(
            "Upload Audio / Video",
            type=["mp3", "wav", "mp4", "m4a"],
            key=st.session_state.uploader_key
        )

        url_input = st.text_input(
                "Or paste YouTube URL",
                key="youtube_url"
        )

        if url_input:
            st.info("Only Youtube Videos Under 10 minutes are supported.")

        if st.button("🚀 Transcribe", use_container_width=True):

            if url_input and not any(x in url_input for x in ["youtube.com","youtu.be"]):
                st.error("Invalid YouTube URL")
                st.stop()

            with st.spinner("Transcribing..."):

                files = None
                data = {"user_id": user_id}
                
                # ✅ initialize
                progress = None
                status = None
                
                # ------------------ FILE UPLOAD ----------------------------
                if uploaded_file:
                    
                    progress = st.progress(10)
                    status = st.empty()
                    status.write("📤 Uploading file...")
                    time.sleep(0.8)
                    
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    }
                    
                    progress.progress(50)
                    status.write("🚀 Sending audio for transcription...")
                    time.sleep(0.8)
                
                # ------------------ YOUTUBE URL -----------------------------
                elif url_input:

                    try:
                        import yt_dlp
                        import os
                        import uuid
                        import tempfile
                        
                        progress = st.progress(0)
                        status = st.empty()
                        
                        status.write("🔍 Checking video duration...")
                        progress.progress(10)
                        time.sleep(0.7)

                        # Create unique temp filename
                        temp_filename = os.path.join(
                            tempfile.gettempdir(),
                            f"{uuid.uuid4()}.mp3"
                        )

                        # ------------------ CHECK VIDEO DURATION FIRST ------------------
                        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                            info = ydl.extract_info(url_input.strip(), download=False)
                            if not info or "duration" not in info:
                                raise Exception("Failed to fetch video metadata")

                            duration = info["duration"]

                        duration_minutes = int(duration // 60)
                        duration_seconds = int(duration % 60)
                        
                        progress.progress(30)
                        time.sleep(0.8)

                        # Allow only up to 10 minutes
                        if duration > 600:  # 10 minutes
                            st.error(
                                f"This video is {duration_minutes} min {duration_seconds} sec long.\n"
                                "For optimal performance, only videos under 10 minutes are supported."
                            )
                            progress.empty()
                            status.empty()
                            st.stop()
                        
                        status.write("⬇️ Downloading audio from YouTube...")
                        progress.progress(50)
                        time.sleep(1)
                        
                        # ------------------ DOWNLOAD FULL AUDIO ------------------
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': temp_filename,
                            'quiet': True,
                            'noplaylist': True,
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url_input.strip()])
                            
                        progress.progress(70)
                        status.write("📂 Preparing audio file...")
                        time.sleep(0.8)
                        
                        # Read downloaded file
                        with open(temp_filename, "rb") as f:
                            file_bytes = f.read()

                        os.remove(temp_filename)
                        
                        files = {
                            "file": (
                                "downloaded_audio.mp3",
                                file_bytes,
                                "audio/mpeg"
                            )
                        }
                        
                        progress.progress(90)
                        status.write("🚀 Sending audio for transcription...")
                        time.sleep(0.8)
                        
                    except Exception as e:
                        
                        if progress:
                            progress.empty()
                            
                        if status:    
                            status.empty()
                            
                        st.error("Failed to download YouTube audio.")
                        st.code(traceback.format_exc())
                        st.write(str(e))
                        st.stop()

                # --------------------- TRANSCRIBE -------------------------------
                try:
                    
                    if not files:
                        st.error("No audio file provided.")
                        st.stop()
                        
                    if progress:
                        progress.progress(95)
                        
                    if status:    
                        status.write("🧠 AI is transcribing the audio...")
                    
                    response = requests.post(
                        f"{BASE_API}/transcribe/",
                        files=files,
                        data=data,
                        timeout=1800
                    )

                    result = response.json()

                    if response.status_code == 200 and "transcript" in result:
                        
                        if progress:
                            progress.progress(100)
                            
                        if status:
                            status.write("✅ Transcription completed")
                        
                        time.sleep(1)  # allow user to see 100%
                        
                        st.session_state.transcript = result["transcript"]
                        st.success("✅ Transcription Completed")
                        
                        # ✅ hide progress UI after finishing
                        if progress:
                            progress.empty()
                            
                        if status:    
                            status.empty()
                    else:
                        st.error(result)

                except requests.exceptions.RequestException as e:
                    
                    if progress:
                        progress.empty()
                        
                    if status:
                        status.empty()
                        
                    st.error("Backend server not running.")
                    st.write(str(e))

    #------------------------ 🌍 SHOW TRANSCRIPT -------------------------------------------------
    if "transcript" in st.session_state:

        st.markdown("### 📝 Transcript")
        
        with st.container(border=True):
            st.text_area(
                "Transcript Output",
                st.session_state.transcript,
                height=300
            )

        # Download transcript
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "📥 Download Transcript",
                st.session_state.transcript,
                file_name="transcript.txt",
                mime="text/plain"
            )
        
        with col2:
            if st.button("📋 Copy Transcript", key="copy_transcript_btn"):
                st.code(st.session_state.transcript)
                st.success("Select the text above and copy.")
        
        #------------------------ 🌐 TRANSLATION -------------------------------------------- 
        st.markdown("---")
        st.subheader("🌐 Translate Transcript to Other Languages")

        languages = {
            "Tamil": "ta", "Hindi": "hi", "French": "fr",
            "German": "de", "Spanish": "es", "Chinese": "zh-cn", "Arabic": "ar",
            "Japanese": "ja", "Korean": "ko", "Telugu": "te", "Malayalam": "ml"
        }
        
        cols = st.columns(4)
        i = 0

        for lang, code in languages.items():
            if cols[i % 4].button(lang):

                text_to_translate = st.session_state.get("transcript", "")

                if not text_to_translate.strip():
                    st.error("Transcript empty. Please transcribe first.")
                    st.stop()

                with st.spinner(f"Translating to {lang}..."):

                    res = requests.post(
                        f"{BASE_API}/translate/",
                        data={
                            "user_id": user_id,
                            "text": text_to_translate,
                            "target_lang": code
                        },
                        timeout=120
                    )

                    if res.status_code != 200:
                        st.error(f"Server error: {res.text}")
                        st.stop()

                    result = res.json()

                    if "translated" in result:
                        st.text_area(
                            f"{lang} Translation",
                            result["translated"],
                            height=220
                        )

                        st.download_button(
                            f"📥 Download {lang} Translation",
                            result["translated"],
                            file_name=f"{lang}_translation.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"Translation failed: {result}")
            i += 1
    else:
        st.info("👉 Transcribe a file to enable translation.")
        
    #------------------------ FOOTER -------------------------------------
    st.markdown("""
    <div class="footer">
        <div>© Hemadharshini • 2026 Voxira AI</div>
    <div>
        <a href="https://github.com/hemaxplore" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/733/733553.png" alt="GitHub" style="width: 26px; vertical-align: middle;">
        </a>
        <a href="https://www.linkedin.com/in/hemadharshini21/" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width: 26px; vertical-align: middle;">
        </a>
        <a href="mailto:darshinihema2102@gmail.com">
            <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" alt="Email" style="width: 26px; vertical-align: middle;">
        </a>
    </div>
    </div>
    """, unsafe_allow_html=True)  
    
# Hide sidebar on login/signup
if st.session_state.page != "dashboard":
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display:none;}
    </style>
    """, unsafe_allow_html=True)        
        
# ================= ROUTING =================
if "page" not in st.session_state:
    st.session_state.page = "login"

if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "signup":
    signup_page()

elif st.session_state.page == "dashboard":

    dashboard()       
