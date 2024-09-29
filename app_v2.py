import streamlit as st
from admin.admin import admin_page
from student.student import student_page
from database.db import initialize_database

# Initialize the database
initialize_database()

def main():
    st.set_page_config(page_title="Grip the Facts", page_icon="?", layout="wide")
    
    # Custom CSS to set white background and black text for all elements
    st.markdown("""
        <style>
        .stApp {
            background-color: white;
        }
        .stApp [data-testid="stHeader"],
        .stApp [data-testid="stToolbar"],
        .stApp [data-testid="stSidebar"] {
            background-color: white;
        }
        body, .stMarkdown, .stText, .stCode {
            color: black !important;
        }
        h1, h2, h3, h4, h5, h6, .stTitle {
            color: black !important;
            font-weight: bold;
        }
        .stAlert > div {
            color: black !important;
        }
        .stButton > button {
            color: white;
            background-color: #58A787;
            border: none;
        }
        .stButton > button:hover {
            background-color: #4c9077;
        }
        #logo-container {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
        }
        #logo-container img {
            max-width: 150px;
            height: auto;
        }
        .stPlotlyChart {
            background-color: white;
        }
        .stDataFrame {
            color: black;
        }
        /* New styles for form elements */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > input,
        .stMultiSelect > div > div > input {
            color: #58A787 !important;
            background-color: white !important;
        }
        .stTextInput > div > label,
        .stSelectbox > div > label,
        .stMultiSelect > div > label {
            color: white !important;
        }
        .stTextInput > div > div > input::placeholder {
            color: #888 !important;
        }
        /* Style for form container */
        [data-testid="stForm"] {
            background-color: #58A787;
            padding: 20px;
            border-radius: 10px;
        }
        /* Sidebar arrow button */
        button[kind="header"] {
            background-color: #58A787 !important;
        }
        button[kind="header"]:hover {
            background-color: #4c9077 !important;
        }
        button[kind="header"] > div {
            color: white !important;
        }
        /* Style for radio button labels */
        .stRadio label {
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Add logo
    st.image("logo.png", width=200)  # Adjust width as needed
    
    st.title("Grip the Facts")

    # Simple navigation 
    page = st.sidebar.selectbox("Choose a page", ["Student", "Admin"])

    if page == "Student":
        student_page()
    elif page == "Admin":
        admin_page()

if __name__ == "__main__":
    main()
