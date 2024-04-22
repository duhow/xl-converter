import os

from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QGroupBox,
    QPushButton,
    QLabel,
    QSizePolicy,
    QScrollArea,
    QFormLayout,
    QSpacerItem,
    QLineEdit,
    QTextEdit,
    QPlainTextEdit,
)
from PySide6.QtCore import(
    Signal,
    QObject,
    Qt,
)

from ui.theme import setTheme
from .widget_manager import WidgetManager

class Signals(QObject):
    custom_resampling = Signal(bool)
    disable_sorting = Signal(bool)
    no_exceptions = Signal(bool)
    enable_jxl_effort_10 = Signal(bool)

class SettingsTab(QWidget):
    def __init__(self):
        super(SettingsTab, self).__init__()

        self.main_lt = QGridLayout()
        self.setLayout(self.main_lt)

        self.wm = WidgetManager("SettingsTab")
        self.signals = Signals()

        # Categories
        self.categories_sa = QScrollArea(self)
        self.categories_w = QWidget()
        self.categories_lt = QVBoxLayout(self.categories_w)

        self.categories_w.setLayout(self.categories_lt)
        self.categories_sa.setWidget(self.categories_w)
        self.categories_sa.setWidgetResizable(True)

        # Settings
        self.settings_sa = QScrollArea(self)
        self.settings_w = QWidget()
        self.settings_lt = QFormLayout(self.settings_w)

        self.settings_w.setLayout(self.settings_lt)
        self.settings_sa.setWidget(self.settings_w)
        self.settings_sa.setWidgetResizable(True)

        # Settings - widgets
        self.dark_theme_cb = self.wm.addWidget("dark_theme_cb", QCheckBox("Dark Theme", self))
        self.disable_downscaling_startup_cb = self.wm.addWidget("disable_downscaling_startup_cb", QCheckBox("Disable Downscaling on Startup", self))
        self.disable_delete_startup_cb = self.wm.addWidget("disable_delete_startup_cb", QCheckBox("Disable Delete Original on Startup", self))
        self.no_exceptions_cb = self.wm.addWidget("no_exceptions_cb", QCheckBox("Disable Exception Popups", self))
        self.no_sorting_cb = self.wm.addWidget("no_sorting_cb", QCheckBox("Input - Disable Sorting", self))
        self.enable_jxl_effort_10 = self.wm.addWidget("enable_jxl_effort_10", QCheckBox("JPEG XL - Enable Effort 10", self))
        self.disable_jxl_utf8_check_cb = self.wm.addWidget("disable_jxl_utf8_check_cb", QCheckBox("libjxl - Disable UTF-8 Check", self))
        self.disable_progressive_jpegli_cb = self.wm.addWidget("disable_progressive_jpegli_cb", QCheckBox("JPEGLI - Disable Progressive Scan", self))
        self.custom_resampling_cb = self.wm.addWidget("custom_resampling_cb", QCheckBox("Downscaling - Custom Resampling", self))

        self.custom_args_cb = self.wm.addWidget("custom_args_cb", QCheckBox("Custom Encoder Arguments"))
        self.avifenc_args_l = QLabel("avifenc args")
        self.avifenc_args_te = self.wm.addWidget("avifenc_args_te", QTextEdit())
        self.cjpegli_args_l = QLabel("cjpegli args")
        self.cjpegli_args_te = self.wm.addWidget("cjpegli_args_te", QTextEdit())
        self.cjxl_args_l = QLabel("cjxl args")
        self.cjxl_args_te = self.wm.addWidget("cjxl_args_te", QTextEdit())
        self.im_args_l = QLabel("ImageMagick args")
        self.im_args_te = self.wm.addWidget("im_args_te", QTextEdit())

        # Settings - signals
        self.dark_theme_cb.toggled.connect(self.setDarkModeEnabled)
        self.no_exceptions_cb.toggled.connect(self.signals.no_exceptions)
        self.no_sorting_cb.toggled.connect(self.signals.disable_sorting)
        self.enable_jxl_effort_10.clicked.connect(self.signals.enable_jxl_effort_10)
        self.custom_resampling_cb.toggled.connect(self.signals.custom_resampling.emit)
        self.custom_args_cb.toggled.connect(self.onCustomArgsToggled)

        # Settings - layout
        self.settings_lt.addRow(self.dark_theme_cb)
        self.settings_lt.addRow(self.disable_downscaling_startup_cb)
        self.settings_lt.addRow(self.disable_delete_startup_cb)
        self.settings_lt.addRow(self.no_exceptions_cb)
        self.settings_lt.addRow(self.no_sorting_cb)
        self.settings_lt.addRow(self.enable_jxl_effort_10)
        self.settings_lt.addRow(self.disable_jxl_utf8_check_cb)
        self.settings_lt.addRow(self.custom_resampling_cb)
        self.settings_lt.addRow(self.disable_progressive_jpegli_cb)
        self.settings_lt.addRow(self.custom_args_cb)
        self.settings_lt.addRow(self.cjxl_args_l, self.cjxl_args_te)
        self.settings_lt.addRow(self.avifenc_args_l, self.avifenc_args_te)
        self.settings_lt.addRow(self.cjpegli_args_l, self.cjpegli_args_te)
        self.settings_lt.addRow(self.im_args_l, self.im_args_te)
        
        self.avifenc_args_te.setMaximumHeight(50)
        self.cjpegli_args_te.setMaximumHeight(50)
        self.cjxl_args_te.setMaximumHeight(50)
        self.im_args_te.setMaximumHeight(50)

        self.avifenc_args_te.setAcceptRichText(False)
        self.cjpegli_args_te.setAcceptRichText(False)
        self.cjxl_args_te.setAcceptRichText(False)
        self.im_args_te.setAcceptRichText(False)

        # Categories - widgets
        self.general_btn = QPushButton("General", self)
        self.conversion_btn = QPushButton("Conversion", self)
        self.advanced_btn  = QPushButton("Advanced", self)
        self.restore_defaults_btn = QPushButton("Reset to Default", self)

        self.general_btn.clicked.connect(lambda: self.changeCategory("General"))
        self.conversion_btn.clicked.connect(lambda: self.changeCategory("Conversion"))
        self.advanced_btn.clicked.connect(lambda: self.changeCategory("Advanced"))
        self.restore_defaults_btn.clicked.connect(self.resetToDefault)

        # Categories - layout
        self.categories_lt.addWidget(self.general_btn)
        self.categories_lt.addWidget(self.conversion_btn)
        self.categories_lt.addWidget(self.advanced_btn)
        self.categories_lt.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.categories_lt.addWidget(self.restore_defaults_btn)

        self.general_btn.setCheckable(True)
        self.conversion_btn.setCheckable(True)
        self.advanced_btn.setCheckable(True)

        # Main layout
        self.main_lt.addWidget(self.categories_sa, 0, 0)
        self.main_lt.addWidget(self.settings_sa, 0, 1)

        self.main_lt.setColumnStretch(0, 3)
        self.main_lt.setColumnStretch(1, 7)

        # Misc.
        self.changeCategory("General")
        self.resetToDefault()
        self.wm.loadState()

        # Refresh state
        self.onCustomArgsToggled()

        # Apply Settings
        self.setDarkModeEnabled(self.dark_theme_cb.isChecked())

    def changeCategory(self, category):
        # Set vars
        general = category == "General"
        conversion = category == "Conversion"
        advanced = category == "Advanced"

        # Set checked
        self.general_btn.setChecked(general)
        self.conversion_btn.setChecked(conversion)
        self.advanced_btn.setChecked(advanced)

        # Set visible
        self.dark_theme_cb.setVisible(general)
        self.disable_downscaling_startup_cb.setVisible(general)
        self.disable_delete_startup_cb.setVisible(general)
        self.no_exceptions_cb.setVisible(general)
        self.no_sorting_cb.setVisible(general)
        
        self.disable_progressive_jpegli_cb.setVisible(conversion)

        self.enable_jxl_effort_10.setVisible(advanced)
        self.custom_resampling_cb.setVisible(advanced)
        self.disable_jxl_utf8_check_cb.setVisible(advanced if os.name == "nt" else False)

        self.custom_args_cb.setVisible(advanced)
        self.avifenc_args_l.setVisible(advanced)
        self.avifenc_args_te.setVisible(advanced)
        self.cjxl_args_l.setVisible(advanced)
        self.cjxl_args_te.setVisible(advanced)
        self.cjpegli_args_l.setVisible(advanced)
        self.cjpegli_args_te.setVisible(advanced)
        self.im_args_l.setVisible(advanced)
        self.im_args_te.setVisible(advanced)

    def onCustomArgsToggled(self):
        enabled = self.custom_args_cb.isChecked()

        self.cjxl_args_l.setEnabled(enabled)
        self.cjxl_args_te.setEnabled(enabled)
        self.avifenc_args_l.setEnabled(enabled)
        self.avifenc_args_te.setEnabled(enabled)
        self.cjpegli_args_l.setEnabled(enabled)
        self.cjpegli_args_te.setEnabled(enabled)
        self.im_args_l.setEnabled(enabled)
        self.im_args_te.setEnabled(enabled)

    def setDarkModeEnabled(self, enabled):
        if enabled:
            setTheme("dark")
        else:
            setTheme("light")        

    def setExceptionsEnabled(self, enabled):
        self.blockSignals(True)
        self.no_exceptions_cb.setChecked(enabled)
        self.blockSignals(False)

    def getSettings(self):
        return {
            "custom_resampling": self.custom_resampling_cb.isChecked(),
            "sorting_disabled": self.no_sorting_cb.isChecked(),
            "disable_downscaling_startup": self.disable_downscaling_startup_cb.isChecked(),
            "disable_delete_startup": self.disable_delete_startup_cb.isChecked(),
            "no_exceptions": self.no_exceptions_cb.isChecked(),
            "disable_jxl_utf8_check": self.disable_jxl_utf8_check_cb.isChecked(),
            "enable_jxl_effort_10": self.enable_jxl_effort_10.isChecked(),
            "disable_progressive_jpegli": self.disable_progressive_jpegli_cb.isChecked(),
            "enable_custom_args": self.custom_args_cb.isChecked(),
            "cjxl_args": self.cjxl_args_te.toPlainText(),
            "avifenc_args": self.avifenc_args_te.toPlainText(),
            "cjpegli_args": self.cjpegli_args_te.toPlainText(),
            "im_args": self.im_args_te.toPlainText(),
        }
    
    def resetToDefault(self):
        self.dark_theme_cb.setChecked(True)
        self.no_sorting_cb.setChecked(False)
        self.disable_downscaling_startup_cb.setChecked(True)
        self.disable_delete_startup_cb.setChecked(True)
        self.no_exceptions_cb.setChecked(False)
        
        self.enable_jxl_effort_10.setChecked(False)
        self.custom_resampling_cb.setChecked(False)
        self.disable_jxl_utf8_check_cb.setChecked(False)
        self.disable_progressive_jpegli_cb.setChecked(False)

        self.custom_args_cb.setChecked(False)
        self.cjxl_args_te.clear()
        self.cjpegli_args_te.clear()
        self.im_args_te.clear()
        self.avifenc_args_te.clear()