from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE_PATH = 'C:/Users/Administrator/Desktop/games.sq3pro'  # Adjust the path as needed

def connect_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/games', methods=['GET'])
def get_all_games():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM game_data")
    games = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(games)

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM game_data WHERE "index" = ?', (game_id,))
    game = cursor.fetchone()
    conn.close()
    if game:
        return jsonify(dict(game))
    return jsonify({'error': 'Game not found'}), 404

@app.route('/games', methods=['POST'])
def add_game():
    new_game = request.json
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO game_data (Name, Platform, Year_of_Release, Genre, NA_sales, EU_sales, JP_sales, Other_sales, Critic_Score, User_Score, Rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_game['Name'], new_game['Platform'], new_game['Year_of_Release'], new_game['Genre'], 
        new_game['NA_sales'], new_game['EU_sales'], new_game['JP_sales'], 
        new_game['Other_sales'], new_game['Critic_Score'], new_game['User_Score'], 
        new_game['Rating']
    ))
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
        SET Name = ?, Platform = ?, Year_of_Release = ?, Genre = ?, NA_sales = ?, EU_sales = ?, JP_sales = ?, Other_sales = ?, Critic_Score = ?, User_Score = ?, Rating = ?
        WHERE "index" = ?
    """, (
        updated_game['Name'], updated_game['Platform'], updated_game['Year_of_Release'], 
        updated_game['Genre'], updated_game['NA_sales'], updated_game['EU_sales'], 
        updated_game['JP_sales'], updated_game['Other_sales'], updated_game['Critic_Score'], 
        updated_game['User_Score'], updated_game['Rating'], game_id
    ))
    conn.commit()
    conn.close()
    return jsonify(updated_game)

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM game_data WHERE "index" = ?', (game_id,))
    conn.commit()
    conn.close()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)