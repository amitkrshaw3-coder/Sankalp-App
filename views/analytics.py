import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.db_supabase import supabase

def render_analysis():
    st.header("📊 Progress Analysis")
    st.markdown("Track your performance and find areas to improve.")

    # Data fetch karne ke liye tabs
    tab_time, tab_accuracy = st.tabs(["⏱️ Study Trends", "🎯 Subject Performance"])

    # --- TAB 1: STUDY TIME TRENDS ---
    with tab_time:
        st.subheader("Study Time (Last 7 Days)")
        
        try:
            # Pichle 7 din ka data nikalna
            past_7_days = str(date.today() - timedelta(days=7))
            response = supabase.table("study_sessions").select("session_date, duration_minutes").gte("session_date", past_7_days).execute()
            sessions = response.data
            
            if sessions:
                # Data ko chart ke liye tayar karna
                df = pd.DataFrame(sessions)
                # Ek din mein agar multiple sessions hain toh unhe jod (sum) dena
                daily_time = df.groupby('session_date')['duration_minutes'].sum().reset_index()
                daily_time.set_index('session_date', inplace=True)
                
                # Streamlit ka inbuilt Bar Chart
                st.bar_chart(daily_time)
            else:
                st.info("No study sessions recorded in the last 7 days yet. Start a Focus Session!")
                
        except Exception as e:
            st.error(f"Could not load study trends: {e}")

    # --- TAB 2: SUBJECT PERFORMANCE ---
    with tab_accuracy:
        st.subheader("Strongest & Weakest Subjects")
        
        try:
            # Test results fetch karna
            test_response = supabase.table("test_results").select("subject, accuracy").execute()
            tests = test_response.data
            
            if tests:
                df_tests = pd.DataFrame(tests)
                # Subject-wise average accuracy nikalna
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
                st.info("No test results added yet. Add scores from the Task Engine to see your accuracy!")
                
        except Exception as e:
            st.error(f"Could not load performance data: {e}")

    # --- FUTURE AI COACH PLACEHOLDER ---
    st.markdown("---")
    st.subheader("🤖 AI Study Coach")
    st.info("AI Analysis: *You have been consistently hitting your daily targets, but accuracy in recent mock tests requires a targeted revision session tomorrow morning. I will adjust your schedule.* (Coming Soon)")
