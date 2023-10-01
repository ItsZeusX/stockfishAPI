from stockfish import Stockfish
import chess
import chess.svg
import os
from flask import Flask, request, jsonify

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '/executables/linux')
print(filename)

stockfish = Stockfish(path=filename)
stockfish.set_depth(20)
stockfish.set_skill_level(20)


app = Flask(__name__)



@app.route('/api/best_move', methods=['POST'])
def post_data():
    
    try:
        #* INIT NEW BOARD
        board = chess.Board()
        
        data = request.json
        moves = data["moves"]
        for m in moves :
          board.push_san(m)

        stockfish.set_fen_position(board.fen())
        
        #* CHECK TIME
        bestMoves = ""
        if "count" not in data : 
            bestMoves = stockfish.get_top_moves(1)
        else : 
            bestMoves = stockfish.get_top_moves(data["count"])
        for move in bestMoves :
            moveFrom = move["Move"][0:2]
            moveTo = move["Move"][2:4]

            board_svg = chess.svg.board(
                board,
                arrows=[chess.svg.Arrow(chess.parse_square(moveFrom), chess.parse_square(moveTo), color="#D18B47")],
            )
  
            move["board_svg"] = board_svg
            response = str({"fen" : board.fen(),"best_moves" : bestMoves})
            response = response.replace("ffce9e","E9EDCC")
            response = response.replace("d18b47","779954")

        return response, 200

    except Exception as e:
        return {"error": "An error occurred", "details": str(e)}, 500



if __name__ == '__main__':
    app.run()






