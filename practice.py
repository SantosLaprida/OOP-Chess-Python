from chessboard.boardutils import BoardUtils
from chessboard.boardutils import NUM_SQUARES
from chessboard.boardutils import NUM_SQUARES_ROW

columns = [
    [i % NUM_SQUARES_ROW == 0 for i in range(NUM_SQUARES)],
    [i % NUM_SQUARES_ROW == 1 for i in range(NUM_SQUARES)],
    [i % NUM_SQUARES_ROW == 2 for i in range(NUM_SQUARES)],
    [i % NUM_SQUARES_ROW == 3 for i in range(NUM_SQUARES)],
    [i % NUM_SQUARES_ROW == 4 for i in range(NUM_SQUARES)],
    [i % NUM_SQUARES_ROW == 5 for i in range(NUM_SQUARES)],
    [i % NUM_SQUARES_ROW == 6 for i in range(NUM_SQUARES)],
    [i % NUM_SQUARES_ROW == 7 for i in range(NUM_SQUARES)]
    ]

notation_dict = {}

for i in range(len(columns)):
    notation_dict[i + 1] = [j for j, value in enumerate(columns[i]) if value]



print(len(notation_dict[1]))
print(notation_dict)
