import sys
import json
import ast

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QTextBrowser, QLineEdit, QPushButton,
    QLabel, QFrame
)

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor

from core.orchestrator import Orchestrator

# Worker Thread

class ChatWorker(QThread):

    finished = pyqtSignal(str)

    def __init__(self, bot, text, student_data=None):
        super().__init__()
        self.bot = bot
        self.text = text
        self.student_data = student_data

    def run(self):

        try:

            if self.student_data:
                result = self.bot.run_grade_prediction(self.student_data)
            else:
                result = self.bot.run(self.text)

        except Exception as e:
            result = f"Error: {e}"

        self.finished.emit(result)

# UI

class StudentAIConsole(QMainWindow):

    def __init__(self):

        super().__init__()

        self.bot = Orchestrator()

        self.setWindowTitle("AI Academic Performance Advisor")
        self.resize(1100, 700)

        self._build_ui()


   

    def _build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        
        # LEFT PANEL (student data)
        

        sidebar = QFrame()
        sidebar.setFixedWidth(320)

        sb_layout = QVBoxLayout(sidebar)

        sb_layout.addWidget(QLabel("Student Feature Input"))

        self.feature_input = QLineEdit()
        self.feature_input.setPlaceholderText(
            "[StudyHours, Attendance, Resources, ... StressLevel]"
        )

        sb_layout.addWidget(self.feature_input)

        self.predict_btn = QPushButton("Predict Grade")

        self.predict_btn.clicked.connect(self._predict_clicked)

        sb_layout.addWidget(self.predict_btn)

        sb_layout.addStretch()

        layout.addWidget(sidebar)


        
        # RIGHT PANEL (chat)
        

        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)

        self.chat_display = QTextBrowser()

        chat_layout.addWidget(self.chat_display)

        input_row = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask about student performance...")

        self.input_field.returnPressed.connect(self._send_message)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self._send_message)

        input_row.addWidget(self.input_field)
        input_row.addWidget(send_btn)

        chat_layout.addLayout(input_row)

        layout.addWidget(chat_container)


   
    # Prediction
   

    def _predict_clicked(self):

        text = self.feature_input.text()

        try:

            student_data = ast.literal_eval(text)

            if len(student_data) != 15:
                raise ValueError("Need 15 features")

        except Exception:

            self._append("SYSTEM", "Invalid input format.")
            return

        self._append("SYSTEM", "Running prediction...")

        self.worker = ChatWorker(self.bot, "", student_data)

        self.worker.finished.connect(self._on_response)

        self.worker.start()


   
    # Chat
   

    def _send_message(self):

        text = self.input_field.text().strip()

        if not text:
            return

        self._append("USER", text)

        self.input_field.clear()

        self.worker = ChatWorker(self.bot, text)

        self.worker.finished.connect(self._on_response)

        self.worker.start()

    # Output handling

    def _on_response(self, text):

        self._append("AI", text)


    def _append(self, role, text):

        html = f"""
        <div style='margin-bottom:10px'>
        <b>{role}</b><br>
        {text}
        </div>
        """

        self.chat_display.append(html)

        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = StudentAIConsole()

    window.show()

    sys.exit(app.exec())