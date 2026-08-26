import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
import time
import hashlib
from supabase import create_client, Client

# =========================================================
# SANKALP V2 - PAGE CONFIG MUST BE FIRST
# =========================================================
st.set_page_config(
    page_title="Sankalp",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STEP D: SUPABASE AUTHENTICATION (LOGIN/SIGNUP)
# =========================================================
@st.cache_resource
def init_connection():
    # .strip() lagane se koi bhi extra space ya 'Enter' khud hatt jayega
    url = st.secrets["SUPABASE_URL"].strip()
    key = st.secrets["SUPABASE_KEY"].strip()
    
    # Agar URL ke aakhir me '/' laga reh gaya ho, toh use bhi hata dega
    if url.endswith('/'):
        url = url[:-1]
        
    return create_client(url, key)

try:
    supabase: Client = init_connection()
except Exception as e:
    st.error("❌ Supabase connect nahi ho pa raha. Secrets check karein.")
    st.stop()

if 'user' not in st.session_state:
    st.session_state.user = None

def login_page():
    # 1. Logo dikhane ka code
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Aapka logo yahan show hoga
        st.image("1000094047.png", use_container_width=True)
        
    st.markdown("<h2 style='text-align: center;'>🔐 Sankalp - Login</h2>", unsafe_allow_html=True)
    
    choice = st.radio("Aap kya karna chahte hain?", ["Login", "Naya Account Banayein (Sign Up)"])
    
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    
    if choice == "Naya Account Banayein (Sign Up)":
        if st.button("Sign Up"):
            try:
                response = supabase.auth.sign_up({"email": email, "password": password})
                st.success("✅ Account ban gaya! Ab aap Login kar sakte hain.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                
    elif choice == "Login":
        if st.button("Login"):
            try:
                # Pehle Supabase se check karega ki password sahi hai ya nahi
                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                
                # Agar password sahi hai, tab 10 second ka loading animation chalega
                progress_text = "System secure kiya ja raha hai... Kripya pratiksha karein."
                my_bar = st.progress(0, text=progress_text)
                
                # 100 percentage tak jayega, har step mein 0.1 second rukega (Total 10 seconds)
                for percent_complete in range(100):
                    time.sleep(0.1) 
                    my_bar.progress(percent_complete + 1, text=f"Loading... {percent_complete + 1}%")
                
                st.success("✅ Login successful!")
                time.sleep(0.5) # Aadha second ruk kar dashboard khulega
                
                st.session_state.user = response.user
                st.rerun() 
            except Exception as e:
                st.error("❌ Galat Email ya Password. Kripya dobara check karein.")

# =========================================================
# YEH LINES MISSING THI - INKI WAJAH SE LOGIN RUKTA HAI
# =========================================================
if st.session_state.user is None:
    login_page()
    st.stop()


# =========================================================
# ORIGINAL APP STARTS HERE (Jab User Login ho jaye)
# =========================================================

DB_NAME = "sankalp.db"

# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()

def init_db():
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name TEXT DEFAULT 'User',
            start_date TEXT,
            best_streak INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            mood INTEGER,
            urge INTEGER,
            trigger TEXT,
            exercise INTEGER DEFAULT 0,
            meditation INTEGER DEFAULT 0,
            journal INTEGER DEFAULT 0,
            relapse INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            entry TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            intensity INTEGER,
            trigger TEXT,
            resisted INTEGER DEFAULT 0
        )
    """)

    # Create default user
    cursor.execute("SELECT COUNT(*) FROM user")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO user (id, name, start_date, best_streak)
            VALUES (1, 'User', ?, 0)
        """, (date.today().isoformat(),))

    conn.commit()

init_db()

# =========================================================
# HELPERS
# =========================================================

def today():
    return date.today().isoformat()

def get_user():
    return conn.execute(
        "SELECT * FROM user WHERE id = 1"
    ).fetchone()

def get_checkin(checkin_date=None):
    checkin_date = checkin_date or today()

    return conn.execute(
        "SELECT * FROM checkins WHERE date = ?",
        (checkin_date,)
    ).fetchone()

