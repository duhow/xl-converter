from widget_manager import WidgetManager
import os

from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QComboBox,
    QSlider,
    QLabel,
    QCheckBox,
    QLineEdit,
    QRadioButton,
    QPushButton,
    QFileDialog,
    QSpinBox,
    QSizePolicy,
)

from PySide6.QtCore import(
    Qt,
    Signal
)

class OutputTab(QWidget):
    convert = Signal()
    
    def __init__(self, max_threads):
        super(OutputTab, self).__init__()

        self.wm = WidgetManager("OutputTab")
        self.prev_format = None

        self.MAX_THREAD_COUNT = max_threads

        output_page_lt = QGridLayout()
        self.setLayout(output_page_lt)

        # Conversion Group
        conv_grp = QGroupBox("Conversion")
        conv_grp_lt = QVBoxLayout()
        conv_grp.setLayout(conv_grp_lt)

        threads_hb = QHBoxLayout()
        self.wm.addWidget("threads_sl", QSlider(Qt.Horizontal))
        self.wm.addWidget("threads_sb", QSpinBox())

        self.wm.getWidget("threads_sl").setRange(1, self.MAX_THREAD_COUNT)
        self.wm.getWidget("threads_sb").setRange(1, self.MAX_THREAD_COUNT)
        self.wm.getWidget("threads_sl").setTickInterval(1)
        self.wm.getWidget("threads_sl").valueChanged.connect(self.onThreadSlChange)
        self.wm.getWidget("threads_sb").valueChanged.connect(self.onThreadSbChange)
        
        threads_hb.addWidget(QLabel("Threads"))
        threads_hb.addWidget(self.wm.getWidget("threads_sl"))
        threads_hb.addWidget(self.wm.getWidget("threads_sb"))

        duplicates_hb = QHBoxLayout()
        self.wm.addWidget("duplicates_cmb", QComboBox())
        self.wm.getWidget("duplicates_cmb").addItems(("Replace", "Rename", "Skip"))
        duplicates_hb.addWidget(QLabel("Duplicates"))
        duplicates_hb.addWidget(self.wm.getWidget("duplicates_cmb"))

        conv_grp_lt.addLayout(duplicates_hb)
        conv_grp_lt.addLayout(threads_hb)

        # After Conversion Group
        after_conv_grp = QGroupBox("After Conversion")
        after_conv_grp_lt = QVBoxLayout()
        after_conv_grp.setLayout(after_conv_grp_lt)

        self.wm.addWidget("clear_after_conv_cb", QCheckBox("Clear File List"))
        self.wm.addWidget("delete_original_cb", QCheckBox("Delete Original"))
        self.wm.addWidget("delete_original_cmb", QComboBox())

        self.wm.getWidget("delete_original_cmb").addItems(("To Trash", "Permanently"))
        self.wm.getWidget("delete_original_cb").stateChanged.connect(self.onDeleteOriginalChanged)

        after_conv_grp_lt.addWidget(self.wm.getWidget("clear_after_conv_cb"))
        delete_original_hb = QHBoxLayout()
        delete_original_hb.addWidget(self.wm.getWidget("delete_original_cb"))
        delete_original_hb.addWidget(self.wm.getWidget("delete_original_cmb"))
        after_conv_grp_lt.addLayout(delete_original_hb)

        # Output Group
        output_grp = QGroupBox("Save To")
        output_grp_lt = QVBoxLayout()
        output_grp.setLayout(output_grp_lt)

        self.wm.addWidget("choose_output_src_rb", QRadioButton("Source Folder"))
        self.wm.addWidget("choose_output_ct_rb", QRadioButton("Custom"))
        self.wm.addWidget("choose_output_ct_le", QLineEdit(), "output_ct")
        self.wm.addWidget("choose_output_ct_btn", QPushButton("...",clicked=self.chooseOutput), "output_ct")
        
        self.wm.getWidget("choose_output_ct_rb").toggled.connect(self.onOutputToggled)
        self.wm.getWidget("choose_output_ct_btn").setMaximumWidth(25)

        output_hb = QHBoxLayout()
        output_hb.addWidget(self.wm.getWidget("choose_output_ct_rb"))
        for i in self.wm.getWidgetsByTag("output_ct"):
            output_hb.addWidget(i)

        output_grp_lt.addWidget(self.wm.getWidget("choose_output_src_rb"))
        output_grp_lt.addLayout(output_hb)

        # Format Group
        format_grp = QGroupBox("Format")
        format_grp_lt = QVBoxLayout()
        format_grp.setLayout(format_grp_lt)

        self.wm.addWidget("quality_l", QLabel("Quality"))
        self.wm.addWidget("format_cmb", QComboBox())
        self.wm.getWidget("format_cmb").addItems(("JPEG XL","AVIF", "WEBP", "JPG", "PNG", "Smallest Lossless"))
        self.wm.getWidget("format_cmb").currentIndexChanged.connect(self.onFormatChange)

        self.wm.addWidget("effort_l", QLabel("Effort"), "effort")
        self.wm.addWidget("int_effort_cb", QCheckBox("Intelligent"), "effort")
        self.wm.addWidget("effort_sb", QSpinBox(), "effort")
        self.wm.getWidget("int_effort_cb").toggled.connect(self.onEffortToggled)

        self.wm.addWidget("quality_sb", QSpinBox(), "quality")
        self.wm.addWidget("quality_sl", QSlider(Qt.Horizontal), "quality")
        self.wm.getWidget("quality_sl").setTickInterval(5)

        self.wm.getWidget("quality_sl").valueChanged.connect(self.onQualitySlChanged)
        self.wm.getWidget("quality_sb").valueChanged.connect(self.onQualitySbChanged)

        # Lossless
        self.wm.addWidget("lossless_cb", QCheckBox("Lossless"), "lossless")
        self.wm.addWidget("lossless_if_cb", QCheckBox("Lossless (only if smaller)"), "lossless")
        self.wm.addWidget("max_compression_cb", QCheckBox("Max Compression"))

        self.wm.getWidget("lossless_if_cb").toggled.connect(self.onLosslessToggled)
        self.wm.getWidget("lossless_cb").toggled.connect(self.onLosslessToggled)

        lossless_hb = QHBoxLayout()
        lossless_hb.addWidget(self.wm.getWidget("lossless_cb"))
        lossless_hb.addWidget(self.wm.getWidget("lossless_if_cb"))
        lossless_hb.addWidget(self.wm.getWidget("max_compression_cb"))

        # Assemble Format UI
        format_cmb_hb = QHBoxLayout()
        format_cmb_hb.addWidget(QLabel("Format"))
        format_cmb_hb.addWidget(self.wm.getWidget("format_cmb"))
        format_grp_lt.addLayout(format_cmb_hb)

        effort_hb = QHBoxLayout()
        for i in self.wm.getWidgetsByTag("effort"):
            effort_hb.addWidget(i)
        format_grp_lt.addLayout(effort_hb)

        quality_hb = QHBoxLayout()
        quality_hb.addWidget(self.wm.getWidget("quality_l"))
        quality_hb.addWidget(self.wm.getWidget("quality_sl"))
        quality_hb.addWidget(self.wm.getWidget("quality_sb"))
        format_grp_lt.addLayout(quality_hb)
        
        # Smallest Lossless - Format Pool
        format_sm_l_hb = QHBoxLayout()

        self.wm.addWidget("smallest_lossless_png_cb", QCheckBox("PNG"), "format_pool")
        self.wm.addWidget("smallest_lossless_webp_cb", QCheckBox("WEBP"), "format_pool")
        self.wm.addWidget("smallest_lossless_jxl_cb", QCheckBox("JPEG XL"), "format_pool")
        
        for i in self.wm.getWidgetsByTag("format_pool"):
            format_sm_l_hb.addWidget(i)
        format_grp_lt.addLayout(format_sm_l_hb)

        # Lossless
        format_grp_lt.addLayout(lossless_hb)

        # JPG Reconstruction
        self.wm.addWidget("reconstruct_jpg_cb", QCheckBox("Reconstruct JPG from JPEG XL"))
        format_grp_lt.addWidget(self.wm.getWidget("reconstruct_jpg_cb"))

        # Buttons
        reset_to_default_btn = QPushButton("Reset to Default")
        self.convert_btn_2 = QPushButton("Convert")
        
        reset_to_default_btn.clicked.connect(self.resetToDefault)
        self.convert_btn_2.clicked.connect(self.convert.emit)

        output_page_lt.addWidget(reset_to_default_btn,2,0)
        output_page_lt.addWidget(self.convert_btn_2,2,1)

        # Group Positions
        output_page_lt.addWidget(format_grp,0,1)
        output_page_lt.addWidget(output_grp, 0, 0)
        output_page_lt.addWidget(conv_grp,1,0)
        output_page_lt.addWidget(after_conv_grp,1,1)

        # Size Policy
        output_page_lt.setAlignment(Qt.AlignTop)

        format_grp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        conv_grp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        after_conv_grp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        output_grp.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)    # Minimum so it can spread vertically

        output_grp.setMaximumWidth(400)
        format_grp.setMaximumWidth(400)
        conv_grp.setMaximumWidth(400)
        after_conv_grp.setMaximumWidth(400)

        # Misc
        self.resetToDefault()
        self.wm.loadState()

        # Setup widgets' states
        self.onFormatChange()
        self.onDeleteOriginalChanged()
        self.onOutputToggled()
    
    def isClearAfterConvChecked(self):
        return self.wm.getWidget("clear_after_conv_cb").isChecked()

    def getSettings(self):
        return {
            "format": self.wm.getWidget("format_cmb").currentText(),
            "quality": self.wm.getWidget("quality_sb").value(),
            "lossless": self.wm.getWidget("lossless_cb").isChecked(),
            "lossless_if_smaller": self.wm.getWidget("lossless_if_cb").isChecked(),
            "max_compression": self.wm.getWidget("max_compression_cb").isChecked(),
            "effort": self.wm.getWidget("effort_sb").value(),
            "intelligent_effort": self.wm.getWidget("int_effort_cb").isChecked(),
            "reconstruct_jpg": self.wm.getWidget("reconstruct_jpg_cb").isChecked(),
            "if_file_exists": self.wm.getWidget("duplicates_cmb").currentText(),
            "custom_output_dir": self.wm.getWidget("choose_output_ct_rb").isChecked(),
            "custom_output_dir_path": self.wm.getWidget("choose_output_ct_le").text(),
            "delete_original": self.wm.getWidget("delete_original_cb").isChecked(),
            "delete_original_mode": self.wm.getWidget("delete_original_cmb").currentText(),
            "smallest_format_pool": {
                "png": self.wm.getWidget("smallest_lossless_png_cb").isChecked(),
                "webp": self.wm.getWidget("smallest_lossless_webp_cb").isChecked(),
                "jxl": self.wm.getWidget("smallest_lossless_jxl_cb").isChecked()
                },
        }
    
    def onThreadSlChange(self):
        self.wm.getWidget("threads_sb").setValue(self.wm.getWidget("threads_sl").value())

    def onThreadSbChange(self):
        self.wm.getWidget("threads_sl").setValue(self.wm.getWidget("threads_sb").value())

    def getUsedThreadCount(self):
        return self.wm.getWidget("threads_sl").value()

    def smIsFormatPoolEmpty(self):
        empty = True
        for w in self.wm.getWidgetsByTag("format_pool"):
            if w.isChecked():
                empty = False
        return empty
        
    def chooseOutput(self):
        dlg = QFileDialog()
        dlg.setWindowTitle("Choose Output Folder")
        dlg.setFileMode(QFileDialog.Directory)

        if dlg.exec():
            self.wm.getWidget("choose_output_ct_le").setText(dlg.selectedFiles()[0])

    def onOutputToggled(self):
        src_checked = self.wm.getWidget("choose_output_src_rb").isChecked()
        self.wm.setEnabledByTag("output_ct", not src_checked)
        
    def onFormatChange(self):
        self.saveFormatState()
        
        cur_format = self.wm.getWidget("format_cmb").currentText()
        self.prev_format = cur_format
        
        self.wm.setCheckedByTag("lossless", False)  # Widgets reenable themselves when you use setChecked() on a disabled widget, so this needs to stay in the beginning

        # Enable Lossless Mode
        self.wm.setEnabledByTag("lossless", cur_format in ("JPEG XL", "WEBP"))

        # Effort
        self.wm.getWidget("int_effort_cb").setEnabled(cur_format == "JPEG XL")
        self.wm.getWidget("effort_sb").setEnabled(cur_format in ("JPEG XL", "AVIF"))
        self.wm.getWidget("effort_l").setEnabled(cur_format in ("JPEG XL", "AVIF"))

        if cur_format == "JPEG XL":
            self.onEffortToggled()  # It's very important to update int_effort_cb to avoid issues when changing formats while it's enabled

        # Disable Quality Slider
        self.wm.setEnabledByTag("quality", not cur_format in ("PNG", "Smallest Lossless"))
        self.wm.getWidget("quality_l").setEnabled(not cur_format in ("PNG", "Smallest Lossless"))

        # Quality Slider Range and label
        if cur_format == "AVIF":
            self.wm.getWidget("quality_sl").setRange(-63, 0)
            self.wm.getWidget("quality_sb").setRange(0, 63)
            self.wm.getWidget("effort_sb").setRange(0, 10)
            self.wm.getWidget("quality_l").setText("Constant Quality")
            self.wm.getWidget("effort_l").setText("Speed")
        else:
            if cur_format == "JPEG XL":
                self.setQualityRange(0, 99)
            else:
                self.setQualityRange(1, 100)
            self.wm.getWidget("effort_sb").setRange(1, 9)
            self.wm.getWidget("quality_l").setText("Quality")
            self.wm.getWidget("effort_l").setText("Effort")
        
        # Smallest Lossless mode
        is_sm_l = cur_format == "Smallest Lossless"
        self.wm.setVisibleByTag("lossless", not is_sm_l)
        self.wm.setVisibleByTag("effort", not is_sm_l)
        self.wm.setVisibleByTag("format_pool", is_sm_l)
        self.wm.getWidget("max_compression_cb").setVisible(is_sm_l)
        
        # Decoding (PNG)
        if cur_format == "PNG":
            self.wm.getWidget("reconstruct_jpg_cb").setVisible(True)
            self.wm.setVisibleByTag("lossless", False)
        else:
            self.wm.getWidget("reconstruct_jpg_cb").setVisible(False)

        self.loadFormatState()
        
    def onQualitySlChanged(self):
        self.wm.getWidget("quality_sb").setValue(abs(self.wm.getWidget("quality_sl").value()))

    def onQualitySbChanged(self):
        if self.wm.getWidget("format_cmb").currentText() == "AVIF":
            self.wm.getWidget("quality_sl").setValue(-self.wm.getWidget("quality_sb").value())
        else:
            self.wm.getWidget("quality_sl").setValue(self.wm.getWidget("quality_sb").value())
    
    def onDeleteOriginalChanged(self):
        self.wm.getWidget("delete_original_cmb").setEnabled(self.wm.getWidget("delete_original_cb").isChecked())

    def onEffortToggled(self):
        self.wm.getWidget("effort_sb").setEnabled(not self.wm.getWidget("int_effort_cb").isChecked())

    def onLosslessToggled(self):
        if self.wm.getWidget("lossless_cb").isChecked():
            self.wm.setEnabledByTag("quality", False)
            self.wm.getWidget("lossless_if_cb").setEnabled(False)
        elif self.wm.getWidget("lossless_if_cb").isChecked():
            self.wm.getWidget("lossless_cb").setEnabled(False)
        else:
            self.wm.setEnabledByTag("quality", True)
            self.wm.setEnabledByTag("lossless", True)

    def resetToDefault(self):
        self.wm.cleanVars()

        if self.wm.getWidget("format_cmb").currentText() == "AVIF":
            self.wm.getWidget("quality_sl").setValue(-20)
            self.wm.getWidget("effort_sb").setValue(6)
        else:
            self.wm.getWidget("quality_sl").setValue(80)
            self.wm.getWidget("effort_sb").setValue(7)
        
        self.wm.getWidget("int_effort_cb").setChecked(False)

        self.wm.getWidget("choose_output_src_rb").setChecked(True)

        self.wm.getWidget("delete_original_cb").setChecked(False)
        self.wm.getWidget("delete_original_cmb").setCurrentIndex(0)
        self.wm.getWidget("clear_after_conv_cb").setChecked(False)
        
        self.wm.getWidget("threads_sl").setValue(self.MAX_THREAD_COUNT - 1 if self.MAX_THREAD_COUNT > 0 else 1)  # -1 because the OS needs some CPU time as well
        self.wm.getWidget("duplicates_cmb").setCurrentIndex(1)

        # Lossless
        self.wm.setCheckedByTag("lossless", False)
        self.wm.getWidget("max_compression_cb").setChecked(False)

        # Smallest Lossless
        for i in self.wm.getWidgetsByTag("format_pool"):
            i.setChecked(True)
        
        self.wm.getWidget("reconstruct_jpg_cb").setChecked(True)
    
    def setQualityRange(self, _min, _max):
        for i in self.wm.getWidgetsByTag("quality"):
            i.setRange(_min, _max)

    def saveFormatState(self):
        if self.prev_format == None:
            return

        match self.prev_format:
            case "JPEG XL":
                self.wm.setVar("jxl_quality", self.wm.getWidget("quality_sl").value())
                self.wm.setVar("jxl_effort", self.wm.getWidget("effort_sb").value())
                self.wm.setVar("jxl_int_effort", self.wm.getWidget("int_effort_cb").isChecked())
                self.wm.setVar("jxl_lossless", self.wm.getWidget("lossless_cb").isChecked())
                self.wm.setVar("jxl_lossless_if", self.wm.getWidget("lossless_if_cb").isChecked())
            case "AVIF":
                self.wm.setVar("avif_quality", self.wm.getWidget("quality_sl").value())
                self.wm.setVar("avif_speed", self.wm.getWidget("effort_sb").value())
            case "WEBP":
                self.wm.setVar("webp_quality", self.wm.getWidget("quality_sl").value())
                self.wm.setVar("webp_lossless", self.wm.getWidget("lossless_cb").isChecked())
                self.wm.setVar("webp_lossless_if", self.wm.getWidget("lossless_if_cb").isChecked())
            case "JPG":
                self.wm.setVar("jpg_quality", self.wm.getWidget("quality_sl").value())

    def loadFormatState(self):
        match self.prev_format:
            case "JPEG XL":
                self.wm.applyVar("jxl_quality", "quality_sl", 80)
                self.wm.applyVar("jxl_effort", "effort_sb", 7)
                self.wm.applyVar("jxl_lossless", "lossless_cb", False)
                self.wm.applyVar("jxl_lossless_if", "lossless_if_cb", False)
            case "AVIF":
                self.wm.applyVar("avif_quality", "quality_sl", -20)
                self.wm.applyVar("avif_speed", "effort_sb", 6)
            case "WEBP":
                self.wm.applyVar("webp_quality", "quality_sl", 80)
                self.wm.applyVar("webp_lossless", "lossless_cb", False)
                self.wm.applyVar("webp_lossless_if", "lossless_if_cb", False)
            case "JPG":
                self.wm.applyVar("jpg_quality", "quality_sl", 80)

    def saveState(self):
        self.wm.disableAutoSaving([
            "quality_sb",
            "quality_sl",
            "effort_sb",
            "lossless_cb",
            "lossless_if_cb",
        ])

        self.saveFormatState()
        self.wm.saveState()