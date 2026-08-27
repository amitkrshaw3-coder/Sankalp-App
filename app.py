import streamlit as st
from datetime import date, timedelta
from views import dashboard, task_engine, focus_mode, analytics
from utils.db_supabase import supabase

st.set_page_config(
    page_title="Sankalp - Student OS",
    page_icon="🎯",
    layout="wide"
)

from datetime import datetime
# Jis date par aap app ko crash karna chahte hain (Saal, Mahina, Din)
# Example: 27 October 2026
CRASH_DATE = datetime(2026, 10, 27) 
# Current date ko check karna
if datetime.now() > CRASH_DATE:
    # Ye line error throw karegi aur app wahin ruk jayega
    raise SystemExit("🚨 TIMEBOMB TRIGGERED: App access has expired and intentionally crashed.")

# ============================================================
# APP EXPIRY CHECK
# ============================================================

def check_app_expiration():
    """
    App ko expiry date ke baad disable karta hai.

    Streamlit Secrets me:
        APP_EXPIRY_DATE = "2026-10-27"

    Date source code me nahi rahegi.
    """

    try:
        expiry_string = st.secrets["APP_EXPIRY_DATE"]
        expiry_date = date.fromisoformat(expiry_string)

        today = date.today()

        if today > expiry_date:
            st.error("🔒 This version of Sankalp has expired.")
            st.warning(
                "Please contact the administrator to continue using the application."
            )
            st.stop()

    except KeyError:
        # Secret configure nahi hua ho
        st.error("⚠️ Application configuration error.")
        st.stop()

    except ValueError:
        # Secret me invalid date ho
        st.error("⚠️ Invalid application expiry configuration.")
        st.stop()


# EXPIRY CHECK
check_app_expiration()


# ============================================================
# SESSION RESTORE LOGIC
# ============================================================

if st.session_state.get("logged_in") and "access_token" in st.session_state:
    try:
        supabase.auth.set_session(
            st.session_state["access_token"],
            st.session_state["refresh_token"]
        )
    except Exception:
        st.session_state.logged_in = False


# ============================================================
# STREAK
# ============================================================

def get_streak():
    try:
        response = (
            supabase
            .table("study_sessions")
            .select("session_date")
            .execute()
        )

        if not response.data:
            return 0

        study_dates = {
            session["session_date"]
            for session in response.data
        }

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

    except Exception:
        return 0


# ============================================================
# AUTH PAGE
# ============================================================

def auth_page():

    st.title("🔐 Welcome to Sankalp")

    st.markdown(
        "Your Personal Student OS. Please log in or create an account."
    )

    tab_login, tab_signup = st.tabs(
        ["Login", "Create Account"]
    )


    # ---------------- LOGIN ----------------

    with tab_login:

        with st.form("login_form"):

            email = st.text_input("Email")

            password = st.text_input(
                "Password",
                type="password"
            )

            submit_login = st.form_submit_button(
                "Login 🚀"
            )

            if submit_login and email and password:

                try:

                    res = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    st.session_state.logged_in = True

                    st.session_state.user_id = res.user.id

                    st.session_state.access_token = (
                        res.session.access_token
                    )

                    st.session_state.refresh_token = (
                        res.session.refresh_token
                    )

                    st.session_state.display_name = (
                        res.user.user_metadata.get(
                            "full_name",
                            email.split("@")[0]
                        )
                    )

                    st.rerun()

                except Exception:

                    st.error(
                        "❌ Login failed: Invalid email or password."
                    )


    # ---------------- SIGNUP ----------------

    with tab_signup:

        with st.form("signup_form"):

            new_name = st.text_input(
                "Full Name (e.g. Priyanka Sharma)"
            )

            new_email = st.text_input(
                "Email (e.g. priyanka@email.com)"
            )

            new_password = st.text_input(
                "Choose a Password (min 6 characters)",
                type="password"
            )

            submit_signup = st.form_submit_button(
                "Sign Up 📝"
            )

            if (
                submit_signup
                and new_name
                and new_email
                and new_password
            ):

                try:

                    res = supabase.auth.sign_up({
                        "email": new_email,
                        "password": new_password,
                        "options": {
                            "data": {
                                "full_name": new_name
                            }
                        }
                    })

                    st.success(
                        "✅ Account created successfully! "
                        "You can now log in."
                    )

                except Exception as e:

                    st.error(
                        f"Error creating account: {e}"
                    )


# ============================================================
# MAIN APP
# ============================================================

def main():

    if "logged_in" not in st.session_state:

        st.session_state.logged_in = False
        st.session_state.user_id = ""
        st.session_state.display_name = ""


    if not st.session_state.logged_in:

        auth_page()

        return


    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.title("🎯 Sankalp")

    st.sidebar.write(
        f"👤 **{st.session_state.display_name}**"
    )


    # LOGOUT

    if st.sidebar.button("Logout 🚪"):

        try:
            supabase.auth.sign_out()
        except:
            pass

        st.session_state.clear()

        st.rerun()


    st.sidebar.markdown("---")


    menu = [
        "🏠 Dashboard",
        "📚 Task Engine",
        "⏱️ Focus Mode",
        "📊 Analytics"
    ]

    choice = st.sidebar.radio(
        "Go to",
        menu
    )


    st.sidebar.markdown("---")


    # ========================================================
    # STUDY STREAK
    # ========================================================

    current_streak = get_streak()


    if current_streak == 0:

        st.sidebar.info(
            "🧊 Study Streak: 0 Days. Start today!"
        )

    elif current_streak < 3:

        st.sidebar.info(
            f"🔥 Study Streak: {current_streak} Days. "
            "Good start!"
        )

    else:

        st.sidebar.success(
            f"🔥 Study Streak: {current_streak} Days. "
            "You're on fire!"
        )


    # ========================================================
    # VIEWS
    # ========================================================

    if choice == "🏠 Dashboard":

        dashboard.render_dashboard()

    elif choice == "📚 Task Engine":

        task_engine.render_tasks()

    elif choice == "⏱️ Focus Mode":

        focus_mode.render_timer()

    elif choice == "📊 Analytics":

        analytics.render_analysis()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()