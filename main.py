from tkinter import *
from tkinter.font import Font

from ChooseBlocksCanvas import ChooseBlocksCanvas
from MoveBlocksCanvas import MoveBlocksCanvas


def main():
    root = Tk()
    #root2 = Tk()
    root.geometry("+1+1")
    Button(command=root.quit, text="Quit").pack()
    myFont = Font(family="Verdana", size=10)
    myFontBold = Font(family="Verdana", size=10, weight='bold')
    t1 = ChooseBlocksCanvas(root, myFont, myFontBold)
    t1.top.geometry("500x500")
    ChooseBlocksCanvas.create_blocks_fst(t1)
    t2 = MoveBlocksCanvas(root, t1, myFont, myFontBold)
    Button(root, text='To code', command=t2.to_code).pack()
    Button(root, text='To blocks', command=t2.to_blocks).pack()
    t2.top.geometry("500x500")
    t2.create_bin()
    root.mainloop()


main()
