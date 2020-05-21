import numpy as np
from graphics import show_mat


def parse_digits():
    all_digits = []
    with open("Digits_Ex3.txt", 'r') as f:
        board = []
        for row in f:
            if not row.strip() and board:
                board = np.array(board)
                all_digits.append(board)
                board = []
            else:
                board.append([int(n) for n in row.strip()])
    return all_digits


def visualize_dataset():
    all_digits = parse_digits()
    comb = np.concatenate([np.concatenate(all_digits[i:i+10], axis=1)
                           for i in range(0, 100, 10)], axis=0)
    show_mat(comb)


if __name__ == '__main__':
    visualize_dataset()
