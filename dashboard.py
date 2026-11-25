from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)
from PySide6.QtCore import Signal


class Dashboard(QWidget):

    open_page = Signal(str)

    def __init__(self):

        super().__init__()

        self.user = None

        self.setup_ui()



    # ===========================
    # Interface
    # ===========================

    def setup_ui(self):

        main_layout = QVBoxLayout()



        # Title

        self.title = QLabel(
            "Smart Market Dashboard"
        )

        self.title.setStyleSheet(
            """
            font-size:30px;
            font-weight:bold;
            """
        )



        # User Info

        self.user_label = QLabel(
            "Welcome"
        )


        self.user_label.setStyleSheet(
            """
            font-size:18px;
            """
        )



        # Cards Area

        cards_layout = QHBoxLayout()



        self.products_card = self.create_card(
            "Products",
            "Manage products and inventory",
            "products"
        )


        self.cashier_card = self.create_card(
            "Cashier",
            "Create sales invoices",
            "cashier"
        )


        self.reports_card = self.create_card(
            "Reports",
            "View sales reports",
            "reports"
        )


        self.customers_card = self.create_card(
            "Customers",
            "Manage customer information",
            "customers"
        )


        self.settings_card = self.create_card(
            "Settings",
            "Update market settings",
            "settings"
        )



        cards_layout.addWidget(
            self.products_card
        )


        cards_layout.addWidget(
            self.cashier_card
        )


        cards_layout.addWidget(
            self.reports_card
        )


        secondary_cards_layout = QHBoxLayout()

        secondary_cards_layout.addWidget(
            self.customers_card
        )

        secondary_cards_layout.addWidget(
            self.settings_card
        )



        main_layout.addWidget(
            self.title
        )


        main_layout.addWidget(
            self.user_label
        )


        main_layout.addLayout(
            cards_layout
        )


        main_layout.addLayout(
            secondary_cards_layout
        )


        main_layout.addStretch()



        self.setLayout(
            main_layout
        )



    # ===========================
    # Create Dashboard Card
    # ===========================

    def create_card(self, title, text, page_name):

        frame = QFrame()


        layout = QVBoxLayout()



        label_title = QLabel(
            title
        )


        label_title.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )


        label_text = QLabel(
            text
        )


        button = QPushButton(
            "Open"
        )

        button.clicked.connect(
            lambda: self.open_page.emit(page_name)
        )



        layout.addWidget(
            label_title
        )

        layout.addWidget(
            label_text
        )

        layout.addWidget(
            button
        )


        frame.setLayout(
            layout
        )


        return frame



    # ===========================
    # Receive User Data
    # ===========================

    def set_user(self, user):

        self.user = user


        self.user_label.setText(
            f"Welcome {user['fullname']} | Role: {user['role']}"
        )
