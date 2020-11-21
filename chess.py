DEPTH = 10
class board:
    #初始化棋盘
    bd = [[' ' for x in range(3)] for y in range(3)]
    bd[0] = ['X', 'X', 'X']
    bd[2] = ['O', 'O', 'O']

    def __init__(self):
        self.show()

    def show(self):
        #打印棋盘
        for x in self.bd:
            print("+-+-+-+")
            for y in x:
                print("|", end='')
                print(y, end='')
            print('|')
        print("+-+-+-+")
        print()

    def move(self, *chesspiece_direction):
        #接受位置参数和方向参数，做出移动
        x, y, direction = chesspiece_direction
        a, b = 0, 0
        #process direction
        if direction == 'U':
            if x - 1 < 0:
                return 1
            a, b = x - 1, y
        elif direction == 'D':
            if x + 1 > 2:
                return 1
            a, b = x + 1, y
        elif direction == 'L':
            if y - 1 < 0:
                return 1
            a, b = x, y - 1
        elif direction == 'R':
            if y + 1 > 2:
                return 1
            a, b = x, y + 1

        #change board
        if self.bd[a][b] != ' ':
            return 1
        else:
            self.bd[a][b] = self.bd[x][y]
            self.bd[x][y] = ' '

        return a, b

    def demove(self, *chesspiece_direction):

        x, y, direction = chesspiece_direction
        if direction == 'U':
            direction = 'D'
        elif direction == 'D':
            direction = 'U'
        elif direction == 'L':
            direction = 'R'
        elif direction == 'R':
            direction = 'L'
        else:
            raise (ValueError)
        self.move(*(x, y, direction))

    def evaluate(self):
        #评估当前局势分数

        if self.judge() == 1:
            return 100
        elif self.judge() == 2:
            return -100
        else:
            score = 0
            for x in range(3):
                for y in range(3):
                    if self.bd[x][y] == 'X' and (x - y) % 2 == 0:
                        score += 1
                    if self.bd[x][y] == 'O' and (x - y) % 2 == 0:
                        score -= 1
            return score
        '''else:
            score = 0
            for x in range(3):
                if self.bd[x][x] == 'X':
                    score += 1
                elif self.bd[x][x] == 'O':
                    score -= 1
            if self.bd[0][2] == 'X':
                score += 1
            elif self.bd[0][2] == 'O':
                score -= 1
            if self.bd[2][0] == 'X':
                score += 1
            elif self.bd[2][0] == 'O':
                score -= 1
            return score'''

    def judge(self):
        #判断输赢
        if (self.bd[0][0] == self.bd[1][1] and self.bd[1][1]
                == self.bd[2][2]) or (self.bd[0][2] == self.bd[1][1]
                                      and self.bd[1][1] == self.bd[2][0]):
            if self.bd[1][1] == 'X':

                return 1
            elif self.bd[1][1] == 'O':

                return 2
        return 0


