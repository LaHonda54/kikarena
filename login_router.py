import streamlit as st
from login_system import check_login

st.set_page_config(page_title="KikArena", page_icon="⚽")  # Browser-Tab und Icon

def login_page():
    st.title("KikArena – Login")  # Titel auf der Seite

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Login"):
        user = check_login(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.experimental_rerun()
        else:
            st.error("Login fehlgeschlagen.")

def app_router():
    if "logged_in" not in st.session_state:
        login_page()
    else:
        user = st.session_state["user"]
        st.sidebar.success(f"Eingeloggt als: {user['username']} ({user['role']})")

        if user["role"] == "admin":
            st.title("KikArena – Admin-Bereich")
            st.write("Verwalte Matches, Spieler, Coins.")
        elif user["role"] == "player":
            st.title("KikArena – Spielerbereich")
            st.write("Starte Matches oder verwalte dein Konto.")

if __name__ == "__main__":
    app_router()
