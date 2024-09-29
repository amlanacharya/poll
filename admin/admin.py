import streamlit as st
from database.db import get_db_connection, get_poll_results, get_all_students
import pandas as pd

def admin_page():
    st.header("Admin Dashboard")

    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter admin password", type="password")
        if st.button("Login"):
            if password == "grip@123":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
    else:
        show_admin_dashboard()

def show_admin_dashboard():
    st.subheader("Manage Polls")

    # new poll component
    with st.expander("Add New Poll"):
        new_question = st.text_input("Enter new poll question")
        new_options = st.text_area("Enter options (one per line)")
        if st.button("Add Poll"):
            options_list = [opt.strip() for opt in new_options.split('\n') if opt.strip()]
            if new_question and len(options_list) >= 2:
                add_new_poll(new_question, options_list)
                st.success("New poll added successfully!")
            else:
                st.error("Please provide a question and at least two options.")

    # poll management component
    st.subheader("Existing Polls")
    polls = get_all_polls()
    for poll in polls:
        with st.expander(f"Poll: {poll['question']}"):
            st.write(f"Status: {'Active' if poll['is_active'] else 'Inactive'}")
            if not poll['is_active']:
                if st.button(f"Activate Poll", key=f"activate_{poll['id']}"):
                    activate_poll(poll['id'])
                    st.rerun()
            else:
                if st.button(f"Deactivate Poll", key=f"deactivate_{poll['id']}"):
                    deactivate_poll(poll['id'])
                    st.rerun()
            
            if st.button(f"Delete Poll", key=f"delete_{poll['id']}"):
                delete_poll(poll['id'])
                st.rerun()
            
            # poll results component
            results = get_poll_results(poll['id'])
            if results:
                st.write("Current Results:")
                for result in results:
                    st.write(f"{result['option_text']}: {result['vote_count']} votes")

    # export student data component
    st.subheader("Export Student Data")
    if st.button("Export Student Data as CSV"):
        students = get_all_students()
        if students:
            df = pd.DataFrame(students, columns=['ID', 'Name', 'Mobile Number', 'Email'])
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="student_data.csv",
                mime="text/csv",
            )
        else:
            st.warning("No student data available to export.")

def add_new_poll(question, options):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO polls (question, is_active) VALUES (?, 0)', (question,))
    poll_id = cur.lastrowid
    for option in options:
        cur.execute('INSERT INTO options (poll_id, option_text) VALUES (?, ?)', (poll_id, option))
    conn.commit()
    conn.close()

def get_all_polls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM polls ORDER BY id DESC')
    polls = cur.fetchall()
    conn.close()
    return polls

def activate_poll(poll_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE polls SET is_active = 0')  # Deactivate all polls
    cur.execute('UPDATE polls SET is_active = 1 WHERE id = ?', (poll_id,))
    conn.commit()
    conn.close()

def deactivate_poll(poll_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE polls SET is_active = 0 WHERE id = ?', (poll_id,))
    conn.commit()
    conn.close()

def delete_poll(poll_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM votes WHERE poll_id = ?', (poll_id,))
    cur.execute('DELETE FROM options WHERE poll_id = ?', (poll_id,))
    cur.execute('DELETE FROM polls WHERE id = ?', (poll_id,))
    conn.commit()
    conn.close()
