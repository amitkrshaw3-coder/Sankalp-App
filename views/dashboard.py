import streamlit as st
from datetime import date
from utils.db_supabase import supabase

def render_dashboard():
    st.title("Good Morning, Amit 👋")
    st.markdown("Here is your battle plan for today.")

    today_str = str(date.today())

    # --- 1. Study Time Calculation ---
    total_minutes = 0
    try:
        session_response = supabase.table("study_sessions").select("duration_minutes").eq("session_date", today_str).execute()
        if session_response.data:
            total_minutes = sum(session['duration_minutes'] for session in session_response.data)
    except Exception as e:
        pass

    hours = total_minutes // 60
    mins = total_minutes % 60
    study_time_display = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

    # --- 2. Task Progress Calculation (NAYA CODE) ---
    total_tasks = 0
    completed_tasks = 0
    progress_percentage = 0
    tasks = []

    try:
        task_response = supabase.table("daily_tasks").select("*").eq("target_date", today_str).execute()
        tasks = task_response.data
        if tasks:
            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if task['status'])
            progress_percentage = int((completed_tasks / total_tasks) * 100)
    except Exception as e:
        st.error("Error fetching tasks.")

    # --- Top Level Metrics ---
    col1, col2, col3 = st.columns(3)
    # Yahan ab percentage aur remaining tasks dynamic ho gaye hain
    col1.metric(label="Today's Progress", value=f"{progress_percentage}%", delta=f"{total_tasks - completed_tasks} tasks remaining", delta_color="inverse")
    col2.metric(label="Study Time", value=study_time_display, delta="Tracked today!")
    col3.metric(label="Avg Accuracy", value="72%", delta="Coming soon")

    st.markdown("---")
    
    col_tasks, col_perf = st.columns([2, 1])

    # --- Task List ---
    with col_tasks:
        st.subheader("📝 Today's Tasks")
        if not tasks:
            st.info("No tasks for today. Go to 'Task Engine' to add your schedule!")
        else:
            for task in tasks:
                task_label = f"**{task['subject']}**: {task['topic']} ({task['task_type']})"
                is_done = st.checkbox(task_label, value=task['status'], key=task['task_id'])
                
                if is_done != task['status']:
                    supabase.table("daily_tasks").update({"status": is_done}).eq("task_id", task['task_id']).execute()
                    st.rerun() # Refresh to update percentage automatically

    # --- Performance Bars ---
    with col_perf:
        st.subheader("📊 Performance")
        st.write("**Focus**")
        st.progress(80) 
        
        st.write(f"**Completion ({progress_percentage}%)**")
        st.progress(progress_percentage) # Dynamic Progress Bar!
        
        st.write("**Accuracy**")
        st.progress(72) 
