from tkinter import *
from tkinter import messagebox
from random import randrange, choice
from copy import deepcopy
import time

w, h = 10,20
tile = 45
game_res = w * tile, h * tile
res = 750, 940
fps = 60

def on_closing():
    global app_running
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        app_running = False

tk = Tk()
app_running = True
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Tetris")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
#tk.iconbitmap("bomb-3175208_640.ico")

canvas = Canvas(tk, width=res[0], height=res[1], bg="red", highlightthickness=0)
canvas.pack()

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
        return "0"

def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))

sc_game = Canvas(tk, width=w * tile + 1, height=h * tile + 1, bg="purple", highlightthickness=0)
sc_game.place(x=20, y=20, anchor=NW)

img_obj1 = PhotoImage(file="img/vasya.png")
canvas.create_image(0, 0, anchor=NW, image=img_obj1)

img_obj2 = PhotoImage(file="img/krol.png")
sc_game.create_image(0, 0, anchor=NW, image=img_obj2)


grid = [sc_game.create_rectangle(x * tile, y * tile, x * tile + tile, y * tile + tile) for x in range(w) for y in range(h)]

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[[x + w // 2, y + 1, 1, 1] for x, y in fig_pos] for fig_pos in figures_pos]
field = [[0 for i in range(w)] for j in range(h)]

anim_count, anim_speed, anim_list = 0, 60, 2000

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
record = "0"

canvas.create_text(505, 30, text="TETRIS", font=("Arial", 45),fill="red", anchor=NW)
canvas.create_text(535, 780, text="score:", font=("Arial", 45),fill="blue", anchor=NW)
_score = canvas.create_text(550, 840, text=str(score), font=("Arial", 45),fill="black", anchor=NW)
canvas.create_text(525, 650, text="record:", font=("Arial", 45),fill="gold", anchor=NW)
_record = canvas.create_text(550, 710, text=record, font=("Arial", 45),fill="gold", anchor=NW)

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def check_borders():
    if figure[i][0] < 0 or figure[i][0] > w - 1:
        return False
    elif figure[i][1] > h - 1 or field[figure[i][1]][figure[i][0]]:
        return False
    return True

def move_obj(event):
    global rotate, anim_limit, dx
    if event.keysym == 'Up':
        rotate = True
    elif event.keysym == 'Down':
        anim_limit = 100
    elif event.keysym == 'Left':
        dx = -1
    elif event.keysym == 'Right':
        dx = 1

sc_game.bind_all("<KeyPress-Up>",move_obj)
sc_game.bind_all("<KeyPress-Down>",move_obj)
sc_game.bind_all("<KeyPress-Left>",move_obj)
sc_game.bind_all("<KeyPress-Right>",move_obj)

dx, rotate = 0, False
while app_running:
    if app_running:
        record = get_record()
        # move x
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i][0] += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
        # move y
        anim_count += anim_speed
        if anim_count > anim_list:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i][1] += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i][1]][figure_old[i][0]] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i][1] - center[1]
                y = figure[i][0] - center[0]
                figure[i][0] = center[0] - x
                figure[i][1] = center[1] + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        # check lines
        line, lines = h - 1, 0
        for row in range(h - 1, -1, -1):
            count = 0
            for i in range(w):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < w:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        # compute score
        score += scores[lines]

        fig = []
        # draw figure
        for i in range(4):
            figure_rect_x = figure[i][0] * tile
            figure_rect_y = figure[i][1] * tile
            fig.append(
                sc_game.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + tile, figure_rect_y + tile,
                                         fill=rgb_to_hex(color)))

        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect_x, figure_rect_y = x * tile, y * tile
                    fig.append(sc_game.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + tile,
                                                        figure_rect_y + tile, fill=rgb_to_hex(col)))

        fig2 = []
        # draw next figure
        for i in range(4):
            figure_rect_x = next_figure[i][0] * tile + 380
            figure_rect_y = next_figure[i][1] * tile + 185
            fig2.append(canvas.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + tile, figure_rect_y + tile,
                                            fill=rgb_to_hex(next_color)))
        # draw titles
        canvas.itemconfigure(_score, text=str(score))
        canvas.itemconfigure(_record, text=record)

        # game over
        for i in range(w):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(w)] for i in range(h)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for item in grid:
                    sc_game.itemconfigure(item, fill=rgb_to_hex(get_color()))
                    time.sleep(0.005)
                    tk.update_idletasks()
                    tk.update()

                for item in grid:
                    sc_game.itemconfigure(item, fill="")

        dx, rotate = 0, False
        tk.update_idletasks()
        tk.update()
        for id_fig in fig: sc_game.delete(id_fig)
        for id_fig in fig2: canvas.delete(id_fig)
    time.sleep(0.005)

# tk.destroy()
#tk.mainloop()
