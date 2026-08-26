import streamlit as st
import time
from datetime import date
from utils.db_supabase import supabase

def render_timer():
    st.header("⏱️ Focus Mode")
    st.markdown("Minimize distractions. It's time for Deep Work.")

    # NAYA: Session state se user ka naam lena
    user_name = st.session_state.get("user_name", "Student")
    today_str = str(date.today())
    
    try:
        # NAYA: .eq("user_name", user_name) add kiya
        response = supabase.table("daily_tasks").select("*").eq("user_name", user_name).eq("target_date", today_str).eq("status", False).execute()
        tasks = response.data
    except Exception as e:
        tasks = []
        st.error("Database connection error.")

    if not tasks:
        st.info("No pending tasks for today! Awesome job. 🎉")
        return

    task_options = {f"{t['subject']} - {t['topic']}": t['task_id'] for t in tasks}
    selected_task_name = st.selectbox("What are you focusing on right now?", list(task_options.keys()))
    
    st.markdown("---")
    session_type = st.radio("Select Session Type", ["Pomodoro (25 Min)", "Deep Work (50 Min)", "Custom (Test Mode)"], horizontal=True)
    
    minutes = 25
    if session_type == "Deep Work (50 Min)":
        minutes = 50
    elif session_type == "Custom (Test Mode)":
        minutes = st.number_input("Enter minutes", min_value=1, max_value=120, value=1)

    start_button = st.button("🚀 Start Focus Session")

    if "session_completed" not in st.session_state:
        st.session_state.session_completed = False
        st.session_state.completed_task_id = None
        st.session_state.completed_task_name = None

    if start_button:
        task_id = task_options[selected_task_name]
        st.write(f"### Focusing on: **{selected_task_name}**")
        
        timer_placeholder = st.empty()
        progress_bar = st.progress(0)
        total_seconds = int(minutes * 60)
        
        for i in range(total_seconds, -1, -1):
            mins, secs = divmod(i, 60)
            timer_placeholder.markdown(
                f"<h1 style='text-align: center; font-size: 80px; color: #ff4b4b;'>{mins:02d}:{secs:02d}</h1>", 
                unsafe_allow_html=True
            )
            progress_bar.progress(1 - (i / total_seconds))
            time.sleep(1)
        
        try:
            # NAYA: "user_name" ke sath data save karna
            supabase.table("study_sessions").insert({
                "user_name": user_name,
                "task_id": task_id,
                "duration_minutes": minutes,
                "session_date": str(date.today())
            }).execute()
            
            st.balloons()
            st.success(f"✅ {minutes} minutes added to today's study time!")
            st.session_state.session_completed = True
            st.session_state.completed_task_id = task_id
            st.session_state.completed_task_name = selected_task_name
            st.rerun()
            
        except Exception as e:
            st.error(f"Error saving session: {e}")

    if st.session_state.session_completed:
        st.markdown("---")
        st.subheader("🎯 Session Complete!")
        st.write(f"Did you complete the target for: **{st.session_state.completed_task_name}**?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Yes, Completed"):
                supabase.table("daily_tasks").update({"status": True}).eq("task_id", st.session_state.completed_task_id).execute()
                st.success("Awesome! Task marked as done.")
                st.session_state.session_completed = False
                time.sleep(1.5)
                st.rerun()
        with col2:
            if st.button("🟡 Partially Done"):
                st.info("Good effort! Keep it up in the next session.")
                st.session_state.session_completed = False
                time.sleep(1.5)
                st.rerun()
        with col3:
            if st.button("❌ No, Got Distracted"):
                st.warning("No worries. Take a break and try again later.")
                st.session_state.session_completed = False
                time.sleep(1.5)
                st.rerun()
