
import streamlit as st
from datetime import date
# Dhyan rahe ki tumhara db_supabase file mein client object ka naam 'supabase' ho
from utils.db_supabase import supabase 

def render_tasks():
    st.header("📚 Task Engine")
    st.markdown("Add your daily study goals and topics here.")

    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.text_input("Subject", placeholder="e.g., Fluid Mechanics or Indian Polity")
            # Tumhare exams ke hisaab se dropdown list
            exam = st.selectbox("Target Exam", ["RRB JE", "UPSC Civil Services", "SSC", "WBPRB", "Other"])
            
        with col2:
            topic = st.text_input("Topic", placeholder="e.g., Bernoulli Equation")
            task_type = st.selectbox("Task Type", ["Theory", "MCQ", "Revision", "Mock Test"])
        
        target_date = st.date_input("Target Date", min_value=date.today())
        
        submit = st.form_submit_button("Add Task 🚀")

        if submit:
            if subject and topic:
                try:
                    # Supabase mein data insert karna
                    # Note: Abhi hum user_id nahi bhej rahe kyunki auth setup nahi hai
                    data, count = supabase.table("daily_tasks").insert({
                        "subject": subject,
                        "topic": topic,
                        "task_type": task_type,
                        "target_date": str(target_date),
                        "status": False
                    }).execute()
                    
                    st.success("Task added successfully! Check your Dashboard.")
                except Exception as e:
                    st.error(f"Error adding task: {e}")
            else:
                st.warning("Please fill both Subject and Topic.")
