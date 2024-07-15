from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE_PATH = '\Desktop\games.sqbpro'

def connect_db():
    return sqlite3.connect(DATABASE_PATH)

@app.route('/games', methods=['GET'])
def get_all_games():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game_data")
    games = cursor.fetchall()
    conn.close()
    return jsonify(games)

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game_data WHERE index=?", (game_id,))
    game = cursor.fetchone()
    conn.close()
    if game:
        return jsonify(game)
    else:
        return jsonify({'error': 'Game not found'}), 404

@app.route('/games', methods=['POST'])
def add_game():
    new_game = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO game_data (Name, Platform, Year_of_Release, NA_sales)
        VALUES (?, ?, ?, ?)
    """, (new_game['Name'], new_game['Platform'], new_game['Year_of_Release'], new_game['NA_sales']))
    conn.commit()
    conn.close()
    return jsonify(new_game), 201

@app.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    updated_game = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE game_data
        SET Name=?, Platform=?, Year_of_Release=?, NA_sales=?
        WHERE index=?
    """, (updated_game['Name'], updated_game['Platform'], updated_game['Year_of_Release'], updated_game['NA_sales'], game_id))
    conn.commit()
    conn.close()
    return jsonify(updated_game)

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM game_data WHERE index=?", (game_id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
