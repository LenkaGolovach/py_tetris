from tkinter import *
from tkinter import messagebox

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
print(grid)
for item in grid:
    canvas.move(item, 20, 20)


canvas.create_text(200,500,text="TETRIS", font=("Arial", 40),fill="white")

#canvas.create_rectangle(420,120,480,480, fill="darkgreen", outline="")
#canvas.create_text(200,500,text="Hello World!", font=("Arial", 40),fill="white")


tk.mainloop()