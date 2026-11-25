from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)

from database import get_connection

import random



class CashierPage(QWidget):

    def __init__(self):

        super().__init__()

        self.cart = []

        self.setup_ui()



    # ===========================
    # Interface
    # ===========================

    def setup_ui(self):

        layout = QVBoxLayout()



        title = QLabel(
            "Cashier"
        )

        title.setStyleSheet(
            """
            font-size:28px;
            font-weight:bold;
            """
        )



        # Search

        search_layout = QHBoxLayout()


        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Barcode or Product Name"
        )


        search_btn = QPushButton(
            "Add"
        )


        search_btn.clicked.connect(
            self.add_product
        )



        search_layout.addWidget(
            self.search_input
        )

        search_layout.addWidget(
            search_btn
        )



        # Cart Table

        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Product",
                "Price",
                "Quantity",
                "Total"
            ]
        )



        # Total

        self.total_label = QLabel(
            "Total: 0"
        )


        self.total_label.setStyleSheet(
            """
            font-size:20px;
            font-weight:bold;
            """
        )



        sell_btn = QPushButton(
            "Complete Sale"
        )


        sell_btn.clicked.connect(
            self.complete_sale
        )



        layout.addWidget(
            title
        )

        layout.addLayout(
            search_layout
        )

        layout.addWidget(
            self.table
        )

        layout.addWidget(
            self.total_label
        )

        layout.addWidget(
            sell_btn
        )


        self.setLayout(
            layout
        )



    # ===========================
    # Add Product To Cart
    # ===========================

    def add_product(self):

        text = self.search_input.text()


        if not text:

            return



        conn = get_connection()

        cursor = conn.cursor()



        cursor.execute(
            """
            SELECT id,name,sell_price,quantity
            FROM products
            WHERE barcode=? OR name=?
            """,
            (
                text,
                text
            )
        )


        product = cursor.fetchone()


        conn.close()



        if not product:

            QMessageBox.warning(
                self,
                "Not Found",
                "Product not found"
            )

            return



        if product[3] <= 0:

            QMessageBox.warning(
                self,
                "Stock",
                "Product out of stock"
            )

            return



        item = {

            "id": product[0],

            "name": product[1],

            "price": product[2],

            "quantity": 1

        }



        self.cart.append(
            item
        )


        self.update_table()



        self.search_input.clear()



    # ===========================
    # Update Cart Table
    # ===========================

    def update_table(self):

        self.table.setRowCount(
            len(self.cart)
        )


        total = 0



        for row, item in enumerate(self.cart):


            item_total = (
                item["price"]
                *
                item["quantity"]
            )


            total += item_total



            values = [

                item["id"],

                item["name"],

                item["price"],

                item["quantity"],

                item_total

            ]



            for col, value in enumerate(values):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(
                        str(value)
                    )
                )



        self.total_label.setText(
            f"Total: {total}"
        )



    # ===========================
    # Complete Sale
    # ===========================

    def complete_sale(self):


        if not self.cart:

            QMessageBox.warning(
                self,
                "Empty",
                "Cart is empty"
            )

            return



        conn = get_connection()

        cursor = conn.cursor()



        invoice = (
            "INV-"
            +
            str(random.randint(10000,99999))
        )



        total = sum(

            item["price"]
            *
            item["quantity"]

            for item in self.cart

        )



        cursor.execute(
            """
            INSERT INTO sales
            (
            invoice_number,
            total,
            payment_method
            )

            VALUES (?,?,?)
            """,
            (
                invoice,
                total,
                "Cash"
            )
        )



        sale_id = cursor.lastrowid



        for item in self.cart:


            cursor.execute(
                """
                INSERT INTO sale_items
                (
                sale_id,
                product_id,
                quantity,
                price,
                total
                )

                VALUES (?,?,?,?,?)
                """,
                (
                    sale_id,
                    item["id"],
                    item["quantity"],
                    item["price"],
                    item["price"]
                    *
                    item["quantity"]
                )
            )



            cursor.execute(
                """
                UPDATE products
                SET quantity = quantity - ?
                WHERE id=?
                """,
                (
                    item["quantity"],
                    item["id"]
                )
            )



        conn.commit()

        conn.close()



        QMessageBox.information(
            self,
            "Success",
            "Sale completed successfully"
        )


        self.cart.clear()

        self.update_table()