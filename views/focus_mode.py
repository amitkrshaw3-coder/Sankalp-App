
import streamlit as st
import time
from datetime import date
from utils.db_supabase import supabase

def render_timer():
    st.header("⏱️ Focus Mode")
    st.markdown("Minimize distractions. It's time for Deep Work.")

    # Aaj ke pending tasks fetch karna
    today_str = str(date.today())
    try:
        response = supabase.table("daily_tasks").select("*").eq("target_date", today_str).eq("status", False).execute()
        tasks = response.data
    except Exception as e:
        tasks = []
        st.error("Database connection error.")

    if not tasks:
        st.info("No pending tasks for today! Awesome job. 🎉")
        return

    # Dropdown ke liye tasks ko format karna
    task_options = {f"{t['subject']} - {t['topic']}": t['task_id'] for t in tasks}
    selected_task_name = st.selectbox("What are you focusing on right now?", list(task_options.keys()))

    # Timer settings
    st.markdown("---")
    session_type = st.radio("Select Session Type", ["Pomodoro (25 Min)", "Deep Work (50 Min)", "Custom (Test Mode)"], horizontal=True)
    
    minutes = 25
    if session_type == "Deep Work (50 Min)":
        minutes = 50
    elif session_type == "Custom (Test Mode)":
        # Testing ke liye bas 1 minute ka timer
        minutes = st.number_input("Enter minutes", min_value=1, max_value=120, value=1)

    start_button = st.button("🚀 Start Focus Session")

    if start_button:
        st.write(f"### Focusing on: **{selected_task_name}**")
        
        # UI Timer Placeholder
        timer_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        total_seconds = int(minutes * 60)
        
        # Countdown logic
        for i in range(total_seconds, -1, -1):
            mins, secs = divmod(i, 60)
            # Timer ko bada aur sundar dikhane ke liye HTML
            timer_placeholder.markdown(
                f"<h1 style='text-align: center; font-size: 80px; color: #ff4b4b;'>{mins:02d}:{secs:02d}</h1>", 
                unsafe_allow_html=True
            )
            
            # Progress bar update
            progress_percent = 1 - (i / total_seconds)
            progress_bar.progress(progress_percent)
            
            time.sleep(1) # 1 second wait
        
        st.success("Session Complete! Great job. Take a short break.")
        st.balloons()
        
        # Next step (future): Yahan hum database mein session save karenge taaki dashboard par total study time update ho
