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
        self._apply_styles()
        self._build_ui()

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0d1117;
            }
            QLabel {
                color: #c9d1d9;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: bold;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #161b22;
                color: #58a6ff;
                border: 1px solid #30363d;
                border-radius: 6px;
                padding: 8px;
                font-family: 'Consolas', 'JetBrains Mono', monospace;
            }
            QLineEdit:focus {
                border: 1px solid #58a6ff;
            }
            QPushButton {
                background-color: #238636;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
            QPushButton:pressed {
                background-color: #1f6feb;
            }
            QTextBrowser {
                background-color: #0d1117;
                color: #c9d1d9;
                border: none;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
            }
            #sidebar {
                background-color: #161b22;
                border-right: 1px solid #30363d;
            }
        """)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0) # Flush to edges
        layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar") # Tagged for QSS
        sidebar.setFixedWidth(320)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(20, 20, 20, 20)
        sb_layout.setSpacing(15)

        sb_layout.addWidget(QLabel("STUDENT FEATURE INPUT"))
        self.feature_input = QLineEdit()
        self.feature_input.setPlaceholderText("[Study, Attend, ... Stress]")
        sb_layout.addWidget(self.feature_input)

        self.predict_btn = QPushButton("EXECUTE PREDICTION")
        self.predict_btn.clicked.connect(self._predict_clicked)
        sb_layout.addWidget(self.predict_btn)
        sb_layout.addStretch()
        layout.addWidget(sidebar)

        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(20, 20, 20, 20)

        self.chat_display = QTextBrowser()
        chat_layout.addWidget(self.chat_display)

        input_row = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Query the system... ('clear' or 'reset' for context clear)")
        self.input_field.returnPressed.connect(self._send_message)

        send_btn = QPushButton("SEND")
        send_btn.setStyleSheet("background-color: #1f6feb;")
        send_btn.clicked.connect(self._send_message)

        input_row.addWidget(self.input_field)
        input_row.addWidget(send_btn)
        chat_layout.addLayout(input_row)
        layout.addWidget(chat_container)

    def _predict_clicked(self):
        text = self.feature_input.text()
        try:
            student_data = ast.literal_eval(text)
            if len(student_data) != 15:
                raise ValueError("Need 15 features")
        except Exception:
            self._append("SYSTEM", "ERR: Invalid input matrix.")
            return

        self._append("SYSTEM", "Processing prediction matrix...")
        self.worker = ChatWorker(self.bot, "", student_data)
        self.worker.finished.connect(self._on_response)
        self.worker.start()

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self._append("USER", text)
        self.input_field.clear()
        self.worker = ChatWorker(self.bot, text)
        self.worker.finished.connect(self._on_response)
        self.worker.start()

    def _on_response(self, text):
        self._append("AI", text)

    def _append(self, role, text):
        # PyQt HTML is primitive, use tables/divs for pseudo-bubbles
        if role == "USER":
            color = "#1f6feb" # Blue
            align = "right"
        elif role == "SYSTEM":
            color = "#d73a49" # Red
            align = "left"
        else:
            color = "#238636" # Green
            align = "left"

        html = f"""
        <div style='margin-bottom: 12px; text-align: {align};'>
            <span style='background-color: {color}; color: white; padding: 4px 8px; font-size: 11px; font-weight: bold; border-radius: 4px;'>
                {role}
            </span>
            <br>
            <span style='color: #c9d1d9; font-size: 14px;'>{text}</span>
        </div>
        """
        self.chat_display.append(html)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = StudentAIConsole()

    window.show()

    sys.exit(app.exec())
