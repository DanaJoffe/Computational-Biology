from graphics.GUI import CellAutomatonGameGUI
from logic.CellAutomatonGame import CellAutomatonGame

if __name__ == '__main__':
    gui = CellAutomatonGameGUI(CellAutomatonGame(200, 200))
    gui.set_all()
    gui.start()


