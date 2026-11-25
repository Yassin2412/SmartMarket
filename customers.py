from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QMessageBox
)

from database import get_connection



# ===========================
# Add Customer Dialog
# ===========================

class AddCustomerDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Add Customer"
        )


        layout = QFormLayout()



        self.name = QLineEdit()

        self.phone = QLineEdit()

        self.address = QLineEdit()



        layout.addRow(
            "Name:",
            self.name
        )

        layout.addRow(
            "Phone:",
            self.phone
        )

        layout.addRow(
            "Address:",
            self.address
        )



        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )


        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )


        layout.addWidget(
            buttons
        )


        self.setLayout(
            layout
        )



    def get_data(self):

        return {

            "name":
            self.name.text(),

            "phone":
            self.phone.text(),

            "address":
            self.address.text()

        }



# ===========================
# Customers Page
# ===========================

class CustomersPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_customers()



    # ===========================
    # UI
    # ===========================

    def setup_ui(self):

        layout = QVBoxLayout()



        title = QLabel(
            "Customers Management"
        )


        title.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )



        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search customer..."
        )


        self.search.textChanged.connect(
            self.search_customers
        )



        buttons = QHBoxLayout()


        add_btn = QPushButton(
            "Add Customer"
        )


        delete_btn = QPushButton(
            "Delete Customer"
        )



        add_btn.clicked.connect(
            self.add_customer
        )


        delete_btn.clicked.connect(
            self.delete_customer
        )



        buttons.addWidget(
            add_btn
        )

        buttons.addWidget(
            delete_btn
        )



        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Phone",
                "Address",
                "Points"
            ]
        )



        layout.addWidget(
            title
        )

        layout.addWidget(
            self.search
        )

        layout.addLayout(
            buttons
        )

        layout.addWidget(
            self.table
        )



        self.setLayout(
            layout
        )



    # ===========================
    # Load Customers
    # ===========================

    def load_customers(self):

        conn = get_connection()

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
            id,
            name,
            phone,
            address,
            points

            FROM customers
            """
        )


        rows = cursor.fetchall()


        conn.close()



        self.table.setRowCount(
            len(rows)
        )


        for row, data in enumerate(rows):

            for col, value in enumerate(data):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )



    # ===========================
    # Add Customer
    # ===========================

    def add_customer(self):

        dialog = AddCustomerDialog()


        if dialog.exec():

            data = dialog.get_data()


            if not data["name"]:

                return



            conn = get_connection()

            cursor = conn.cursor()



            cursor.execute(
                """
                INSERT INTO customers
                (
                name,
                phone,
                address
                )

                VALUES (?,?,?)
                """,
                (
                    data["name"],
                    data["phone"],
                    data["address"]
                )
            )



            conn.commit()

            conn.close()



            self.load_customers()



    # ===========================
    # Delete Customer
    # ===========================

    def delete_customer(self):

        row = self.table.currentRow()


        if row < 0:

            return



        customer_id = self.table.item(
            row,
            0
        ).text()



        conn = get_connection()

        cursor = conn.cursor()



        cursor.execute(
            """
            DELETE FROM customers
            WHERE id=?
            """,
            (
                customer_id,
            )
        )



        conn.commit()

        conn.close()



        self.load_customers()



    # ===========================
    # Search
    # ===========================

    def search_customers(self):

        text = self.search.text().lower()


        for row in range(
            self.table.rowCount()
        ):

            name = self.table.item(
                row,
                1
            ).text().lower()



            self.table.setRowHidden(
                row,
                text not in name
            )