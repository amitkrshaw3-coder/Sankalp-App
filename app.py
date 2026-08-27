import streamlit as st
from datetime import date, timedelta
from views import dashboard, task_engine, focus_mode, analytics
from utils.db_supabase import supabase

st.set_page_config(page_title="Sankalp - Student OS", page_icon="🎯", layout="wide")

# --- SESSION RESTORE LOGIC ---
# Har baar Streamlit rerun hone par RLS ke liye session set karna zaroori hai
if st.session_state.get("logged_in") and "access_token" in st.session_state:
    try:
        supabase.auth.set_session(
            st.session_state["access_token"], 
            st.session_state["refresh_token"]
        )
    except Exception:
        # Agar token expire ho jaye toh logout kar do
        st.session_state.logged_in = False

def get_streak():
    try:
        # RLS enable hone ki wajah se, ye automatically sirf logged-in user ka data layega
        response = supabase.table("study_sessions").select("session_date").execute()
        
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

# --- UPDATED AUTH SYSTEM (Supabase Auth) ---
def auth_page():
    st.title("🔐 Welcome to Sankalp")
    st.markdown("Your Personal Student OS. Please log in or create an account.")
    
    tab_login, tab_signup = st.tabs(["Login", "Create Account"])
    
    # --- LOGIN TAB ---
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login 🚀")
            
            if submit_login and email and password:
                try:
                    # Supabase ki built-in auth api use karna
                    res = supabase.auth.sign_in_with_password({
                        "email": email, 
                        "password": password
                    })
                    
                    st.session_state.logged_in = True
                    st.session_state.user_id = res.user.id
                    st.session_state.access_token = res.session.access_token
                    st.session_state.refresh_token = res.session.refresh_token
                    # Display name metadata se nikalna (agar set kiya ho toh)
                    st.session_state.display_name = res.user.user_metadata.get("full_name", email.split("@")[0])
                    
                    st.rerun()
                except Exception as e:
                    st.error("❌ Login failed: Invalid email or password.")
                    
    # --- SIGN UP TAB ---
    with tab_signup:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name (e.g. Priyanka Sharma)")
            new_email = st.text_input("Email (e.g. priyanka@email.com)")
            new_password = st.text_input("Choose a Password (min 6 characters)", type="password")
            submit_signup = st.form_submit_button("Sign Up 📝")
            
            if submit_signup and new_name and new_email and new_password:
                try:
                    # Supabase Auth me naya user create karna aur metadata me naam save karna
                    res = supabase.auth.sign_up({
                        "email": new_email,
                        "password": new_password,
                        "options": {
                            "data": {
                                "full_name": new_name
                            }
                        }
                    })
                    st.success("✅ Account created successfully! You can now log in.")
                except Exception as e:
                    st.error(f"Error creating account: {e}")

def main():
    # Session state initialization
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.session_state.display_name = ""
        
    if not st.session_state.logged_in:
        auth_page()
        return 
        
    # --- MAIN APP ---
    st.sidebar.title("🎯 Sankalp")
    st.sidebar.write(f"👤 **{st.session_state.display_name}**") 
    
    if st.sidebar.button("Logout 🚪"):
        try:
            supabase.auth.sign_out()
        except:
            pass
        st.session_state.clear()
        st.rerun()
        
    st.sidebar.markdown("---")
    
    menu = ["🏠 Dashboard", "📚 Task Engine", "⏱️ Focus Mode", "📊 Analytics"]
    choice = st.sidebar.radio("Go to", menu)
    
    st.sidebar.markdown("---")
    
    current_streak = get_streak()
    
    if current_streak == 0:
        st.sidebar.info("🧊 Study Streak: 0 Days. Start today!")
    elif current_streak < 3:
        st.sidebar.info(f"🔥 Study Streak: {current_streak} Days. Good start!")
    else:
        st.sidebar.success(f"🔥 Study Streak: {current_streak} Days. You're on fire!")
        
    # Views render karna
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
