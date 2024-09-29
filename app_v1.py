import streamlit as st
from admin.admin import admin_page
from student.student import student_page
from database.db import initialize_database

# Initialize the database
initialize_database()

def main():
    st.set_page_config(page_title="Grip the Facts", page_icon="?", layout="wide")
    
    # Add logo
    st.image("logo.png", width=400)  # Adjust width as needed
    
    st.title("Grip the Facts")

    # Simple navigation
    page = st.sidebar.selectbox("Choose a page", ["Student", "Admin"])

    if page == "Student":
        student_page()
    elif page == "Admin":
        admin_page()

if __name__ == "__main__":
    main()
