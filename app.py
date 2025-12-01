import streamlit as st
import pages.Login
import pages.CybersecurityDashboard
import pages.ITDashboard  # second domain

st.set_page_config(page_title="CW2 Intelligence Platform", layout="wide")


def main():
    # Persistent session state for auth
    if "logged_in_user" not in st.session_state:
        st.session_state["logged_in_user"] = None
        st.session_state["role"] = None

    # Top header bar
    st.title("Multi-Domain Intelligence Platform (CW2)")

    with st.sidebar:
        st.header("Navigation")

        # Show who is logged in (if anyone)
        if st.session_state["logged_in_user"]:
            st.success(
                f"Logged in as: {st.session_state['logged_in_user']} "
                f"({st.session_state['role']})"
            )
            if st.button("Logout"):
                # clear session and force rerun with new state
                st.session_state["logged_in_user"] = None
                st.session_state["role"] = None
                st.rerun()          # 🔥 replace experimental_rerun with rerun
        else:
            st.info("Not logged in")

        page = st.selectbox(
            "Go to",
            ["Login", "Cybersecurity Dashboard", "IT Dashboard"],
        )

    # Route to correct page
    if page == "Login":
        pages.Login.show()
    elif page == "Cybersecurity Dashboard":
        pages.CybersecurityDashboard.show()
    elif page == "IT Dashboard":
        pages.ITDashboard.show()


if __name__ == "__main__":
    main()