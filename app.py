import streamlit as st
from datetime import date, timedelta
from views import dashboard, task_engine, focus_mode, analytics
from utils.db_supabase import supabase

st.set_page_config(page_title="Sankalp - Student OS", page_icon="🎯", layout="wide")

def get_streak(user_name):
    try:
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

# --- NAYA CODE: Advanced Auth System (Login & Sign Up) ---
def auth_page():
    st.title("🔐 Welcome to Sankalp")
    st.markdown("Your Personal Student OS. Please log in or create an account.")
    
    tab_login, tab_signup = st.tabs(["Login", "Create Account"])
    
    # --- LOGIN TAB ---
    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username (Unique ID)")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login 🚀")
            
            if submit_login and username and password:
                try:
                    # Database se user check karna
                    res = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
                    if res.data:
                        st.session_state.logged_in = True
                        st.session_state.user_name = username  # Database filtering ke liye Unique ID
                        st.session_state.display_name = res.data[0]['name']  # Greeting (dikhane) ke liye Asli Naam
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password.")
                except Exception as e:
                    st.error(f"Error: {e}")
                    
    # --- SIGN UP TAB ---
    with tab_signup:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name (e.g. Priyanka Sharma)")
            new_username = st.text_input("Choose a Username (e.g. priyanka_01)")
            new_password = st.text_input("Choose a Password", type="password")
            submit_signup = st.form_submit_button("Sign Up 📝")
            
            if submit_signup and new_name and new_username and new_password:
                try:
                    # Check karo ki username pehle se toh nahi hai
                    check_res = supabase.table("users").select("username").eq("username", new_username).execute()
                    if check_res.data:
                        st.warning("⚠️ This Username is already taken. Try adding numbers (e.g. priyanka_02).")
                    else:
                        # Naya user save karna
                        supabase.table("users").insert({
                            "username": new_username,
                            "name": new_name,
                            "password": new_password
                        }).execute()
                        st.success("✅ Account created successfully! Please go to the 'Login' tab to enter the app.")
                except Exception as e:
                    st.error(f"Error creating account: {e}")

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.display_name = ""

    if not st.session_state.logged_in:
        auth_page()
        return 

    # --- MAIN APP ---
    st.sidebar.title("🎯 Sankalp")
    st.sidebar.write(f"👤 **{st.session_state.display_name}**") 
    
    if st.sidebar.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.session_state.user_name = ""
        st.session_state.display_name = ""
        st.rerun()
        
    st.sidebar.markdown("---")
    
    menu = ["🏠 Dashboard", "📚 Task Engine", "⏱️ Focus Mode", "📊 Analytics"]
    choice = st.sidebar.radio("Go to", menu)
    
    st.sidebar.markdown("---")
    
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
