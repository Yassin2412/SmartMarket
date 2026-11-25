from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton
)

from database import get_connection



class ReportsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load_reports()



    # ===========================
    # Interface
    # ===========================

    def setup_ui(self):

        layout = QVBoxLayout()



        title = QLabel(
            "Sales Reports"
        )

        title.setStyleSheet(
            """
            font-size:28px;
            font-weight:bold;
            """
        )



        self.sales_count = QLabel(
            "Invoices: 0"
        )


        self.total_sales = QLabel(
            "Total Sales: 0"
        )


        refresh_btn = QPushButton(
            "Refresh"
        )


        refresh_btn.clicked.connect(
            self.load_reports
        )



        self.table = QTableWidget()


        self.table.setColumnCount(
            5
        )


        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Invoice",
                "Total",
                "Payment",
                "Date"
            ]
        )



        layout.addWidget(
            title
        )


        layout.addWidget(
            self.sales_count
        )


        layout.addWidget(
            self.total_sales
        )


        layout.addWidget(
            refresh_btn
        )


        layout.addWidget(
            self.table
        )


        self.setLayout(
            layout
        )



    # ===========================
    # Load Reports
    # ===========================

    def load_reports(self):

        conn = get_connection()

        cursor = conn.cursor()



        # Statistics

        cursor.execute(
            """
            SELECT COUNT(*), 
            SUM(total)
            FROM sales
            """
        )


        stats = cursor.fetchone()



        count = stats[0] or 0

        total = stats[1] or 0



        self.sales_count.setText(
            f"Invoices: {count}"
        )


        self.total_sales.setText(
            f"Total Sales: {total}"
        )



        # Sales Table

        cursor.execute(
            """
            SELECT
            id,
            invoice_number,
            total,
            payment_method,
            created_at

            FROM sales

            ORDER BY id DESC
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