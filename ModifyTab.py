from PySide6.QtWidgets import(
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QCheckBox,
    QLabel,
    QSpinBox,
    QGroupBox
)

MAX_RES_PX = 999999999
MAX_FILE_SIZE = 1024**2   # KiB

class ModifyTab(QWidget):
    def __init__(self):
        super(ModifyTab, self).__init__()

        # Set Main Layout
        tab_lt = QGridLayout()
        self.setLayout(tab_lt)
        
        self.downscale_lt = QVBoxLayout()
        downscale_grp = QGroupBox("Downscaling")
        downscale_grp.setLayout(self.downscale_lt)

        # Enable Downscaling
        self.downscaling_cb = QCheckBox("Downscale")
        self.downscale_lt.addWidget(self.downscaling_cb)
        self.downscaling_cb.stateChanged.connect(self.toggleDownscaleUI)

        # Scale by
        self.mode_lt = QHBoxLayout()
        self.mode_lt.addWidget(QLabel("Scale by"))
        self.downscale_lt.addLayout(self.mode_lt)

        self.mode_cmb = QComboBox()
        self.mode_cmb.addItems(("Percent", "Pixels", "Max Filesize"))
        self.mode_cmb.currentIndexChanged.connect(self.onModeChanged)
        self.mode_lt.addWidget(self.mode_cmb)

        # Percent
        scl_p_lt = QHBoxLayout()
        self.scl_p_l = QLabel("Percent")
        self.scl_p_sb = QSpinBox()
        self.scl_p_sb.setRange(1, 99)
        
        self.scl_p_sb.setSuffix(" %")
        
        scl_p_lt.addWidget(self.scl_p_l)
        scl_p_lt.addWidget(self.scl_p_sb)
        self.downscale_lt.addLayout(scl_p_lt)

        # Pixels - Width
        scl_px_w_lt = QHBoxLayout()
        self.scl_px_w_l = QLabel("Max Width")
        self.scl_px_w_sb = QSpinBox()
        self.scl_px_w_sb.setRange(1, MAX_RES_PX)
        self.scl_px_w_sb.setSuffix(" px")
        
        scl_px_w_lt.addWidget(self.scl_px_w_l)
        scl_px_w_lt.addWidget(self.scl_px_w_sb)
        self.downscale_lt.addLayout(scl_px_w_lt)
        
        # Pixels - Height
        scl_px_h_lt = QHBoxLayout()
        self.scl_px_h_l = QLabel("Max Height")
        self.scl_px_h_sb = QSpinBox()
        self.scl_px_h_sb.setRange(1, MAX_RES_PX)
        self.scl_px_h_sb.setSuffix(" px")
        
        scl_px_h_lt.addWidget(self.scl_px_h_l)
        scl_px_h_lt.addWidget(self.scl_px_h_sb)
        self.downscale_lt.addLayout(scl_px_h_lt)

        # Filesize
        scl_fs_lt = QHBoxLayout()
        self.scl_fs_l = QLabel("Max File Size")
        self.scl_fs_sb = QSpinBox()
        self.scl_fs_sb.setRange(0, MAX_FILE_SIZE)
        self.scl_fs_sb.setSuffix(" KiB")
        
        scl_fs_lt.addWidget(self.scl_fs_l)
        scl_fs_lt.addWidget(self.scl_fs_sb)
        self.downscale_lt.addLayout(scl_fs_lt)

        # Filesize - Step
        scl_fs_s_lt = QHBoxLayout()
        self.scl_fs_s_l = QLabel("Step")
        self.scl_fs_s_sb = QSpinBox()
        self.scl_fs_s_sb.setRange(0, MAX_FILE_SIZE)
        self.scl_fs_s_sb.setSuffix(" %")
        
        scl_fs_s_lt.addWidget(self.scl_fs_s_l)
        scl_fs_s_lt.addWidget(self.scl_fs_s_sb)
        self.downscale_lt.addLayout(scl_fs_s_lt)

        # Resample
        rs_lt = QHBoxLayout()
        rs_lt.addWidget(QLabel("Resample"))
        self.rs_cmb = QComboBox()
        self.rs_cmb.addItems(("Default", "Point"))

        # Regarding Resampling - resources
        # https://imagemagick.org/script/command-line-options.php#filter
        # https://github.com/ImageMagick/ImageMagick/blob/main/MagickCore/resize.c
        # https://imagemagick.org/script/command-line-options.php#list

        rs_lt.addWidget(self.rs_cmb)
        self.downscale_lt.addLayout(rs_lt)

        # Misc
        misc_grp = QGroupBox("Misc.")
        misc_grp_lt = QVBoxLayout()
        misc_grp.setLayout(misc_grp_lt)

        # Metadata
        self.metadata_cb = QCheckBox("Preserve Metadata")
        misc_grp_lt.addWidget(self.metadata_cb)

        # Date / Time
        self.date_time_cb = QCheckBox("Preserve Date && Time")
        misc_grp_lt.addWidget(self.date_time_cb)

        # Bottom
        default_btn = QPushButton("Reset to Default")
        default_btn.clicked.connect(self.resetToDefault)
        convert_btn = QPushButton("Convert")    # To be removed??

        tab_lt.addWidget(default_btn,2,0)
        tab_lt.addWidget(convert_btn,2,1)

        # Set Default
        self.resetToDefault()
        self.toggleDownscaleUI(False)
        self.onModeChanged()

        # Add to main layout
        tab_lt.addWidget(downscale_grp,0,0)
        tab_lt.addWidget(misc_grp,0,1)
    
    def toggleDownscaleUI(self, n):
        self.mode_cmb.setEnabled(n)
        self.scl_fs_sb.setEnabled(n)
        self.scl_fs_s_sb.setEnabled(n)
        self.scl_fs_s_l.setEnabled(n)
        self.scl_p_sb.setEnabled(n)
        self.scl_px_w_sb.setEnabled(n)
        self.scl_px_h_sb.setEnabled(n)
        self.rs_cmb.setEnabled(n)

    def resetToDefault(self):
        self.mode_cmb.setCurrentIndex(0)
        self.scl_fs_sb.setValue(300)
        self.scl_fs_s_sb.setValue(10)
        self.scl_p_sb.setValue(80)
        self.scl_px_w_sb.setValue(2000)
        self.scl_px_h_sb.setValue(2000)
    
    def onModeChanged(self):
        index = self.mode_cmb.currentText()
        if index == "Percent":
            self.scl_p_l.setVisible(True)
            self.scl_p_sb.setVisible(True)
        else:
            self.scl_p_l.setVisible(False)
            self.scl_p_sb.setVisible(False)

        if index == "Pixels":
            self.scl_px_h_l.setVisible(True)
            self.scl_px_h_sb.setVisible(True)
            self.scl_px_w_l.setVisible(True)
            self.scl_px_w_sb.setVisible(True)
        else:
            self.scl_px_h_l.setVisible(False)
            self.scl_px_h_sb.setVisible(False)
            self.scl_px_w_l.setVisible(False)
            self.scl_px_w_sb.setVisible(False)
        
        if index == "Max Filesize":
            self.scl_fs_l.setVisible(True)
            self.scl_fs_sb.setVisible(True)
            self.scl_fs_s_sb.setVisible(True)
            self.scl_fs_s_l.setVisible(True)
        else:
            self.scl_fs_l.setVisible(False)
            self.scl_fs_sb.setVisible(False)
            self.scl_fs_s_sb.setVisible(False)
            self.scl_fs_s_l.setVisible(False)
    
    def getSettings(self):
        params = {
            "downscaling": {
                "enable": self.downscaling_cb.isChecked(),
                "mode": self.mode_cmb.currentText(),
                "percent": self.scl_p_sb.value(),
                "filesize_step": self.scl_fs_s_sb.value(),
                "width": self.scl_px_w_sb.value(),
                "height": self.scl_px_w_sb.value(),
                "filesize": self.scl_fs_sb.value(),
                "resample": self.rs_cmb.currentText().lower()
            },
            "misc": {
                "metadata": self.metadata_cb.isChecked(),
                "date_time": self.date_time_cb.isChecked()
            }
        }
        return params