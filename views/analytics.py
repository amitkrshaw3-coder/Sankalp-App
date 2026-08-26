import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.db_supabase import supabase

def render_analysis():
    st.header("📊 Progress Analysis")
    st.markdown("Track your performance and find areas to improve.")
    
    # NAYA: User name nikalna
    user_name = st.session_state.get("user_name", "Student")

    tab_time, tab_accuracy = st.tabs(["⏱️ Study Trends", "🎯 Subject Performance"])

    with tab_time:
        st.subheader("Study Time (Last 7 Days)")
        try:
            past_7_days = str(date.today() - timedelta(days=7))
            # NAYA: .eq("user_name", user_name) filter lagaya
            response = supabase.table("study_sessions").select("session_date, duration_minutes").eq("user_name", user_name).gte("session_date", past_7_days).execute()
            sessions = response.data
            
            if sessions:
                df = pd.DataFrame(sessions)
                daily_time = df.groupby('session_date')['duration_minutes'].sum().reset_index()
                daily_time.set_index('session_date', inplace=True)
                st.bar_chart(daily_time)
            else:
                st.info("No study sessions recorded in the last 7 days yet.")
        except Exception as e:
            st.error(f"Could not load study trends: {e}")

    with tab_accuracy:
        st.subheader("Strongest & Weakest Subjects")
        try:
            # NAYA: .eq("user_name", user_name) filter lagaya
            test_response = supabase.table("test_results").select("subject, accuracy").eq("user_name", user_name).execute()
            tests = test_response.data
            
            if tests:
                df_tests = pd.DataFrame(tests)
                subject_acc = df_tests.groupby('subject')['accuracy'].mean().reset_index()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Top Performing Subjects 🏆**")
                    top_subjects = subject_acc.sort_values(by='accuracy', ascending=False).head(3)
                    st.dataframe(top_subjects, hide_index=True, use_container_width=True)
                with col2:
                    st.write("**Needs Attention ⚠️**")
                    weak_subjects = subject_acc.sort_values(by='accuracy', ascending=True).head(3)
                    st.dataframe(weak_subjects, hide_index=True, use_container_width=True)
                
                st.markdown("---")
                st.write("**Overall Subject Accuracy**")
                subject_acc.set_index('subject', inplace=True)
                st.line_chart(subject_acc)
            else:
                st.info("No test results added yet.")
        except Exception as e:
            pass