class playchess:

    board = board()
    list_position = []
    for x in range(3):
        for y in range(3):
            list_position.append((x, y))

    def getonestep(self):
        #获取玩家输入的位置与方向参数
        position = int(
            input("the location of your chess piece(从左上到右下标号依次为123456789):")[0])
        direction = input(
            "the direction(U D L R means up, down, left, right):").upper()
        x, y = self.list_position[position - 1]
        return x, y, direction

    def allbotchess(self):
        #获取所有电脑棋子位置
        botchess_list = []
        for x in range(len(self.board.bd)):
            for y in range(len(self.board.bd)):
                if self.board.bd[x][y] == 'X':
                    botchess_list.append((x, y))
        return botchess_list

    def allplayerchess(self):
        #获取所有玩家棋子位置
        botchess_list = []
        for x in range(len(self.board.bd)):
            for y in range(len(self.board.bd)):
                if self.board.bd[x][y] == 'O':
                    botchess_list.append((x, y))
        return botchess_list

    def allmove(self, *chess):
        #获取当前棋子可走方向
        move_list = []
        x, y = chess
        if 0 <= x - 1 <= 2 and self.board.bd[x - 1][y] == ' ':
            move_list.append('U')
        if 0 <= x + 1 <= 2 and self.board.bd[x + 1][y] == ' ':
            move_list.append('D')
        if 0 <= y - 1 <= 2 and self.board.bd[x][y - 1] == ' ':
            move_list.append('L')
        if 0 <= y + 1 <= 2 and self.board.bd[x][y + 1] == ' ':
            move_list.append('R')

        return move_list

    def max_research(self, depth, a, b):
        if depth == 0 or self.board.judge() != 0:
            return self.board.evaluate()
        v = -1000
        botchess_list = self.allbotchess()
        for chess in botchess_list:
            move_list = self.allmove(*chess)
            x, y = chess
            for move in move_list:
                #print(x, y, move)
                x1, y1 = self.board.move(*(x, y, move))
                v = max(v, self.min_research(depth - 1, a, b))
                if v >= b:
                    self.board.demove(*(x1, y1, move))
                    return v
                a = max(a, v)
                self.board.demove(*(x1, y1, move))
        return v

    def min_research(self, depth, a, b):
        if depth == 0 or self.board.judge() != 0:
            return self.board.evaluate()
        v = 1000
        playerchess_list = self.allplayerchess()
        for chess in playerchess_list:
            move_list = self.allmove(*chess)
            x, y = chess
            for move in move_list:
                #print(x, y, move)
                x1, y1 = self.board.move(*(x, y, move))
                v = min(v, self.max_research(depth - 1, a, b))
                if v <= a:
                    self.board.demove(*(x1, y1, move))
                    return v
                b = min(b, v)
                self.board.demove(*(x1, y1, move))
        return v

    def maxmin_research(self, depth):

        v = -1000
        best_move = ()
        a, b = -1000, 1000
        botchess_list = self.allbotchess()
        for chess in botchess_list:
            move_list = self.allmove(*chess)
            x, y = chess
            for move in move_list:
                #print(x, y, move)
                x1, y1 = self.board.move(*(x, y, move))
                score = self.min_research(depth - 1, a, b)
                if score > v:
                    best_move = x, y, move
                    v = score
                if v >= b:
                    self.board.demove(*(x1, y1, move))
                    return best_move
                a = max(a, v)
                self.board.demove(*(x1, y1, move))
        return best_move

    def aiturn(self):
        print('My turn,i move (> ▽ <)')
        best = self.maxmin_research(DEPTH)
        self.board.move(*best)
        self.board.show()
        if self.board.judge() == 1:
            print('(#^.^#)我 赢 力')
            return 0
        return 1

    def playerturn(self):
        print('Your turn,u move（○｀ 3′○）')
        move_list = []
        playerchess_list = self.allplayerchess()
        for chess in playerchess_list:
            move_list.append(self.allmove(*chess))
        sum = 0
        for i in range(3):
            sum += len(move_list[i])
        if sum == 0:
            print('你已经无路可走了 你输了 [○･｀Д´･ ○]')
            return 0
        while self.board.move(*self.getonestep()) == 1:
            print('U cant move like that! (｡•ˇ‸ˇ•｡)')

        if self.board.judge() == 2:
            print('你赢了（这个应该不太可能8')
            return 0
        self.board.show()
        return 1

    def play(self):
        #进行游戏
        first = input("你想先手吗？输入'Y'(是) 或'N'(否):")
        if first.upper() == 'Y':
            while (self.playerturn() and self.aiturn()):
                pass
        else:
            while (self.aiturn() and self.playerturn()):
                pass


if __name__ == '__main__':
    print("规则：上面三个棋子是电脑的，下面三个棋子是你的，只能像象棋一样前后左右走，对角线连满则判胜负(#^.^#)")
    play = playchess()
    play.play()
    print('press enter to end the game')
    input('')