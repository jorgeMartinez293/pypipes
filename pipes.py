#!/usr/bin/env python3

from random import randint
import shutil
import sys
import time
import argparse

COLORS = {
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'YELLOW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'WHITE': '\033[37m',
    'RESET': '\033[0m'
}

COLOR_CODES = list(COLORS.values())[:-1]

class Instance:
    class Pipe:
        def __init__(self, game, color, thin, turn_chance):
            self.game=game
            self.board_shape=(self.game.columns, self.game.rows)
            self.color_code = COLOR_CODES[randint(0, len(COLOR_CODES) - 1)] if not color else COLORS[color]
            self.x_pos, self.y_pos=self._spawn()
            self.thin=thin
            self.turn_chance=turn_chance

            initial_char = ''
            if self.pointing == 0 or self.pointing == 1:
                initial_char = '│' if self.thin else '┃'
            else:
                initial_char = '─' if self.thin else '━'
            self.game.board[self.y_pos][self.x_pos] = self.color_code + initial_char + COLORS['RESET']

        def _turn(self):
            if self.pointing == 2 or self.pointing == 3:
                self.pointing=randint(0,1)
            else:
                self.pointing=randint(2,3)

            return self.pointing

        def _spawn(self):
            s = randint(0,3)
            if s == 0:
                x = 0
                y = randint(0, self.game.rows - 1)
                self.pointing = 2
            elif s == 1:
                x = self.game.columns - 1
                y = randint(0, self.game.rows - 1)
                self.pointing = 3
            elif s == 2:
                x = randint(0, self.game.columns - 1)
                y = 0
                self.pointing = 0
            elif s == 3:
                x = randint(0, self.game.columns - 1)
                y = self.game.rows - 1
                self.pointing = 1
            return x, y           

        def _harakiri(self):
            self.game._delete_pipe(self)

        def am_i_out(self):
            if self.x_pos >= 0 and self.x_pos < self.game.columns and self.y_pos >= 0 and self.y_pos < self.game.rows:
                return True
            else:
                self.game._create_pipe()
                self._harakiri()
                return False

        def _move(self):
            cha=None
            if self.pointing == 0:
                self.y_pos += 1
                cha='│' if self.thin else '┃'
            elif self.pointing == 1:
                self.y_pos -= 1
                cha='│' if self.thin else '┃'
            elif self.pointing == 2:
                self.x_pos += 1
                cha='─' if self.thin else '━'
            elif self.pointing == 3:
                self.x_pos -= 1                    
                cha='─' if self.thin else '━'

            if not self.am_i_out():
                return

            self.game.board[self.y_pos][self.x_pos] = self.color_code + cha + COLORS['RESET']

            if randint(0, self.turn_chance) == 0:
                old_pointing = self.pointing
                self._turn()
 
                if old_pointing == 1:                     
                    if self.pointing == 2:
                        cha = '┌' if self.thin else '┏'
                    elif self.pointing == 3:
                        cha = '┐' if self.thin else '┓'
                elif old_pointing == 0:
                    if self.pointing == 2:
                        cha = '└' if self.thin else '┗'
                    elif self.pointing == 3:
                        cha = '┘' if self.thin else '┛'

                elif old_pointing == 3:
                    if self.pointing == 0:
                        cha = '┌' if self.thin else '┏'
                    elif self.pointing == 1:
                        cha = '└' if self.thin else '┗'
                elif old_pointing == 2:
                    if self.pointing == 0:
                        cha = '┐' if self.thin else '┓'
                    elif self.pointing == 1:
                        cha = '┘' if self.thin else '┛'
       
                self.game.board[self.y_pos][self.x_pos] = self.color_code + cha + COLORS['RESET']
        
            


    def __init__(self, n_pipes, max_iter, speed, color, thin, turn_chance):
        self.columns, self.rows=shutil.get_terminal_size() 
        self.active_pipes=[]
        self.board=self._create_table()
        self.max_iter=max_iter
        self.speed=speed
        self.color=color if color in COLORS else None
        self.thin=thin
        self.turn_chance=turn_chance
        for _ in range(n_pipes):
            self._create_pipe()

    def _create_table(self):
        board = [[' '] * self.columns for _ in range(self.rows)]
        return board

    def _create_pipe(self):
        pipe=self.Pipe(game=self, color=self.color, thin=self.thin, turn_chance=self.turn_chance)
        self.active_pipes.append(pipe)

    def _delete_pipe(self, pipe):
        self.active_pipes.remove(pipe)

    def _update(self):
        for pipe in self.active_pipes:
            pipe._move()

    def _draw_frame(self):
        sys.stdout.write("\033[H")
        sys.stdout.write(str(self))
        sys.stdout.flush()

    def play(self):
        i = 0
        while True:
            self._draw_frame()
            self._update()
            time.sleep(self.speed)
            i+=1
            if i==self.max_iter:
                i=0
                self._snap()

    def _snap(self):
        for pipe in self.active_pipes:
            self._delete_pipe(pipe)
            self._create_pipe()
        self.board=self._create_table()

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.board)          


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A python recreation of pipes.sh'
    )

    parser.add_argument(
        '-n',
        '--pipes',
        type=int,
        default=1,
        help='Number of simultaneous pipes (by default 1)'
    )

    parser.add_argument(
        '-r',
        '--reset',
        type=int,
        default=2000,
        help='Iterations before restoring the window (by default 2000)'
    )

    parser.add_argument(
        '-s',
        '--speed',
        type=float,
        default=0.02,
        help='Seconds between each pipe movement (by default 0.02)'
    )

    parser.add_argument(
        '-c',
        '--color',
        type=str,
        default=None,
        help='Sets the color of the pipes, if not specified, multicolor'
    )

    parser.add_argument(
        '-t',
        '--thin',
        type=bool,
        default=False,
        help='Defines if the pipes should be thin (default False)'
    )

    parser.add_argument(
        '-p',
        '--prob',
        type=int,
        default=10,
        help='Defines how often (1/x) the pipes turn (by default 10)'
    )

    args = parser.parse_args()

    instance = Instance(
        n_pipes=args.pipes, 
        max_iter=args.reset, 
        speed=args.speed,
        color=args.color,
        thin=args.thin,
        turn_chance=args.prob
    )

    try:
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        instance.play()

    except KeyboardInterrupt:
        pass

    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        print()
