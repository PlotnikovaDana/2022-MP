from collections import namedtuple

Dir = namedtuple("Dir", ["char", "dy", "dx"])

class Maze:
    START = "S"
    END   = "E"
    WALL  = "#"
    PATH  = " "
    OPEN  = {PATH, END}  # места на карте, куда можно переместиться (не стена или уже исследованные)

    RIGHT = Dir(">",  0,  1)
    DOWN  = Dir("v",  1,  0)
    LEFT  = Dir("<",  0, -1)
    UP    = Dir("^", -1,  0)
    DIRS  = [RIGHT, DOWN, LEFT, UP]

    @classmethod
    def load_maze(cls, fname):
        with open(fname) as inf:
            lines = (line.rstrip("\r\n") for line in inf)
            maze  = [list(line) for line in lines]
        return cls(maze)

    def __init__(self, maze):
        self.maze = maze

    def __str__(self):
        return "\n".join(''.join(line) for line in self.maze)

    def find_start(self):
        for y,line in enumerate(self.maze):
            try:
                x = line.index("S")
                return y, x
            except ValueError:
                pass

        # not found!
        raise ValueError("Начальное местоположение не найдено")

    def solve(self, y, x):
        if self.maze[y][x] == Maze.END:
            # базовый вариант - конечная точка найдена
            return True
        else:
            # рекурсивно искать в каждом направлении отсюда
            for dir in Maze.DIRS:
                ny, nx = y + dir.dy, x + dir.dx
                if self.maze[ny][nx] in Maze.OPEN:  # могу я пойти этим путем?
                    if self.maze[y][x] != Maze.START: # не перезаписывайте Maze.START
                        self.maze[y][x] = dir.char  # выбранное направление маркировки
                    if self.solve(ny, nx):          # пересмотреть...
                        return True                 # решение найдено!

            # решение не найдено из этого места
            if self.maze[y][x] != Maze.START:       # не перезаписывайте Maze.START
                self.maze[y][x] = Maze.PATH         # удалить неудачный поиск с карты
            return False

def main():
    maze = Maze.load_maze("maze-for-u.txt")

    print("Лабиринт загружен:")
    print(maze)

    try:
        sy, sx = maze.find_start()
        print("решение...")
        if maze.solve(sy, sx):
            print(maze)
        else:
            print("    решение не найдено")
    except ValueError:
        print("Начальная точка не найдена.")

if __name__=="__main__":
    main()