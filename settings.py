from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFormLayout,
    QMessageBox
)

from database import get_connection



class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_settings()



    # ===========================
    # Interface
    # ===========================

    def setup_ui(self):

        main_layout = QVBoxLayout()



        title = QLabel(
            "Market Settings"
        )


        title.setStyleSheet(
            """
            font-size:28px;
            font-weight:bold;
            """
        )



        form = QFormLayout()



        self.market_name = QLineEdit()

        self.phone = QLineEdit()

        self.address = QLineEdit()

        self.tax = QLineEdit()



        form.addRow(
            "Market Name:",
            self.market_name
        )


        form.addRow(
            "Phone:",
            self.phone
        )


        form.addRow(
            "Address:",
            self.address
        )


        form.addRow(
            "Tax (%):",
            self.tax
        )



        save_btn = QPushButton(
            "Save Settings"
        )


        save_btn.clicked.connect(
            self.save_settings
        )



        main_layout.addWidget(
            title
        )


        main_layout.addLayout(
            form
        )


        main_layout.addWidget(
            save_btn
        )


        main_layout.addStretch()



        self.setLayout(
            main_layout
        )



    # ===========================
    # Load Settings
    # ===========================

    def load_settings(self):

        conn = get_connection()

        cursor = conn.cursor()



        cursor.execute(
            """
            SELECT
            market_name,
            phone,
            address,
            tax

            FROM settings

            WHERE id=1
            """
        )


        data = cursor.fetchone()


        conn.close()



        if data:


            self.market_name.setText(
                str(data[0])
            )


            self.phone.setText(
                str(data[1])
            )


            self.address.setText(
                str(data[2])
            )


            self.tax.setText(
                str(data[3])
            )



    # ===========================
    # Save Settings
    # ===========================

    def save_settings(self):

        try:

            conn = get_connection()

            cursor = conn.cursor()



            cursor.execute(
                """
                UPDATE settings

                SET

                market_name=?,

                phone=?,

                address=?,

                tax=?

                WHERE id=1
                """,

                (
                    self.market_name.text(),

                    self.phone.text(),

                    self.address.text(),

                    float(
                        self.tax.text()
                        or 0
                    )
                )
            )



            conn.commit()

            conn.close()



            QMessageBox.information(
                self,
                "Saved",
                "Settings saved successfully"
            )



        except Exception as e:


            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )