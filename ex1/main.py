from configuration import rows, cols
from graphics.CellAutomatonGameGUI import CellAutomatonGameGUI
from logic.CellAutomatonGame import CellAutomatonGame

if __name__ == '__main__':
    gui = CellAutomatonGameGUI(CellAutomatonGame(rows, cols))
    gui.set_all()
    gui.start()
