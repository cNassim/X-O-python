# X-O-python

X-O-python is a Python implementation of the classic Tic-Tac-Toe game. This project allows a player to play Tic-Tac-Toe against an AI that uses the Minimax algorithm.

## Features

- Single-player game against an AI
- AI uses the Minimax algorithm
- Graphical User Interface (GUI) using Tkinter and customTkinter

## Requirements

- Python 3.x
- Tkinter
- customTkinter

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/cNassim/X-O-python.git
    ```
2. Navigate to the project directory:
    ```bash
    cd X-O-python
    ```
3. Install the required packages:
    ```bash
    pip install tkinter customtkinter
    ```
4. Run the game:
    ```bash
    python game.py
    ```

## How to Play

1. The game will start with a menu where you can choose the game mode. The game settings are in both English and French.
    - **Classiques**: The classic Tic-Tac-Toe game.
    - **Case Grises**: Similar to the classic mode but with disabled boxes.
    - **Reverse XO**: The goal is to force the opponent to align three boxes of the same color; the first one to do so loses.
2. After selecting the game mode, you will be prompted to configure the game settings. 
    - **Classiques Mode**:
        - Choose if you want to start first.
        - Select the size of the board.
        - Set the difficulty level.
        - Choose your color and the AI's color (you cannot choose the same color).
    - **Case Grises Mode**:
        - Same settings as the Classiques mode.
        - Additionally, choose the number of disabled boxes or let it be random.
        - Alternatively, select the pyramid style where disabled boxes form a pyramid, and choose its position (top, left, right, or down).
    - **Reverse XO Mode**:
        - The objective is to avoid aligning three boxes of the same color.
3. Enjoy the game! :)

## Contributing

Contributions are welcome! If you have any suggestions, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Author

This project was created by [cNassim](https://github.com/cNassim) for a school project.
