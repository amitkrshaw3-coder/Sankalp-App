
import streamlit as st

def render_dashboard():
    st.title("Good Morning, Amit 👋")
    st.markdown("Here is your battle plan for today.")

    # Top Level Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Today's Progress", value="78%", delta="2 tasks remaining")
    col2.metric(label="Study Time", value="4h 20m", delta="-1h 40m to target", delta_color="inverse")
    col3.metric(label="Avg Accuracy", value="72%", delta="+5% from yesterday")

    st.markdown("---")
    
    # Task List & Performance Columns
    col_tasks, col_perf = st.columns([2, 1])

    with col_tasks:
        st.subheader("📝 Today's Tasks")
        # In future, fetch this from Supabase
        st.checkbox("Fluid Mechanics – Bernoulli Equation", value=True)
        st.checkbox("Thermodynamics – First Law", value=True)
        st.checkbox("50 RRB JE Questions")
        st.checkbox("Previous Year Paper – 1 hour")
        st.checkbox("Revision – 30 minutes")

    with col_perf:
        st.subheader("📊 Performance")
        st.write("**Focus**")
        st.progress(80)
        st.write("**Completion**")
        st.progress(90)
        st.write("**Accuracy**")
        st.progress(72)
