from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFormLayout,
    QDialog,
    QDialogButtonBox
)

from database import get_connection



# ===========================
# Add Product Dialog
# ===========================

class AddProductDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Add Product"
        )


        layout = QFormLayout()



        self.barcode = QLineEdit()

        self.name = QLineEdit()

        self.category = QLineEdit()

        self.supplier = QLineEdit()

        self.buy_price = QLineEdit()

        self.sell_price = QLineEdit()

        self.quantity = QLineEdit()



        layout.addRow(
            "Barcode:",
            self.barcode
        )

        layout.addRow(
            "Name:",
            self.name
        )

        layout.addRow(
            "Category:",
            self.category
        )

        layout.addRow(
            "Supplier:",
            self.supplier
        )

        layout.addRow(
            "Buy Price:",
            self.buy_price
        )

        layout.addRow(
            "Sell Price:",
            self.sell_price
        )

        layout.addRow(
            "Quantity:",
            self.quantity
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

            "barcode":
            self.barcode.text(),

            "name":
            self.name.text(),

            "category":
            self.category.text(),

            "supplier":
            self.supplier.text(),

            "buy_price":
            self.buy_price.text(),

            "sell_price":
            self.sell_price.text(),

            "quantity":
            self.quantity.text()

        }



# ===========================
# Products Page
# ===========================

class ProductsPage(QWidget):


    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_products()



    # ===========================
    # UI
    # ===========================

    def setup_ui(self):

        layout = QVBoxLayout()



        title = QLabel(
            "Products Management"
        )


        title.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )



        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search product..."
        )


        self.search.textChanged.connect(
            self.search_products
        )



        buttons = QHBoxLayout()


        add_btn = QPushButton(
            "Add Product"
        )


        delete_btn = QPushButton(
            "Delete Product"
        )



        add_btn.clicked.connect(
            self.add_product
        )


        delete_btn.clicked.connect(
            self.delete_product
        )



        buttons.addWidget(
            add_btn
        )

        buttons.addWidget(
            delete_btn
        )



        self.table = QTableWidget()


        self.table.setColumnCount(
            8
        )


        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Barcode",
                "Name",
                "Category",
                "Buy",
                "Sell",
                "Quantity",
                "Supplier"
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
    # Load Products
    # ===========================

    def load_products(self):

        conn = get_connection()

        cursor = conn.cursor()



        cursor.execute(
            """
            SELECT
            id,
            barcode,
            name,
            category,
            buy_price,
            sell_price,
            quantity,
            supplier

            FROM products
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
    # Add Product
    # ===========================

    def add_product(self):

        dialog = AddProductDialog()


        if dialog.exec():

            data = dialog.get_data()



            try:

                conn = get_connection()

                cursor = conn.cursor()


                cursor.execute(
                    """
                    INSERT INTO products
                    (
                    barcode,
                    name,
                    category,
                    supplier,
                    buy_price,
                    sell_price,
                    quantity
                    )

                    VALUES (?,?,?,?,?,?,?)
                    """,
                    (
                    data["barcode"],
                    data["name"],
                    data["category"],
                    data["supplier"],
                    float(data["buy_price"]),
                    float(data["sell_price"]),
                    int(data["quantity"])
                    )
                )


                conn.commit()

                conn.close()


                self.load_products()



            except Exception as e:


                QMessageBox.warning(
                    self,
                    "Error",
                    str(e)
                )



    # ===========================
    # Delete Product
    # ===========================

    def delete_product(self):

        row = self.table.currentRow()


        if row < 0:

            return



        product_id = self.table.item(
            row,
            0
        ).text()



        conn = get_connection()

        cursor = conn.cursor()



        cursor.execute(
            "DELETE FROM products WHERE id=?",
            (product_id,)
        )


        conn.commit()

        conn.close()



        self.load_products()



    # ===========================
    # Search
    # ===========================

    def search_products(self):

        text = self.search.text().lower()


        for row in range(
            self.table.rowCount()
        ):

            name = self.table.item(
                row,
                2
            ).text().lower()



            self.table.setRowHidden(
                row,
                text not in name
            )