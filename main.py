from products import ProductsPage
from cashier import CashierPage
from customers import CustomersPage
from reports import ReportsPage
from settings import SettingsPage
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QToolBar
)
from PySide6.QtGui import QAction

from database import create_database
from login import LoginPage
from dashboard import Dashboard


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Market OS")

        self.resize(1400, 800)


        # ===========================
        # Pages Container
        # ===========================

        self.pages = QStackedWidget()

        self.setCentralWidget(self.pages)


        # ===========================
        # Pages
        # ===========================

        self.login_page = LoginPage()
        self.dashboard_page = Dashboard()
        self.products_page = ProductsPage()
        self.cashier_page = CashierPage()
        self.customers_page = CustomersPage()
        self.reports_page = ReportsPage()
        self.settings_page = SettingsPage()


        # Add Pages

        self.pages.addWidget(self.login_page)
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.products_page)
        self.pages.addWidget(self.cashier_page)
        self.pages.addWidget(self.customers_page)
        self.pages.addWidget(self.reports_page)
        self.pages.addWidget(self.settings_page)


        # Navigation bar (shown after a successful login)
        self.navigation_bar = QToolBar("Navigation")
        self.addToolBar(self.navigation_bar)
        self.navigation_bar.setVisible(False)

        self.add_navigation_action("Dashboard", "dashboard")
        self.add_navigation_action("Products", "products")
        self.add_navigation_action("Cashier", "cashier")
        self.add_navigation_action("Customers", "customers")
        self.add_navigation_action("Reports", "reports")
        self.add_navigation_action("Settings", "settings")



        # ===========================
        # Login Signal
        # ===========================

        self.login_page.login_success.connect(
            self.open_dashboard
        )

        self.dashboard_page.open_page.connect(
            self.open_page
        )


        # Start With Login

        self.pages.setCurrentWidget(
            self.login_page
        )



    # ===========================
    # Open Dashboard
    # ===========================

    def open_dashboard(self, user):

        self.dashboard_page.set_user(user)

        self.navigation_bar.setVisible(True)

        self.pages.setCurrentWidget(
            self.dashboard_page
        )


    def add_navigation_action(self, title, page_name):

        action = QAction(title, self)

        action.triggered.connect(
            lambda checked=False, name=page_name: self.open_page(name)
        )

        self.navigation_bar.addAction(action)


    def open_page(self, page_name):

        pages = {
            "dashboard": self.dashboard_page,
            "products": self.products_page,
            "cashier": self.cashier_page,
            "customers": self.customers_page,
            "reports": self.reports_page,
            "settings": self.settings_page
        }

        page = pages.get(page_name)

        if page:
            if page_name == "products":
                self.products_page.load_products()
            elif page_name == "customers":
                self.customers_page.load_customers()
            elif page_name == "reports":
                self.reports_page.load_reports()
            elif page_name == "settings":
                self.settings_page.load_settings()

            self.pages.setCurrentWidget(page)



# ===========================
# Application Start
# ===========================

if __name__ == "__main__":


    # Create Database

    create_database()


    app = QApplication(sys.argv)


    window = MainWindow()

    window.show()


    sys.exit(
        app.exec()
    )

    create_database()

    print("==============================")
    print(" Smart Market Database Ready ")
    print("==============================")
