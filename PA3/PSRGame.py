# Benjamin Cape - 21F - CS76
# PA3
# 10.06.10

from psr_checkers import Board


class PSRGame:
    def __init__(self, player1, player2, player3):
        self.board = Board()
        self.players = [player1, player2, player3]

    def make_move(self):

        player = self.players[self.board.turn.value]
        move = player.choose_move(self.board)

        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\n"
        board_str = str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        # move_str = "White to move" if self.board.turn else "Black to move"

        return board_str
