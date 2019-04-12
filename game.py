import tkinter

SETTINGS = {
    "window_title": "RockFall",
    "window_height": "480",
    "window_width": "600",
    "player_height": "20",
    "player_width": "10",
    "player_color": "red"
}

root = tkinter.Tk()
window = tkinter.Canvas(root, height = SETTINGS["window_height"], width = SETTINGS["window_width"])
window.pack()





root.mainloop()