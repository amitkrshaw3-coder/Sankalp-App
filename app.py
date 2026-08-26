import streamlit as st

# 1. Page ki nayi setting (Clean aur Modern look)
st.set_page_config(page_title="Sankalp App", page_icon="🌿", layout="centered")

# 2. Logo ko center me aur perfect size me karne ke liye Columns ka use
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("1000094047.png", use_container_width=True)

# 3. Main Title - Naye Premium Style ke sath
st.markdown("<h1 style='text-align: center; color: #4CAF50; font-size: 3.2em; font-weight: 800; margin-bottom: 0px;'>S A N K A L P</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #81C784; letter-spacing: 3px; margin-top: -10px;'>STRONG MIND • BETTER LIFE</h4>", unsafe_allow_html=True)

st.write("---")

# 4. Naya 'Dashboard' Tracker Look 
st.markdown("<h3 style='text-align: center;'>📊 Aapki Pragati</h3>", unsafe_allow_html=True)
st.text("") # Thodi space ke liye

m1, m2, m3 = st.columns(3)
m1.metric(label="🛡️ Protection", value="Secured", delta="Active")
m2.metric(label="🔥 No-Fap Streak", value="Day 1", delta="+1 Aaj")
m3.metric(label="🎯 Mind Score", value="100%", delta="Focused")

st.write("---")

# 5. Khubsurat Tabs (Colorful Highlight Boxes ke sath)
st.markdown("### 🧘 Sankalp Ke 4 Stambh")
tab1, tab2, tab3, tab4 = st.tabs(["🎯 FOCUS", "🛡️ DISCIPLINE", "🧘 CONTROL", "🏔️ FREEDOM"])

with tab1:
    st.info("**Focus (ध्यान):** Apne dhyan ko bhatakne na dein. Apna poora focus apni aage ki padhai, competitive exams, aur career goals par lagayein.")
with tab2:
    st.warning("**Discipline (अनुशासन):** Lagataar prayas hi safalta ki kunji hai. Har roz apna time-table follow karna aur bhatkaav se bachna hi asli discipline hai.")
with tab3:
    st.success("**Control (नियंत्रण):** Apne mind aur emotions ko control karein. Jab bhi kamzori mehsoos ho, lambi saans lein aur is app ko dekhein.")
with tab4:
    st.error("**Freedom (स्वतंत्रता):** Buri aadaton se azaadi hi asli azaadi hai. Ek baar yeh aadat chhut gayi, toh aap zindagi me kuch bhi hasil kar sakte hain.")
