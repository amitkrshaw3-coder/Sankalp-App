import streamlit as st
from datetime import date
from utils.db_supabase import supabase

def render_dashboard():
    st.title("Good Morning, Amit 👋")
    st.markdown("Here is your battle plan for today.")

    today_str = str(date.today())

    # --- NAYA CODE: Database se aaj ka total study time nikalna ---
    total_minutes = 0
    try:
        session_response = supabase.table("study_sessions").select("duration_minutes").eq("session_date", today_str).execute()
        sessions = session_response.data
        if sessions:
            total_minutes = sum(session['duration_minutes'] for session in sessions)
    except Exception as e:
        st.error("Error fetching study time.")

    # Time ko hours aur minutes mein convert karna
    hours = total_minutes // 60
    mins = total_minutes % 60
    study_time_display = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

    # Top Level Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Today's Progress", value="78%", delta="Hardcoded (Next up!)")
    col2.metric(label="Study Time", value=study_time_display, delta="Dynamic! 🔥")
    col3.metric(label="Avg Accuracy", value="72%", delta="Hardcoded")

    st.markdown("---")
    
    col_tasks, col_perf = st.columns([2, 1])

    with col_tasks:
        st.subheader("📝 Today's Tasks")
        
        try:
            response = supabase.table("daily_tasks").select("*").eq("target_date", today_str).execute()
            tasks = response.data
            
            if not tasks:
                st.info("No tasks for today. Go to 'Task Engine' to add your schedule!")
            else:
                for task in tasks:
                    task_label = f"**{task['subject']}**: {task['topic']} ({task['task_type']})"
                    is_done = st.checkbox(task_label, value=task['status'], key=task['task_id'])
                    
                    if is_done != task['status']:
                        supabase.table("daily_tasks").update({"status": is_done}).eq("task_id", task['task_id']).execute()
                        st.rerun()
                        
        except Exception as e:
            st.error(f"Database Error: {e}")

    with col_perf:
        st.subheader("📊 Performance")
        st.write("**Focus**")
        st.progress(80)
        st.write("**Completion**")
        st.progress(90)
        st.write("**Accuracy**")
        st.progress(72)
