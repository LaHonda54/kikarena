import sqlite3
import streamlit as st

DB = "fifa_start.db"

st.set_page_config(page_title="KikArena – Match Start", page_icon="⚽")
st.title("KikArena – Match starten")

def get_players():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE role = 'player'")
    players = [row[0] for row in c.fetchall()]
    conn.close()
    return players

def get_user_id(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_user_coins(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT coins FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def start_match(player1, player2, einsatz):
    if player1 == player2:
        return "Ein Spieler kann nicht gegen sich selbst spielen."
    p1_id = get_user_id(player1)
    p2_id = get_user_id(player2)
    p1_coins = get_user_coins(player1)
    p2_coins = get_user_coins(player2)

    if p1_coins < einsatz or p2_coins < einsatz:
        return "Nicht genügend Coins bei einem der Spieler."

    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO matches (player1_id, player2_id, coins) VALUES (?, ?, ?)", (p1_id, p2_id, einsatz))
    match_id = c.lastrowid
    c.execute("UPDATE users SET coins = coins - ? WHERE id IN (?, ?)", (einsatz, p1_id, p2_id))
    conn.commit()
    conn.close()
    return f"Match #{match_id} gestartet: {player1} vs {player2}!"

spieler = get_players()
if len(spieler) >= 2:
    p1 = st.selectbox("Spieler 1", spieler)
    p2 = st.selectbox("Spieler 2", [s for s in spieler if s != p1])
    einsatz = st.slider("Wetteinsatz (Coins)", 1, 100, 10)

    if st.button("Spiel starten"):
        result = start_match(p1, p2, einsatz)
        st.info(result)
else:
    st.warning("Mindestens 2 Spieler müssen existieren.")
