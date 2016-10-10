from tkinter import *

from ChooseBlocksCanvas import ChooseBlocksCanvas
from MoveBlocksCanvas import MoveBlocksCanvas


def main():
    root = Tk()
    root.geometry("+1+1")
    Button(command=root.quit, text="Quit").pack()
    t1 = ChooseBlocksCanvas(root)
    t1.top.geometry("+10+100")
    ChooseBlocksCanvas.create_blocks_fst(t1)
    t2 = MoveBlocksCanvas(root, t1)
    t2.top.geometry("+520+100")
    root.mainloop()


main()
