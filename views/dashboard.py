import streamlit as st
from datetime import date, datetime
from utils.db_supabase import supabase

def render_dashboard():
    # --- 1. Dynamic Greeting ---
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"
        
    # User ka naam nikalna
    user_name = st.session_state.get("user_name", "Student")
    
    st.title(f"{greeting}, {user_name} 👋")
    st.markdown("Here is your battle plan for today.")

    today_str = str(date.today())

    # --- 2. Study Time Calculation ---
    total_minutes = 0
    try:
        # STRICT FILTER: .eq("user_name", user_name)
        session_response = supabase.table("study_sessions").select("duration_minutes").eq("user_name", user_name).eq("session_date", today_str).execute()
        if session_response.data:
            total_minutes = sum(session['duration_minutes'] for session in session_response.data)
    except Exception as e:
        pass

    hours = total_minutes // 60
    mins = total_minutes % 60
    study_time_display = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"

    # --- 3. Task Progress Calculation ---
    total_tasks = 0
    completed_tasks = 0
    progress_percentage = 0
    tasks = []

    try:
        # STRICT FILTER: .eq("user_name", user_name)
        task_response = supabase.table("daily_tasks").select("*").eq("user_name", user_name).eq("target_date", today_str).execute()
        tasks = task_response.data
        if tasks:
            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if task['status'])
            if total_tasks > 0:
                progress_percentage = int((completed_tasks / total_tasks) * 100)
    except Exception as e:
        pass

    # --- 4. Avg Accuracy Calculation ---
    avg_accuracy = 0
    try:
        # STRICT FILTER: .eq("user_name", user_name)
        acc_response = supabase.table("test_results").select("accuracy").eq("user_name", user_name).execute()
        if acc_response.data:
            total_acc = sum(test['accuracy'] for test in acc_response.data)
            avg_accuracy = int(total_acc / len(acc_response.data))
    except Exception as e:
        pass

    # --- Top Level Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Today's Progress", value=f"{progress_percentage}%", delta=f"{total_tasks - completed_tasks} tasks remaining", delta_color="inverse")
    col2.metric(label="Study Time", value=study_time_display, delta="Tracked today!")
    col3.metric(label="Avg Accuracy", value=f"{avg_accuracy}%", delta="Overall tests") 

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
                    st.rerun()

    # --- Performance Bars ---
    with col_perf:
        st.subheader("📊 Performance")
        st.write("**Focus**")
        st.progress(80) 
        
        st.write(f"**Completion ({progress_percentage}%)**")
        st.progress(progress_percentage) 
        
        st.write(f"**Accuracy ({avg_accuracy}%)**")
        st.progress(avg_accuracy)
