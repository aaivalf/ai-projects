from tkinter import Button, Label, messagebox
import random
import settings
import sys

from prover import get_safe_cells_from_prover9


def update_board_with_prover9_results():
    safe_cells = get_safe_cells_from_prover9(Cell.all)
    unclicked_safe_cells = []
    for x, y in safe_cells:
        cell = Cell.get_cell_by_axis(x, y)
        if cell and not cell.is_opened:
            cell.show_cell()
            unclicked_safe_cells.append((x, y))
    return unclicked_safe_cells


class Cell:
    all = []
    cell_count = settings.CELL_COUNT #set nr of cells from settings.py
    cell_count_label_object = None #display nr of remaining cells

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine #cell contains mine
        self.is_opened = False #track if cell revealed
        self.is_mine_candidate = False #track if cell potential mine
        self.cell_btn_object = None
        self.x = x
        self.y = y
        self._surrounded_cells=[]
        Cell.all.append(self) #add the cells

    # create cell interaction
    def create_btn_object(self, location):
        btn = Button(
            location,
            width=12,
            height=4,
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            update_board_with_prover9_results()
            #win when nr of cells left = nr of mines
            if Cell.cell_count == settings.MINES_COUNT:
                messagebox.showinfo("Game Over", "Congratulations! You won the game!")

        #if cell opened then cancel interactions with it
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    @staticmethod
    def get_cell_by_axis(x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @surrounded_cells.setter
    def surrounded_cells(self, value):
        self._surrounded_cells = value

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            self.cell_btn_object.configure(
                bg='gray'
            )
        self.is_opened = True

    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        messagebox.showerror("Game Over", "You clicked on a mine")
        #sys.exit()

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg='orange'
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg='gray'
            )
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"