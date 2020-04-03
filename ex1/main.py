from GUI import CellAutomatonGameGUI
from logic.CellAutomatonGame import CellAutomatonGame

if __name__ == '__main__':
    gui = CellAutomatonGameGUI(CellAutomatonGame())
    gui.set_all()
    gui.start()


