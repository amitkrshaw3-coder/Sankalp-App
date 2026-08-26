import streamlit as st

# 1. Page Config (Dark Mode / Clean Look)
st.set_page_config(page_title="Sankalp App", page_icon="🌿", layout="centered")

# --- SIDEBAR NAVIGATION (Pages You Should Build wale section se inspired) ---
st.sidebar.image("1000094047.png", width=100)
st.sidebar.title("SANKALP")
page = st.sidebar.radio("Navigation", ["Dashboard", "Urge Help", "Recovery Journal", "Settings"])

# ==========================================
# PAGE 1: MAIN DASHBOARD (Home Screen)
# ==========================================
if page == "Dashboard":
    # Logo and Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
         st.image("1000094047.png", use_container_width=True)
         
    st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>S A N K A L P</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #81C784; font-size: 18px;'>Take back control of your mind.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Day 12 • Stay Strong</p>", unsafe_allow_html=True)
    
    st.write("---")

    # 1. Current Streak Section
    st.markdown("### 🔥 Current Streak")
    st.markdown("<h1 style='color: #4CAF50; font-size: 3.5rem; margin-top: -15px;'>12 Days</h1>", unsafe_allow_html=True)
    st.caption("Keep going — you're building discipline.")

    # 2. Metrics Section (Mind Score & Urges)
    m1, m2 = st.columns(2)
    with m1:
        st.metric(label="🧠 Mind Score", value="92%")
    with m2:
        st.metric(label="⚠️ Urges Today", value="1")

    st.write("---")

    # 3. Urge Button Section (When an urge hits)
    st.markdown("### 🚨 When an urge hits")
    st.info("Breathe • Delay • Move • Win")
    
    btn1, btn2 = st.columns(2)
    with btn1:
        st.button("🏃 Start Exercise", use_container_width=True, type="primary")
    with btn2:
        st.button("📞 Call Partner", use_container_width=True)

    st.write("---")

    # 4. Today's Growth
    st.markdown("### 🌱 Today's Growth")
    st.checkbox("📘 Read 10 pages")
    st.caption("Small wins beat strong urges.")

    st.write("---")

    # 5. Recovery Toolkit
    st.markdown("### 🛠️ Recovery Toolkit")
    tk1, tk2, tk3 = st.columns(3)
    with tk1:
        st.button("🧘 Meditate", use_container_width=True)
    with tk2:
        st.button("📓 Journal", use_container_width=True)
    with tk3:
        st.button("🎯 Goals", use_container_width=True)

# ==========================================
# PAGE 2: URGE HELP (Panic Button Page)
# ==========================================
elif page == "Urge Help":
    st.title("🚨 Emergency Urge Help")
    st.warning("Take a deep breath. You are stronger than your urges. Wait for 10 minutes before making any decision.")
    st.video("https://www.youtube.com/watch?v=inpok4MKVLM") # Calm breathing video example
    st.button("I feel better now, back to Dashboard")

# ==========================================
# PAGE 3 & 4: PLACEHOLDERS
# ==========================================
elif page == "Recovery Journal":
    st.title("📓 Recovery Journal")
    st.text_area("Write your daily thoughts, mood tracking, and triggers here...")
    st.button("Save Entry")

elif page == "Settings":
    st.title("⚙️ Settings")
    st.write("Smart Porn Blocker Settings:")
    st.checkbox("Enable DNS Filtering", value=True)
    st.checkbox("Strict Mode (No override)", value=False)
