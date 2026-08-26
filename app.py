import streamlit as st

# Page Config
st.set_page_config(page_title="Sankalp - Student OS", page_icon="🎯", layout="wide")

# Modular Imports
from views import dashboard, task_engine, focus_mode, analytics

def main():
    st.sidebar.title("🎯 Sankalp")
    st.sidebar.markdown("---")
    
    # Navigation
    menu = ["🏠 Dashboard", "📚 Task Engine", "⏱️ Focus Mode", "📊 Analytics"]
    choice = st.sidebar.radio("Go to", menu)
    
    st.sidebar.markdown("---")
    st.sidebar.info("🔥 Study Streak: 12 Days")

    # Routing
    if choice == "🏠 Dashboard":
        dashboard.render_dashboard()
    elif choice == "📚 Task Engine":
        task_engine.render_tasks()
    elif choice == "⏱️ Focus Mode":
        focus_mode.render_timer()
    elif choice == "📊 Analytics":
        analytics.render_analysis()

if __name__ == "__main__":
    main()
