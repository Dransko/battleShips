
class GameBoard(object):

    def __init__(self, battleships, board_width, board_height):
        self.battleships = battleships
        self.shots = []
        self.board_width = board_width
        self.board_height = board_height
    
    # update battleship with any hits
    # save the fact that the shot was a 
    # hit or miss
    def take_shot(self, shot_location):
        is_hit = False
        for b in self.battleships:
            idx = b.body_index(shot_location)
            if idx is not None:
                # it was a hit
                is_hit = True
                b.hits[idx] = True
                break
        
        self.shots.append(Shot(shot_location, is_hit))

    def is_game_over(self):
        return all([b.is_destroyed() for b in self.battleships])
        



class Shot(object):

    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit


class Battleship(object):

    @staticmethod
    def build(head, length, direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i)
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "W":
                el = (head[0] - i, head[1])
            elif direction == "E":
                el = (head[0] + i, head[1])
            
            body.append(el)
        return Battleship(body)

    def __init__(self, body):
        self.body = body
        self.hits = [False] * len(body)

    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None
    
    def is_destroyed(self):
        return all(self.hits)
        

def render(game_board, show_battleships=False):
    header = "+"+ "-"*game_board.board_width + "+"
    print(header)


    #Construct empty board
    board = []
    for _ in range(game_board.board_width):
        board.append([None for _ in range(game_board.board_height)])

    if show_battleships:
        #Add the battleships to the board
        for b in game_board.battleships:
            for x, y in b.body:
                board[x][y] = "O"

    #Add the shots to the board
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            ch = "X"
        else:
            ch = "."
        board[x][y] = ch



    for y in range(game_board.board_height):
        row = []
        for x in range(game_board.board_width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")
    print(header)



if __name__ == "__main__":

    battleships = [
        Battleship.build((1,1), 2, "N"),
        Battleship.build((5,8), 5, "N"),
        Battleship.build((2,3), 4, "E")
    ]


    game_board = GameBoard(battleships, 10, 10)

    while True:
        inp = input("Where do you want to shoot?\n")
        xstr, ystr = inp.split(",")
        x = int(xstr)
        y = int(ystr)

        game_board.take_shot((x,y))
        render(game_board)

        if game_board.is_game_over():
            print("YOU WIN")
            break

      