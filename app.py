import streamlit as st
from datetime import date, timedelta

# Page Config (sabse upar hona chahiye)
st.set_page_config(page_title="Sankalp - Student OS", page_icon="🎯", layout="wide")

from views import dashboard, task_engine, focus_mode, analytics
from utils.db_supabase import supabase

def get_streak():
    try:
        # Database se saari study session dates nikalna
        response = supabase.table("study_sessions").select("session_date").execute()
        if not response.data:
            return 0
            
        # Saari unique dates ka ek set banana
        study_dates = {session['session_date'] for session in response.data}
        
        streak = 0
        check_date = date.today()
        
        # Check 1: Kya aaj padhai ki?
        if str(check_date) in study_dates:
            streak += 1
            check_date -= timedelta(days=1)
        # Check 2: Agar aaj nahi ki, par kya kal ki thi? (Toh streak tuti nahi hai)
        elif str(check_date - timedelta(days=1)) not in study_dates:
            return 0
        else:
            check_date -= timedelta(days=1)
            
        # Piche ki dates check karte jao
        while str(check_date) in study_dates:
            streak += 1
            check_date -= timedelta(days=1)
            
        return streak
    except Exception as e:
        return 0

def main():
    st.sidebar.title("🎯 Sankalp")
    st.sidebar.markdown("---")
    
    # Navigation
    menu = ["🏠 Dashboard", "📚 Task Engine", "⏱️ Focus Mode", "📊 Analytics"]
    choice = st.sidebar.radio("Go to", menu)
    
    st.sidebar.markdown("---")
    
    # --- DYNAMIC STREAK CALCULATION ---
    current_streak = get_streak()
    
    if current_streak == 0:
        st.sidebar.info("🧊 Study Streak: 0 Days. Start today!")
    elif current_streak < 3:
        st.sidebar.info(f"🔥 Study Streak: {current_streak} Days. Good start!")
    elif current_streak < 7:
        st.sidebar.success(f"🔥 Study Streak: {current_streak} Days. You're on fire!")
    else:
        st.sidebar.success(f"🏆 Study Streak: {current_streak} Days. Unstoppable!")

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
