import streamlit as st
from datetime import date, timedelta
from views import dashboard, task_engine, focus_mode, analytics
from utils.db_supabase import supabase

st.set_page_config(page_title="Sankalp - Student OS", page_icon="🎯", layout="wide")

# --- NAYA CODE: get_streak ab user_name accept karega aur data filter karega ---
def get_streak(user_name):
    try:
        # NAYA: .eq("user_name", user_name) add kiya gaya hai
        response = supabase.table("study_sessions").select("session_date").eq("user_name", user_name).execute()
        if not response.data:
            return 0
            
        study_dates = {session['session_date'] for session in response.data}
        streak = 0
        check_date = date.today()
        
        if str(check_date) in study_dates:
            streak += 1
            check_date -= timedelta(days=1)
        elif str(check_date - timedelta(days=1)) not in study_dates:
            return 0
        else:
            check_date -= timedelta(days=1)
            
        while str(check_date) in study_dates:
            streak += 1
            check_date -= timedelta(days=1)
            
        return streak
    except Exception as e:
        return 0

# --- Login Page UI ---
def login_page():
    st.title("🔐 Welcome to Sankalp")
    st.markdown("Please log in to your Student OS.")
    
    with st.form("login_form"):
        name = st.text_input("Enter your Name", placeholder="e.g. Amit")
        submit = st.form_submit_button("Enter App 🚀")
        
        if submit and name:
            # User ka naam session mein save kar liya
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.rerun() # App ko refresh karo taaki dashboard khule

def main():
    # Session state initialization
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_name = ""

    # Agar login nahi hai, toh sirf login page dikhao aur code yahin rok do
    if not st.session_state.logged_in:
        login_page()
        return 

    # --- Yahan se Main App shuru hota hai (Only for logged in users) ---
    st.sidebar.title("🎯 Sankalp")
    st.sidebar.write(f"👤 **{st.session_state.user_name}**") # Sidebar mein bhi naam dikhega
    st.sidebar.markdown("---")
    
    menu = ["🏠 Dashboard", "📚 Task Engine", "⏱️ Focus Mode", "📊 Analytics"]
    choice = st.sidebar.radio("Go to", menu)
    
    st.sidebar.markdown("---")
    
    # NAYA: Function ko call karte waqt user ka naam bhejna hai
    current_streak = get_streak(st.session_state.user_name)
    
    if current_streak == 0:
        st.sidebar.info("🧊 Study Streak: 0 Days. Start today!")
    elif current_streak < 3:
        st.sidebar.info(f"🔥 Study Streak: {current_streak} Days. Good start!")
    else:
        st.sidebar.success(f"🔥 Study Streak: {current_streak} Days. You're on fire!")

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
