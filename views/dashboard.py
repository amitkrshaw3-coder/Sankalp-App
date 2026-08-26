import streamlit as st
from datetime import date, datetime # datetime import add kiya
from utils.db_supabase import supabase

def render_dashboard():
    # --- NAYA CODE: Time-based Greeting ---
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
        
    # Session state se user ka naam nikalna
    user_name = st.session_state.get("user_name", "Student")
    
    st.title(f"{greeting}, {user_name} 👋")
    st.markdown("Here is your battle plan for today.")

    today_str = str(date.today())

    # --- Iske neeche tumhara pehle wala metrics aur progress ka code rahega ---
    # ... (total_minutes calculation etc.)

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
