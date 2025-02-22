from PySide6.QtWidgets import(
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
)
from PySide6.QtCore import(
    Qt,
    QUrl,
)
from PySide6.QtGui import(
    QDesktopServices,
)

from data.constants import VERSION, LICENSE_PATH, LICENSE_3RD_PARTY_PATH
from ui.update_checker import UpdateChecker
from data import fonts

class AboutTab(QWidget):
    def __init__(self):
        super(AboutTab, self).__init__()

        tab_lt = QHBoxLayout()
        self.setLayout(tab_lt)
        self.update_checker = UpdateChecker()

        # Label
        title_l = QLabel(f"XL Converter")
        version_l = QLabel(f"Version {VERSION}")
        credits_l = QLabel(f"""
            <div style='line-height: 120%;'>
            <a href=\"mailto:contact@codepoems.eu\">contact@codepoems.eu</a><br>
            <a href=\"{QUrl.fromLocalFile(LICENSE_PATH).toString()}\">license</a> / 
            <a href=\"{QUrl.fromLocalFile(LICENSE_3RD_PARTY_PATH).toString()}\">3rd party</a>
            </div>
        """)

        title_l.setOpenExternalLinks(True)
        credits_l.setOpenExternalLinks(True)

        ## Label - styles
        title_l.setFont(fonts.ABOUT_TITLE)
        version_l.setFont(fonts.ABOUT_VERSION)
        credits_l.setFont(fonts.ABOUT_DESC)

        title_l.setStyleSheet("padding-bottom: 3px;")
        version_l.setStyleSheet("padding-bottom: 5px;")

        title_l.setAlignment(Qt.AlignCenter)
        version_l.setAlignment(Qt.AlignCenter)
        credits_l.setAlignment(Qt.AlignCenter)
        
        text_vb = QVBoxLayout()
        text_vb.addWidget(title_l)
        text_vb.addWidget(version_l)
        text_vb.addWidget(credits_l)
        tab_lt.addLayout(text_vb)

        # Buttons
        buttons_vb = QVBoxLayout()

        self.update_btn = QPushButton("Check for Updates", clicked=self.checkForUpdate)
        self.update_checker.finished.connect(lambda: self.update_btn.setEnabled(True))
        self.manual_btn = QPushButton("Manual", clicked=lambda: QDesktopServices.openUrl(QUrl("https://xl-docs.codepoems.eu/")))
        self.report_bug_btn = QPushButton("Report Bug", clicked=lambda: QDesktopServices.openUrl(QUrl("https://github.com/JacobDev1/xl-converter/issues")))
        self.website_btn = QPushButton("Website", clicked=lambda: QDesktopServices.openUrl(QUrl("https://codepoems.eu/xl-converter")))
        self.donate_btn = QPushButton("Donate", clicked=lambda: QDesktopServices.openUrl(QUrl("https://codepoems.eu/donate")))

        buttons_vb.addWidget(self.update_btn)
        buttons_vb.addWidget(self.manual_btn)
        buttons_vb.addWidget(self.report_bug_btn)
        buttons_vb.addWidget(self.website_btn)
        buttons_vb.addWidget(self.donate_btn)
        tab_lt.addLayout(buttons_vb)

        # Layout

        text_vb.setAlignment(Qt.AlignVCenter)
        buttons_vb.setAlignment(Qt.AlignVCenter)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def checkForUpdate(self):
        self.update_checker.run()
        self.update_btn.setEnabled(False)