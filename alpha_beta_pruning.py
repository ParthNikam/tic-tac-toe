import time


# tic-tac-toe
class Game:
    def __init__(self):
        self.initialize_game()
    
    def initialize_game(self):
        self.current_state=[['.','.','.'],
                            ['.','.','.'],
                            ['.','.','.']]

        # player X always has first turn
        self.player_turn = 'X'

    def draw_board(self):
        for i in range(0,3):
            for j in range(0,3):
                print('{}|'.format(self.current_state[i][j]), end=" ")
            print()
        print()

    # check if a move is valid
    def is_valid(self, px, py):
        if (px < 0 or px > 2 or py < 0 or py > 2):
            return False
        elif (self.current_state[px][py] != '.'): 
            return False
        else:
            return True

    # check if the game has ended and return the winner
    def is_end(self):
        
        # vertical win
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and \
                self.current_state[0][i] == self.current_state[1][i] and \
                self.current_state[1][i] == self.current_state[2][i]):
                return self.current_state[0][i]

        # horizontal win
        for i in range(0, 3):
            if (self.current_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.current_state[i] == ['O', 'O', 'O']):
                return 'O'

        # diagonal 1
        if (self.current_state[0][0] != '.' and \
            self.current_state[0][0] == self.current_state[1][1] and \
            self.current_state[0][0] == self.current_state[2][2]):
            return self.current_state[0][0]

        # diagonal 2
        if (self.current_state[0][2] != '.' and \
            self.current_state[0][2] == self.current_state[1][1] and \
            self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]

        # check if is board filled
        for i in range(0, 3):
            for j in range(0, 3):
                # if there's an empty cell, continue the game
                if (self.current_state[i][j] == '.'):
                    return None

        # game tied
        return '.'


    # the AI wants to maximize its own score and minimize ours
    # AI is 'O' human is 'X'

    def max_alpha_beta(self, alpha, beta):
        maxv = -2
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    if maxv >= beta:
                        return (maxv, px, py)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)                

    def min_alpha_beta(self, alpha, beta):

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)


    def play(self):
        while True:
            self.draw_board()
            self.result = self.is_end()

            # Printing the appropriate message if the game has ended
            if self.result != None:
                if self.result == 'X':
                    print('The winner is X!')
                elif self.result == 'O':
                    print('The winner is O!')
                elif self.result == '.':
                    print("game tied!")

                self.initialize_game()
                return

            if self.player_turn == 'X':
                while True:
                    start = time.time()
                    (m, qx, qy) = self.min_alpha_beta(-2,2) # lower bound and upper bound 
                    end = time.time()
                    print('Evaluation time: {}s'.format(round(end - start, 7)))
                    # print('Recommended move: X = {}, Y = {}'.format(qx, qy))

                    inputs = input("enter space separated i j coordinates: ").split()
                    px, py = int(inputs[0]), int(inputs[1])

                    qx, qy = px, py

                    if self.is_valid(px, py):
                        self.current_state[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else:
                        print('Invalid move! Try again.')

            else:
                (m, px, py) = self.max_alpha_beta(-2,2)
                self.current_state[px][py] = 'O'
                self.player_turn = 'X'        
            


def main(): 
    g = Game()
    g.play()


if __name__ == "__main__":
    main()