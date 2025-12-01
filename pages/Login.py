import streamlit as st
import sqlite3
import bcrypt
import bcrypt as br
from db_helper import connect_db
import bcrypt

def show():
    st.title("Login System")

    with st.form("login", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

    if login_btn:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()

        if row:
            stored_hash, role = row
            if bcrypt.checkpw(password.encode(), stored_hash.encode()):
                st.session_state["logged_in_user"] = username
                st.session_state["role"] = role
                st.success(f"Login successful. Welcome {username}! (Role: {role})")


                st.rerun()
            else:
                st.error("Incorrect password")
        else:
            st.error("User not found")