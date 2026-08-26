import streamlit as st

# Page ki setting aur title
st.set_page_config(page_title="Sankalp App", page_icon="🌿")

# Aapka bheja hua Logo display karna
st.image("1000094047.png", use_column_width=True)

# Main Title aur Subtitle
st.markdown("<h1 style='text-align: center; color: white;'>S A N K A L P</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: lightgreen;'>STRONG MIND • BETTER LIFE</h4>", unsafe_allow_html=True)

st.write("---")

# Protection Status Section
st.markdown("### 🛡️ Current Status")
st.success("Protection Active: Aap bilkul sahi raste par hain!")

# Logo me diye gaye 4 pillars (Tabs)
tab1, tab2, tab3, tab4 = st.tabs(["🎯 FOCUS", "🛡️ DISCIPLINE", "🧘 CONTROL", "🏔️ FREEDOM"])

with tab1:
    st.write("**Focus:** Apne dhyan ko bhatakne na dein. Aaj ka din apne goals ko samarpit karein.")
with tab2:
    st.write("**Discipline:** Lagataar prayas hi safalta ki kunji hai. Apne raste par date rahein.")
with tab3:
    st.write("**Control:** Apne mind ko control karein, usko aap par control na karne dein.")
with tab4:
    st.write("**Freedom:** Buri aadaton se azaadi hi asli azaadi hai.")
