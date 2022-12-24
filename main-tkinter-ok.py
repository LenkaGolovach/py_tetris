from tkinter import *
from tkinter import messagebox
from random import randrange, choice

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

img_obj1 = PhotoImage(file="img/vasya.png")
canvas.create_image(0, 0, anchor=NW, image=img_obj1)


grid = [canvas.create_rectangle(x * tile, y * tile, x * tile + tile, y * tile + tile) for x in range(w) for y in range(h)]
for item in grid:
    canvas.move(item, 20, 20)

score = 0
record = "0"

canvas.create_text(505, 30, text="TETRIS", font=("Arial", 45),fill="red", anchor=NW)
canvas.create_text(535, 780, text="score:", font=("Arial", 45),fill="blue", anchor=NW)
canvas.create_text(550, 840, text=str(score), font=("Arial", 45),fill="blue", anchor=NW)
canvas.create_text(525, 650, text="record:", font=("Arial", 45),fill="gold", anchor=NW)
canvas.create_text(550, 710, text=record, font=("Arial", 45),fill="gold", anchor=NW)

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

print(rgb_to_hex(get_color()))

for item in grid:
    canvas.itemconfigure(item, fill=rgb_to_hex(get_color()))

for item in grid:
    canvas.itemconfigure(item, fill="")

tk.mainloop()