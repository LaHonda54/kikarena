import sqlite3
import streamlit as st

DB = "fifa_start.db"

st.set_page_config(page_title="KikArena – Auswertung", page_icon="⚽")
st.title("KikArena – Spielauswertung")

def get_open_matches():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT m.id, u1.username, u2.username, m.coins
        FROM matches m
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        WHERE m.result IS NULL
    """)
    matches = c.fetchall()
    conn.close()
    return matches

def set_match_result(match_id, winner_username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT player1_id, player2_id, coins FROM matches WHERE id = ?", (match_id,))
    match = c.fetchone()
    if not match:
        conn.close()
        return "Match nicht gefunden."

    player1_id, player2_id, einsatz = match
    c.execute("SELECT id FROM users WHERE username = ?", (winner_username,))
    winner = c.fetchone()
    if not winner:
        conn.close()
        return "Gewinner nicht gefunden."

    winner_id = winner[0]
    total = einsatz * 2
    c.execute("UPDATE users SET coins = coins + ? WHERE id = ?", (total, winner_id))
    c.execute("UPDATE matches SET result = 'done', winner_id = ? WHERE id = ?", (winner_id, match_id))
    conn.commit()
    conn.close()
    return f"{winner_username} hat gewonnen und {total} Coins erhalten."

matches = get_open_matches()
if matches:
    match_options = [f"#{m[0]}: {m[1]} vs {m[2]} (Einsatz: {m[3]})" for m in matches]
    selected = st.selectbox("Offene Spiele", match_options)
    match_id = int(selected.split(":")[0][1:])
    usernames = selected.split(":")[1].split("vs")
    player1 = usernames[0].strip()
    player2 = usernames[1].split("(")[0].strip()

    winner = st.selectbox("Gewinner auswählen", [player1, player2])

    if st.button("Ergebnis speichern"):
        info = set_match_result(match_id, winner)
        st.success(info)
else:
    st.info("Keine offenen Spiele gefunden.")
