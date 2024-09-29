import streamlit as st
from database.db import add_student, get_active_poll, get_poll_options, add_vote, get_poll_results
import plotly.graph_objects as go
import time
import re

def student_page():
    st.header("Explore and Engage! 🎮")

    if 'student_id' not in st.session_state:
        show_registration_form()
    else:
        show_active_poll()

def show_registration_form():
    st.subheader("Register to Vote! 📝")
    with st.form("registration_form"):
        st.markdown('<p style="color: black;">Please fill out the form below:</p>', unsafe_allow_html=True)
        name = st.text_input("Name*")
        mobile_number = st.text_input("Mobile Number*")
        email = st.text_input("Email*")
        submitted = st.form_submit_button("Register")

        if submitted:
            if name and mobile_number and email:
                # Validate mobile number
                if not re.match(r'^[789]\d{9}$', mobile_number):
                    st.error("Invalid mobile number. Please enter a valid mobile number.")
                # Validate email
                elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    st.error("Invalid email address. Please enter a valid email address.")
                else:
                    try:
                        student_id = add_student(name, mobile_number, email)
                        st.session_state.student_id = student_id
                        st.success("Registration successful! You can now participate in the poll.")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
            else:
                st.error("Please provide name, mobile number, and email.")

def show_active_poll():
    active_poll = get_active_poll()
    if active_poll:
        st.subheader(f"Active Poll: {active_poll['question']}")
        options = get_poll_options(active_poll['id'])
        
        if 'voted' not in st.session_state:
            st.session_state.voted = False

        if not st.session_state.voted:
            if options and isinstance(options, list) and len(options) > 0:
                st.markdown("""
                    <style>
                    .stRadio label {
                        color: black !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                selected_option = st.radio("Choose your answer:", options, format_func=lambda x: x['option_text'])
                if st.button("Submit Vote"):
                    add_vote(active_poll['id'], st.session_state.student_id, selected_option['id'])
                    st.session_state.voted = True
                    st.success("Your vote has been recorded!")
                    st.balloons()
            else:
                st.warning("No options available for this poll.")
        
        # results placeholder
        results_placeholder = st.empty()
        
        # results update
        while True:
            results = get_poll_results(active_poll['id'])
            total_votes = sum(result['vote_count'] for result in results)
            
            # poll graph data
            option_texts = [result['option_text'] for result in results]
            vote_counts = [result['vote_count'] for result in results]
            percentages = [(count / total_votes) * 100 if total_votes > 0 else 0 for count in vote_counts]
            
            # poll graph
            fig = go.Figure(data=[
                go.Bar(
                    x=percentages,
                    y=option_texts,
                    orientation='h',
                    text=[f"{count} votes ({percentage:.1f}%)" for count, percentage in zip(vote_counts, percentages)],
                    textposition='auto',
                    marker_color='rgb(26, 118, 255)'
                )
            ])
            
            fig.update_layout(
                title="Live Voting Results",
                xaxis_title="Percentage of Votes",
                yaxis_title="Options",
                height=400,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            # results update
            with results_placeholder.container():
                st.subheader("Current Results")
                st.plotly_chart(fig, use_container_width=True)
                st.write(f"Total votes: {total_votes}")
            
            # results update delay
            time.sleep(5)
    else:
        st.info("There is no active poll at the moment. Please check back later.")

    if st.button("Refresh"):
        st.rerun()
