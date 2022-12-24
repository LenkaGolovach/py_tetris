from tkinter import *
from tkinter import messagebox
from random import randrange, choice
from copy import deepcopy

w, h = 10,20
tile = 45
game_res = w * tile, h * tile
res = 750, 940
fps = 60

def on_closing():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        tk.destroy()


tk = Tk()
tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Tetris")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
#tk.iconbitmap("bomb-3175208_640.ico")

canvas = Canvas(tk, width=res[0], height=res[1], bg="red", highlightthickness=0)
canvas.pack()

sc_game = Canvas(tk, width=w * tile + 1, height=h * tile + 1, bg="purple", highlightthickness=0)
sc_game.place(x=20, y=20, anchor=NW)

img_obj1 = PhotoImage(file="img/vasya.png")
canvas.create_image(0, 0, anchor=NW, image=img_obj1)

img_obj2 = PhotoImage(file="img/krol.png")
sc_game.create_image(0, 0, anchor=NW, image=img_obj2)


grid = [sc_game.create_rectangle(x * tile, y * tile, x * tile + tile, y * tile + tile) for x in range(w) for y in range(h)]
# for item in grid:
#     sc_game.move(item, 20, 20)

score = 0
record = "0"

canvas.create_text(505, 30, text="TETRIS", font=("Arial", 45),fill="red", anchor=NW)
canvas.create_text(535, 780, text="score:", font=("Arial", 45),fill="blue", anchor=NW)
canvas.create_text(550, 840, text=str(score), font=("Arial", 45),fill="black", anchor=NW)
canvas.create_text(525, 650, text="record:", font=("Arial", 45),fill="gold", anchor=NW)
canvas.create_text(550, 710, text=record, font=("Arial", 45),fill="gold", anchor=NW)

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[(x + w // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

#draw figure
for i in range(4):
    figure_rect_x = figure[i][0] * tile
    figure_rect_y = figure[i][1] * tile
    sc_game.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + tile, figure_rect_y + tile, fill = rgb_to_hex(color))

#draw next figure
for i in range(4):
    figure_rect_x = next_figure[i][0] * tile + 380
    figure_rect_y = next_figure[i][1] * tile + 185
    canvas.create_rectangle(figure_rect_x, figure_rect_y, figure_rect_x + tile, figure_rect_y + tile, fill = rgb_to_hex(next_color))

for item in grid:
    sc_game.itemconfigure(item, fill=rgb_to_hex(get_color()))

for item in grid:
    sc_game.itemconfigure(item, fill="")

tk.mainloop()