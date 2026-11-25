from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QFrame
)

from PySide6.QtCore import Signal

import sqlite3

from database import get_connection



class LoginPage(QWidget):

    login_success = Signal(dict)


    def __init__(self):

        super().__init__()

        self.setup_ui()



    # ===========================
    # User Interface
    # ===========================

    def setup_ui(self):

        layout = QVBoxLayout()


        self.card = QFrame()

        card_layout = QVBoxLayout()



        self.title = QLabel(
            "Smart Market OS"
        )

        self.title.setStyleSheet(
            """
            font-size:28px;
            font-weight:bold;
            """
        )


        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText(
            "Username"
        )


        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Password"
        )

        self.password_input.setEchoMode(
            QLineEdit.Password
        )



        self.login_button = QPushButton(
            "Login"
        )


        self.login_button.clicked.connect(
            self.login
        )



        card_layout.addWidget(
            self.title
        )

        card_layout.addWidget(
            self.username_input
        )

        card_layout.addWidget(
            self.password_input
        )

        card_layout.addWidget(
            self.login_button
        )


        self.card.setLayout(
            card_layout
        )


        layout.addStretch()

        layout.addWidget(
            self.card
        )

        layout.addStretch()


        self.setLayout(
            layout
        )



    # ===========================
    # Login Function
    # ===========================

    def login(self):

        username = self.username_input.text()

        password = self.password_input.text()



        if not username or not password:

            QMessageBox.warning(
                self,
                "Error",
                "Please enter username and password"
            )

            return



        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT id, username, fullname, role
            FROM users
            WHERE username=? AND password=?
            """,
            (
                username,
                password
            )
        )


        result = cursor.fetchone()


        conn.close()



        if result:


            user = {

                "id": result[0],

                "username": result[1],

                "fullname": result[2],

                "role": result[3]

            }


            self.login_success.emit(
                user
            )


            self.password_input.clear()



        else:


            QMessageBox.critical(
                self,
                "Login Failed",
                "Wrong username or password"
            )