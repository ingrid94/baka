from tkinter import *
from tkinter.font import Font


class ChooseBlocksCanvas:
    def __init__(self, root, myFont, myFontBold):
        self.top = Toplevel(root)
        self.canvas = Canvas(self.top, width=500, height=500, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.myFont = myFont
        self.myFontBold = myFontBold

    def get_focus_set(self):
        return self.canvas.focus_set()

    def gettags(self, int):
        return self.canvas.gettags(int)

    @staticmethod
    def command_block_coords(x, y, h, w):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + w - 5, y, x + w, y + 5,
                  x + w, y + h - 5, x + w - 5, y + h,
                  x + 45, y + h, x + 40, y + h + 5,
                  x + 25, y + h + 5, x + 20, y + h,
                  x + 5, y + h, x, y + h - 5,
                  x, y + 5]
        return points

    @staticmethod
    # x,y are upper left side corner coordinates, h is height of main block, w is width of main block
    # z is length of commands (when condition true) and lower block part to connect with other blocks
    def control_block_coords(x, y, h, w, z):
        points = [x, y + 5, x + 5, y,
                  x + 20, y, x + 25, y + 5,
                  x + 40, y + 5, x + 45, y,
                  x + w - 5, y, x + w, y + 5,
                  x + w, y + h - 5, x + w - 5, y + h,
                  x + 55, y + h, x + 50, y + h + 5,
                  x + 35, y + h + 5, x + 30, y + h,
                  x + 15, y + h, x + 10, y + h + 5,
                  x + 10, y + z + 35,
                  x, y + z + 35, x, y + 5]
        points_lower = [x + 10, y + z + 35, x + 15, y + z + 40,
                        x + 85, y + z + 40, x + 90, y + z + 45,
                        x + 90, y + z + 50,
                        x + 85, y + z + 55, x + 45, y + z + 55,
                        x + 40, y + z + 60, x + 25, y + z + 60,
                        x + 20, y + z + 55, x + 5, y + z + 55,
                        x, y + z + 50, x, y + z + 35]
        return [points, points_lower]

    @staticmethod
    def inside_block_coords(x, y, h, w):
        a = (h / 2)
        points = [x, y + a, x + a, y,
                  x + w, y, x + w + a, y + a,
                  x + w, y + h, x + a, y + h,
                  x, y + a]
        return points

    def create_blocks_fst(self):
        text_height = Font.metrics(self.myFont, 'linespace')
        top_line = 20

        # block for Expr
        self.canvas.create_polygon(self.command_block_coords(50, top_line, text_height+15, 110), fill='violet red',
                                   outline='purple', tags='expr_block')
        self.canvas.create_polygon(self.inside_block_coords(55, top_line + 10, text_height, 90),
                                   fill='light pink', tags='expr_block')
        top_line += text_height+25

        # block for return command
        txt_len = Font.measure(self.myFont, 'return')
        self.canvas.create_polygon(self.command_block_coords(50, top_line, text_height+15, 10 + txt_len + 20 + txt_len),
                                   fill='violet red', outline='purple', tags='return_block')
        self.canvas.create_text(57, top_line+8, anchor=NW, text='return', tags='return_block', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(52+1.3*txt_len, top_line + 10, text_height, txt_len),
                                   fill='light pink', tags='return_block')
        top_line += text_height+25

        # block for variable assignment command
        txt_len = Font.measure(self.myFont, 'variable')
        txt2_len = Font.measure(self.myFontBold, '=')
        self.canvas.create_polygon(self.command_block_coords(50, top_line, text_height+15,
                                                             10 + txt_len + 15 + txt2_len + 15 + txt_len + 10),
                                   fill='violet red', outline='purple', tags='variable_block')
        self.canvas.create_polygon(self.inside_block_coords(60, top_line + 10, text_height, txt_len+5),
                                   fill='dodger blue', outline='steel blue', tags='variable_block')
        self.canvas.create_text(67, top_line+10, anchor=NW, text="variable", tags='variable_block', font=self.myFont)
        self.canvas.create_text(67 + txt_len + 8, top_line+10, anchor=NW, text="=", tags='variable_block', font=self.myFontBold)
        self.canvas.create_polygon(self.inside_block_coords(67 + txt_len + 8 + txt2_len + 5, top_line+10, text_height, txt_len), fill='light pink',
                                   tags='variable_block')
        top_line += text_height+25

        # block for if statement
        txt_len = Font.measure(self.myFont, 'if')
        self.canvas.create_polygon(self.control_block_coords(50, top_line, text_height+15, 10+txt_len+15+8*txt_len+15, 25)[0], fill='orange',
                                   outline='chocolate', tags='if_block')
        self.canvas.create_polygon(self.control_block_coords(50, top_line, text_height+15, 10+txt_len+10+9*txt_len+15, 25)[1], fill='orange',
                                   outline='chocolate', tags='if_block')
        self.canvas.create_text(67, top_line+10, anchor=NW, text='if', tags='if_block', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(67+2*txt_len, top_line+9, text_height, 8*txt_len), fill='peachpuff', tags='if_block')

        top_line += text_height + 75

        # block for while statement
        txt_len = Font.measure(self.myFont, 'while')
        self.canvas.create_polygon(self.control_block_coords(50, top_line, text_height+15, 10+txt_len+15+txt_len+25, 25)[0], fill='orange',
                                   outline='chocolate', tags='while_block')
        self.canvas.create_polygon(self.control_block_coords(50, top_line, text_height+15, 10+txt_len+15+txt_len+25, 25)[1], fill='orange',
                                   outline='chocolate', tags='while_block')
        self.canvas.create_text(60, top_line+10, anchor=NW, text='while', tags='while_block', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(65+txt_len, top_line+9, text_height, 55), fill='peachpuff', tags='while_block')

        top_line += text_height + 75

        txt_len = Font.measure(self.myFont, 'print()')
        self.canvas.create_polygon(self.inside_block_coords(50, top_line, text_height+4, txt_len + 30 + txt_len),
                                   fill='limegreen', outline='green',
                                   tags='print')
        self.canvas.create_text(65, top_line+2, anchor=NW, text="print(", tags='print', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(60+txt_len, top_line+2, text_height, txt_len), fill='lightgreen', tags='print')
        self.canvas.create_text(70+2*txt_len, top_line+2, anchor=NW, text=")", tags='print', font=self.myFont)

        top_line += text_height + 15

        # complete print block
        self.canvas.create_polygon(self.command_block_coords(50, top_line, 2*text_height + 5, 135), fill='violet red',
                                   outline='purple', tags='print_complete')
        self.canvas.create_polygon(self.inside_block_coords(55, top_line+10, text_height+4, txt_len + 30 + txt_len),
                                   fill='limegreen', outline='green',
                                   tags='print_complete')
        self.canvas.create_text(65, top_line + 12, anchor=NW, text="print(", tags='print_complete', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(60 + txt_len, top_line + 12, text_height, txt_len),
                                   fill='lightgreen', tags='print_complete')
        self.canvas.create_text(70 + 2 * txt_len, top_line + 12, anchor=NW, text=")", tags='print_complete', font=self.myFont)
        top_line += text_height + 25

        # right side column
        # equals statement block
        top_line = 20
        txt_len = Font.measure(self.myFontBold, ' == ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*1.2*txt_len+txt_len+15),
                                   fill='dodger blue', outline='steel blue', tags='equals')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line+2, text_height, 1.2*txt_len), fill='sky blue',
                                   tags='equals')
        self.canvas.create_text(312+1.2*txt_len+10, top_line+2, anchor=NW, text="==", tags='equals', font=self.myFontBold)
        self.canvas.create_polygon(self.inside_block_coords(310+1.2*txt_len+txt_len+10,
                                                            top_line+2, text_height, 1.2*txt_len),
                                   fill='sky blue', tags='equals')
        top_line += text_height + 15

        # not equal statement block
        txt_len = Font.measure(self.myFontBold, ' != ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*1.5*txt_len+txt_len+15),
                                   fill='dodger blue', outline='steel blue', tags='not_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line + 2, text_height, 1.5*txt_len),
                                   fill='sky blue', tags='not_equal')
        self.canvas.create_text(312+1.5*txt_len+10, top_line+2, anchor=NW, text="!=", tags='not_equal', font=self.myFontBold)
        self.canvas.create_polygon(self.inside_block_coords(310+1.5*txt_len+txt_len+10,
                                                            top_line+2, text_height, 1.5*txt_len),
                                   fill='sky blue', tags='not_equal')
        top_line += text_height + 15

        # grater than block
        txt_len = Font.measure(self.myFontBold, ' > ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*2*txt_len+txt_len+15), fill='dodger blue', outline='steel blue',
                                   tags='greater')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line+2, text_height, 2*txt_len), fill='sky blue', tags='greater')
        self.canvas.create_text(312+2*txt_len+10, top_line+2, anchor=NW, text=">", tags='greater', font=self.myFontBold)
        self.canvas.create_polygon(self.inside_block_coords(310+2*txt_len+txt_len+10, top_line+2, text_height, 2*txt_len), fill='sky blue', tags='greater')
        top_line += text_height + 15

        # smaller than block
        txt_len = Font.measure(self.myFontBold, ' < ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*2*txt_len+txt_len+15),
                                   fill='dodger blue', outline='steel blue', tags='smaller')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line+2, text_height, 2*txt_len), fill='sky blue',
                                   tags='smaller')
        self.canvas.create_text(312+2*txt_len+10, top_line, anchor=NW, text="<", tags='smaller', font=self.myFontBold)
        self.canvas.create_polygon(self.inside_block_coords(310+2*txt_len+txt_len+10, top_line+2,
                                                            text_height, 2*txt_len), fill='sky blue', tags='smaller')
        top_line += text_height + 15

        # grater or equal block
        txt_len = Font.measure(self.myFontBold, ' >= ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*1.2*txt_len+txt_len+15),
                                   fill='dodger blue', outline='steel blue', tags='greater_or_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line+2, text_height, 1.2*txt_len), fill='sky blue',
                                   tags='greater_or_equal')
        self.canvas.create_text(312+1.2*txt_len+10, top_line, anchor=NW, text=">=", tags='greater_or_equal',
                                font=self.myFontBold)
        self.canvas.create_polygon(self.inside_block_coords(310+1.2*txt_len+txt_len+10,
                                                            top_line+2, text_height, 1.2*txt_len), fill='sky blue',
                                   tags='greater_or_equal')
        top_line += text_height + 15

        # smaller or equal block
        txt_len = Font.measure(self.myFontBold, ' <= ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*1.2*txt_len+txt_len+15),
                                   fill='dodger blue', outline='steel blue', tags='smaller_or_equal')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line+2, text_height, 1.2*txt_len), fill='sky blue',
                                   tags='smaller_or_equal')
        self.canvas.create_text(312+1.2*txt_len+10, top_line, anchor=NW, text="<=", tags='smaller_or_equal', font=self.myFontBold)
        self.canvas.create_polygon(self.inside_block_coords(310+1.2*txt_len+txt_len+10,
                                                            top_line+2, text_height, 1.2*txt_len), fill='sky blue',
                                   tags='smaller_or_equal')
        top_line += text_height + 15

        # or block
        txt_len = Font.measure(self.myFontBold, ' or ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*1.7*txt_len+txt_len+15),
                                   fill='dodger blue', outline='steel blue', tags='or')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line+2, text_height, 1.7*txt_len), fill='sky blue',
                                   tags='or')
        self.canvas.create_text(312+1.7*txt_len+10, top_line, anchor=NW, text="or", tags='or', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(310+1.7*txt_len+txt_len+10, top_line+2, text_height,
                                                            1.7*txt_len), fill='sky blue', tags='or')
        top_line += text_height + 15

        # and block
        txt_len = Font.measure(self.myFont, 'and ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 15+2*1.2*txt_len+txt_len+15),
                                   fill='dodger blue', outline='steel blue', tags='and')
        self.canvas.create_polygon(self.inside_block_coords(310, top_line+2, text_height, 1.2*txt_len), fill='sky blue',
                                   tags='and')
        self.canvas.create_text(310+1.2*txt_len+12, top_line+2, anchor=NW, text="and", tags='and', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(312+1.2*txt_len+txt_len+10,
                                                            top_line+2, text_height, 1.2*txt_len),
                                   fill='sky blue', tags='and')
        top_line += text_height + 15

        # not block
        txt_len = Font.measure(self.myFont, 'not ')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height+4, 10+txt_len+10+1.6*txt_len),
                                   fill='dodger blue', outline='steel blue', tags='not')
        self.canvas.create_text(312, top_line+2, anchor=NW, text='not', tags='not', font=self.myFont)
        self.canvas.create_polygon(self.inside_block_coords(312+txt_len, top_line+2, text_height, 1.6*txt_len),
                                   fill='sky blue', tags='not')
        top_line += text_height + 15

        # block for variable
        txt_len = Font.measure(self.myFont, 'variable')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height, txt_len+20), fill='dodger blue', outline='steel blue',
                                   tags='variable')
        self.canvas.create_text(315, top_line, anchor=NW, text="variable", tags='variable', font=self.myFont)

        # None block
        txt_len = Font.measure(self.myFont, 'None')
        self.canvas.create_polygon(self.inside_block_coords(400, top_line, text_height, txt_len+20), fill='dodger blue', outline='steel blue',
                                   tags='none')
        self.canvas.create_text(415, top_line, anchor=NW, text="None", tags='none', font=self.myFont)

        top_line += text_height + 15

        # block for creating number
        txt_len = Font.measure(self.myFont, 'number')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height, txt_len+20), fill='dodger blue', outline='steel blue',
                                   tags='number')
        self.canvas.create_text(315, top_line, anchor=NW, text="number", tags='number', font=self.myFont)

        # True block
        txt_len = Font.measure(self.myFont, 'True')
        self.canvas.create_polygon(self.inside_block_coords(400, top_line, text_height, txt_len+20), fill='dodger blue', outline='steel blue',
                                   tags='true')
        self.canvas.create_text(415, top_line, anchor=NW, text="True", tags='true', font=self.myFont)
        top_line += text_height + 15

        # block for creating string
        txt_len = Font.measure(self.myFont, 'string')
        self.canvas.create_polygon(self.inside_block_coords(300, top_line, text_height, txt_len+20), fill='dodger blue', outline='steel blue',
                                   tags='string')
        self.canvas.create_text(315, top_line, anchor=NW, text="string", tags='string', font=self.myFont)

        # False block
        txt_len = Font.measure(self.myFont, 'False')
        self.canvas.create_polygon(self.inside_block_coords(400, top_line, text_height, txt_len+25), fill='dodger blue', outline='steel blue',
                                   tags='false')
        self.canvas.create_text(415, top_line, anchor=NW, text="False", tags='false', font=self.myFont)

    def bind(self, function):
        self.canvas.bind("<ButtonPress-1>", function)
