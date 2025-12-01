import streamlit as st


def show():
    st.title("Overview Dashboard")

    st.write(
        """
        This overview page summarises the CW2 Multi-Domain Intelligence Platform.

        - Use **CybersecurityDashboard** for security incident analytics.
        - Use **ITDashboard** for IT operations / service outages.
        - Use the **app** page for the combined navigation and login.
        """
    )


if __name__ == "__main__":
    show()