def save_checkin(
    mood, urge, trigger, exercise, meditation, journal_done, relapse
):
    conn.execute("""
        INSERT INTO checkins
        (date, mood, urge, trigger, exercise, meditation, journal, relapse)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            mood = excluded.mood,
            urge = excluded.urge,
            trigger = excluded.trigger,
            exercise = excluded.exercise,
            meditation = excluded.meditation,
            journal = excluded.journal,
            relapse = excluded.relapse
    """, (
        today(), mood, urge, trigger, int(exercise), int(meditation), int(journal_done), int(relapse)
    ))

    conn.commit()

def calculate_streak():
    rows = conn.execute("""
        SELECT date, relapse
        FROM checkins
        WHERE date <= ?
        ORDER BY date DESC
    """, (today(),)).fetchall()

    if not rows:
        user = get_user()
        start = datetime.fromisoformat(user["start_date"]).date()

        return max(0, (date.today() - start).days + 1)

    streak = 0
    current = date.today()

    row_dict = {row["date"]: row["relapse"] for row in rows}

    while True:
        d = current.isoformat()

        if d in row_dict and row_dict[d] == 1:
            break

        streak += 1
        current -= timedelta(days=1)

        # Avoid counting days before user's start date
        user = get_user()
        start_date = datetime.fromisoformat(
            user["start_date"]
        ).date()

        if current < start_date:
            break

    return streak

def calculate_best_streak():
    rows = conn.execute("""
        SELECT date, relapse
        FROM checkins
        ORDER BY date ASC
    """).fetchall()

    if not rows:
        return 0

    best = 0
    current_streak = 0
    previous_date = None

    for row in rows:

        d = datetime.fromisoformat(row["date"]).date()

        if row["relapse"] == 1:
            current_streak = 0
            previous_date = d
            continue

        if previous_date is not None:
            if d == previous_date + timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1
        else:
            current_streak = 1

        best = max(best, current_streak)
        previous_date = d

    return best

def total_clean_days():
    return conn.execute("""
        SELECT COUNT(*)
        FROM checkins
        WHERE relapse = 0
    """).fetchone()[0]

def total_resisted_urges():
    return conn.execute("""
        SELECT COUNT(*)
        FROM urges
        WHERE resisted = 1
    """).fetchone()[0]

def save_urge(intensity, trigger, resisted):
    conn.execute("""
        INSERT INTO urges
        (date, intensity, trigger, resisted)
        VALUES (?, ?, ?, ?)
    """, (
        today(), intensity, trigger, int(resisted)
    ))

    conn.commit()

def save_journal(entry):
    conn.execute("""
        INSERT INTO journal (date, entry)
        VALUES (?, ?)
    """, (
        today(), entry
    ))

    conn.commit()

