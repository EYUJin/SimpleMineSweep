from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from time import time
from random import sample


class MineGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 350, 400)

        self.setWindowTitle("지뢰 찾기")

        _icon = QIcon(
            "./elmo.png"
        )
        self.setWindowIcon(_icon)  # PyQT는 camel 표기법 따름에 유의하자

        # Blocks Left
        self.num_blocks = 16
        self.remain_cnt = self.num_blocks

        # Bombs (2)
        self.bomb_idcs = sample(
            range(self.num_blocks),
            k=2,
        )

        # Status Label: Blocks left / Game over
        self.main_label = QLabel(self)
        self.main_label.resize(300, 30)
        self.main_label.move(10, 10)
        self.dispStatus()
        # Time left
        self.time_left = 120  # secs
        self.start_time = int(time())
        self.clock_label = QLabel(self)
        self.clock_label.resize(300, 30)
        self.clock_label.move(200, 10)
        self.displayTime()

        self.blocks = []  # list of objects
        for r in range(self.num_blocks//4):
            for c in range(self.num_blocks//4):
                _button = QPushButton(text="■", parent=self)
                _button.move(50 + r*55, 50 + c*55)
                _button.resize(50, 50)
                _button.clicked.connect(self.buttonAction)
                self.blocks.append(_button)
        self.bomb_blocks = [
            self.blocks[self.bomb_idcs[0]],
            self.blocks[self.bomb_idcs[1]],
        ]

        rstButton = QPushButton(text="Reset", parent=self)
        rstButton.move(200, 300)
        rstButton.clicked.connect(self.rstButtonAction)

        timer = QTimer(self)
        timer.start(1000)  # 1 sec
        timer.timeout.connect(self.displayTime)

    def dispStatus(self):
        self.main_label.setText(
            f"Blocks Left: {self.remain_cnt}"
        )

    def buttonAction(self):
        obj = self.sender()
        if obj not in self.bomb_blocks:
            obj.setText(
                f" "
            )
            self.remain_cnt -= 1
            self.dispStatus()
        else:
            self.game_over()

    def rstButtonAction(self):
        for b in self.blocks:
            b.setText("■")
        self.remain_cnt = self.num_blocks
        self.time_left = 120
        self.start_time = int(time())
        self.dispStatus()

    def displayTime(self):
        self.time_left -= 1
        if self.time_left >= 0:
            self.clock_label.setText(
                f"Left Time: {self.time_left}"
            )
        else:
            self.game_over()

    def game_over(self):
        self.time_left = 0
        self.main_label.setText(
            "Game Over"
        )
        for block in self.bomb_blocks:
            block.setText("♨")


# event loop
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MineGame()
    win.show()
    app.exec_()
