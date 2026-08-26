import streamlit as st
from datetime import date
from utils.db_supabase import supabase

def render_dashboard():
    st.title("Good Morning 👋")
    st.markdown("Here is your battle plan for today.")

    # Top Level Metrics (Abhi ke liye UI mockup rakhte hain)
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Today's Progress", value="78%", delta="2 tasks remaining")
    col2.metric(label="Study Time", value="4h 20m", delta="-1h 40m to target", delta_color="inverse")
    col3.metric(label="Avg Accuracy", value="72%", delta="+5% from yesterday")

    st.markdown("---")
    
    col_tasks, col_perf = st.columns([2, 1])

    with col_tasks:
        st.subheader("📝 Today's Tasks")
        
        try:
            # Aaj ki date ke tasks fetch karna
            today_str = str(date.today())
            response = supabase.table("daily_tasks").select("*").eq("target_date", today_str).execute()
            tasks = response.data
            
            if not tasks:
                st.info("No tasks for today. Go to 'Task Engine' to add your schedule!")
            else:
                for task in tasks:
                    # UI mein task dikhana aur uska status database se map karna
                    task_label = f"**{task['subject']}**: {task['topic']} ({task['task_type']})"
                    is_done = st.checkbox(task_label, value=task['status'], key=task['task_id'])
                    
                    # Agar tum checkbox tick/untick karte ho, toh Supabase update ho jayega
                    if is_done != task['status']:
                        supabase.table("daily_tasks").update({"status": is_done}).eq("task_id", task['task_id']).execute()
                        st.rerun() # Page refresh taaki progress update ho sake
                        
        except Exception as e:
            st.error(f"Database Error: Please check your db_supabase setup. Details: {e}")

    with col_perf:
        st.subheader("📊 Performance")
        st.write("**Focus**")
        st.progress(80)
        st.write("**Completion**")
        st.progress(90)
        st.write("**Accuracy**")
        st.progress(72)