def reset_streak():
    conn.execute(
        "UPDATE user SET start_date = ?, best_streak = 0 WHERE id = 1",
        (today(),)
    )

    conn.commit()

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
.main-title { font-size: 42px; font-weight: 800; text-align: center; margin-bottom: 0; }
.subtitle { text-align: center; color: #777; font-size: 18px; margin-bottom: 30px; }
.card { padding: 20px; border-radius: 18px; border: 1px solid rgba(128,128,128,0.25); margin-bottom: 15px; }
.big-number { font-size: 38px; font-weight: 800; }
.small-text { color: #777; }
.urge-box { padding: 25px; border-radius: 20px; text-align: center; border: 2px solid rgba(255,80,80,0.35); }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    # Safely email nikalne ka tarika
    try:
        if isinstance(st.session_state.user, dict):
            user_email = st.session_state.user.get("email", "User")
        else:
            user_email = getattr(st.session_state.user, "email", "User")
    except:
        user_email = "User"

    st.write(f"👤 Logged in as: **{user_email}**")
    
    if st.button("🚪 Logout", type="primary"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()
        
    st.divider()

    st.markdown("## 🧭 Sankalp")

    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = "Dashboard"
    if st.button("🚨 Urge Rescue", use_container_width=True):
        st.session_state.page = "Urge Rescue"
    if st.button("📔 Journal", use_container_width=True):
        st.session_state.page = "Journal"
    if st.button("📊 Progress", use_container_width=True):
        st.session_state.page = "Progress"
    if st.button("⚙️ Settings", use_container_width=True):
        st.session_state.page = "Settings"

    st.divider()
    st.caption("Sankalp V2")
    st.caption("Build discipline. Regain control.")

# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":
    st.markdown('<p class="main-title">🧭 SANKALP</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Take back your control.</p>', unsafe_allow_html=True)

    current_streak = calculate_streak()
    best_streak = calculate_best_streak()
    clean = total_clean_days()
    resisted = total_resisted_urges()

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🔥 Current Streak", f"{current_streak} days")
    with c2: st.metric("🏆 Best Streak", f"{best_streak} days")
    with c3: st.metric("🌱 Clean Days", clean)
    with c4: st.metric("🛡️ Urges Resisted", resisted)

    st.divider()

    st.markdown("""
    <div class="urge-box">
    <h2>🚨 Having an urge?</h2>
    <p>You don't need to fight the entire day.</p>
    <p>Just win the next few minutes.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚨 I HAVE AN URGE", type="primary", use_container_width=True):
        st.session_state.page = "Urge Rescue"
        st.rerun()

    st.divider()
    st.subheader("🌱 Today's Check-in")
    existing = get_checkin()

    with st.form("daily_checkin"):
        mood = st.slider("😊 How are you feeling today?", 1, 10, existing["mood"] if existing else 7)
        urge = st.slider("🔥 Urge intensity", 0, 10, existing["urge"] if existing else 0)
        trigger = st.selectbox("What was your biggest trigger?", ["None", "Boredom", "Loneliness", "Stress", "Anxiety", "Social Media", "Being alone", "Late night", "Other"])
        
        col1, col2, col3 = st.columns(3)
        with col1: exercise = st.checkbox("🏃 Exercise", value=bool(existing["exercise"]) if existing else False)
        with col2: meditation = st.checkbox("🧘 Meditation", value=bool(existing["meditation"]) if existing else False)
        with col3: journal_done = st.checkbox("📔 Journal", value=bool(existing["journal"]) if existing else False)
        
        relapse = st.checkbox("I relapsed today")
        submitted = st.form_submit_button("Save Today's Check-in", use_container_width=True)

        if submitted:
            save_checkin(mood, urge, trigger, exercise, meditation, journal_done, relapse)
            st.success("Today's check-in saved successfully.")
            st.rerun()

    st.divider()
    st.subheader("💡 Today's Reminder")
    reminders = [
        "An urge is temporary. Your decision doesn't have to be.",
        "You don't need motivation. You need one good decision.",
        "Protect your attention. Protect your future.",
        "One clean day at a time.",
        "Discipline becomes easier when repeated."
    ]
    import random
    st.info(random.choice(reminders))


# =========================================================
# URGE RESCUE
# =========================================================

elif st.session_state.page == "Urge Rescue":
    st.title("🚨 Urge Rescue")
    st.write("Don't negotiate with the urge. Give yourself a few minutes and let the intensity come down.")
    st.divider()
    
    st.subheader("Step 1 — Identify the urge")
    intensity = st.slider("How strong is the urge right now?", 0, 10, 5)
    trigger = st.selectbox("What triggered it?", ["Boredom", "Loneliness", "Stress", "Social Media", "Being alone", "Late night", "Random thought", "Other"])
    st.divider()
    
    st.subheader("Step 2 — 60 Second Breathing")
    st.write("Inhale slowly for 4 seconds, hold for 2 seconds, then exhale for 6 seconds.")
    
    if st.button("▶ Start 60 Second Rescue", type="primary", use_container_width=True):
        progress = st.progress(0)
        timer_text = st.empty()
        for i in range(60):
            remaining = 60 - i
            timer_text.markdown(f"<h1 style='text-align:center'>{remaining}</h1>", unsafe_allow_html=True)
            progress.progress((i + 1) / 60)
            time.sleep(1)
        timer_text.success("60 seconds completed. The urge does not control you.")
        
    st.divider()
    st.subheader("Step 3 — Change your environment")
    st.write("Choose one:")
    a, b, c = st.columns(3)
    with a: st.button("🚶 Go for a walk")
    with b: st.button("💪 Do 20 push-ups")
    with c: st.button("📵 Leave the phone")
    
    st.divider()
    st.subheader("Step 4 — What happened?")
    r1, r2 = st.columns(2)
    with r1:
        if st.button("🛡️ I RESISTED", use_container_width=True):
            save_urge(intensity, trigger, True)
            st.success("Excellent. You successfully rode out the urge.")
    with r2:
        if st.button("➡️ Still struggling", use_container_width=True):
            save_urge(intensity, trigger, False)
            st.warning("That's okay. Change your environment and repeat the rescue process.")


# =========================================================
# JOURNAL
# =========================================================

elif st.session_state.page == "Journal":
    st.title("📔 Recovery Journal")
    st.write("Write honestly. This journal is for understanding yourself, not judging yourself.")
    
    entry = st.text_area("Today's thoughts", height=220, placeholder="What happened today?\nWhat triggered you?\nWhat helped you?\nWhat will you do differently tomorrow?")
    
    if st.button("💾 Save Journal Entry", type="primary", use_container_width=True):
        if entry.strip():
            save_journal(entry)
            st.success("Journal entry saved.")
        else:
            st.warning("Please write something first.")
            
    st.divider()
    st.subheader("Previous Entries")
    entries = conn.execute("SELECT * FROM journal ORDER BY id DESC LIMIT 10").fetchall()
    
    if not entries:
        st.info("No journal entries yet.")
    else:
        for item in entries:
            with st.expander(item["date"]):
                st.write(item["entry"])


# =========================================================
# PROGRESS
# =========================================================

elif st.session_state.page == "Progress":
    st.title("📊 Your Progress")
    current = calculate_streak()
    best = calculate_best_streak()
    clean = total_clean_days()
    resisted = total_resisted_urges()

    c1, c2 = st.columns(2)
    with c1:
        st.metric("🔥 Current Streak", f"{current} days")
        st.metric("🌱 Clean Days", clean)
    with c2:
        st.metric("🏆 Best Streak", f"{best} days")
        st.metric("🛡️ Urges Resisted", resisted)

    st.divider()
    st.subheader("📅 Recovery Calendar")
    start_date = date.today() - timedelta(days=29)
    calendar_data = []
    
    for i in range(30):
        d = start_date + timedelta(days=i)
        row = get_checkin(d.isoformat())
        if row is None: status = "⚪"
        elif row["relapse"]: status = "🔴"
        elif row["urge"] >= 7: status = "🟡"
        else: status = "🟢"
        calendar_data.append(f"{d.strftime('%d %b')}: {status}")

    cols = st.columns(5)
    for i, item in enumerate(calendar_data):
        with cols[i % 5]:
            st.write(item)

    st.divider()
    st.subheader("🧠 Understanding Your Triggers")
    trigger_rows = conn.execute("SELECT trigger, COUNT(*) AS total FROM checkins WHERE trigger IS NOT NULL GROUP BY trigger ORDER BY total DESC").fetchall()
    
    if trigger_rows:
        for row in trigger_rows:
            st.write(f"**{row['trigger']}** — {row['total']} time(s)")
    else:
        st.info("Complete a few daily check-ins to see your patterns.")


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":
    st.title("⚙️ Settings")
    user = get_user()
    
    st.subheader("Profile")
    name = st.text_input("Your name", value=user["name"])
    
    if st.button("Save Profile"):
        conn.execute("UPDATE user SET name = ? WHERE id = 1", (name,))
        conn.commit()
        st.success("Profile updated.")
        
    st.divider()
    st.subheader("🔒 Content Protection")
    st.checkbox("Enable protection mode", value=False, help="This is currently only a UI setting. Actual device-level blocking will be implemented in the Android version.")
    
    st.divider()
    st.subheader("⚠️ Reset")
    st.warning("Resetting your streak changes the start date. Your journal and historical data will remain.")
    
    if st.button("Reset Current Streak", type="secondary"):
        reset_streak()
        st.success("Your new streak starts today.")
        st.rerun()

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption("Sankalp • One decision at a time.")
