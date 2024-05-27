from unittest.mock import patch, ANY

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.output_tab import OutputTab

@pytest.fixture
def app(qtbot):
    with patch("ui.output_tab.WidgetManager.loadState"), \
        patch("ui.output_tab.WidgetManager.saveState"):
        app = QApplication.instance()
        if not app:
            app = QApplication([])
        tab = OutputTab(
            4,
            {
                "disable_delete_startup": False,
                "enable_jxl_effort_10": False,
                "enable_quality_precision_snapping": False,
                "jpg_encoder": "JPEGLI",
            }
        )
        qtbot.addWidget(tab)
        return tab

def test_initial_state(app):
    # Format
    settings = app.getSettings()
    assert settings["format"] == "JPEG XL"
    assert settings["quality"] == 80
    assert settings["lossless"] == False
    assert settings["max_compression"] == False
    assert settings["effort"] == 7
    assert settings["intelligent_effort"] == False
    assert settings["reconstruct_jpg"] == True
    assert settings["jxl_modular"] == False
    assert settings["delete_original"] == False
    assert not app.smIsFormatPoolEmpty()

    # Conv.
    assert settings["if_file_exists"] == "Rename"
    assert app.getUsedThreadCount() == 3
    
    # After conv.
    assert not app.isClearAfterConvChecked()
    assert settings["delete_original_mode"] == "To Trash"

    # Save To
    assert settings["custom_output_dir"] == False
    assert settings["custom_output_dir_path"] == ""
    assert settings["keep_dir_struct"] == False

def test_thread_slider_change(app, qtbot):
    qtbot.mouseClick(app.threads_sl, Qt.LeftButton, pos=app.threads_sl.rect().center())
    assert app.threads_sb.value() == app.threads_sl.value()

def test_thread_spinbox_change(app):
    app.threads_sb.setValue(2)
    assert app.threads_sb.value() == 2
    assert app.threads_sb.value() == app.threads_sl.value()

def test_thread_slider_change(app):
    app.quality_sl.setValue(50)
    assert app.quality_sl.value() == 50
    assert app.quality_sl.value() == app.quality_sb.value()

def test_thread_spinbox_change(app):
    app.quality_sb.setValue(50)
    assert app.quality_sb.value() == 50
    assert app.quality_sl.value() == app.quality_sb.value()

def test_deleteOriginal_change(app):
    app.delete_original_cb.setChecked(True)
    assert app.delete_original_cmb.isEnabled()

def test_output_toggled(app):
    app.choose_output_ct_rb.setChecked(True)
    assert app.choose_output_ct_le.isEnabled()
    assert app.choose_output_ct_btn.isEnabled()
    
    app.choose_output_src_rb.setChecked(True)
    assert not app.choose_output_ct_le.isEnabled()
    assert not app.choose_output_ct_btn.isEnabled()

def test_onFormatChange_int_e_toggle(app):
    app.format_cmb.setCurrentIndex(app.format_cmb.findText("JPEG XL"))
    app.int_effort_cb.setChecked(True)

    assert not app.effort_sb.isEnabled()

def test_onFormatChange_lossless_toggled(app):
    app.lossless_cb.setChecked(True)
    
    assert app.lossless_cb.isEnabled()
    assert not app.quality_sl.isEnabled()
    assert not app.quality_sb.isEnabled()
    
    app.lossless_cb.setChecked(False)
    
    assert app.lossless_cb.isEnabled()
    assert app.quality_sl.isEnabled()
    assert app.quality_sb.isEnabled()

@pytest.mark.parametrize("file_format, int_effort, effort, effort_label, quality, lossless, jxl_modular, jpg_encoder, reconstruct_jpg, smallest_lossless, chroma_subsampling", [
    ("JPEG XL", True, True, "Effort", True, True, True, False, False, False, False),
    ("AVIF", False, True, "Speed", True, False, False, False, False, False, True),
    ("WebP", False, False, ANY, True, True, False, False, False, False, False),
    ("JPEG", False, False, ANY, True, False, False, True, False, False, True),
    ("PNG", False, False, ANY, False, False, False, False, True, False, False),
    ("Smallest Lossless", False, False, ANY, False, False, False, False, False, True, False),
])
def test_onFormatChange_visibility(app, file_format, int_effort, effort, effort_label, quality, lossless, jxl_modular, jpg_encoder, reconstruct_jpg, smallest_lossless, chroma_subsampling):
    app.format_cmb.setCurrentIndex(app.format_cmb.findText(file_format))
    assert app.format_cmb.currentText() == file_format
    
    # Effort
    assert app.int_effort_cb.isVisibleTo(app) == int_effort
    assert app.effort_sb.isVisibleTo(app) == effort
    assert app.effort_l.isVisibleTo(app) == effort
    assert app.effort_l.text() == effort_label
    
    # Quality
    assert app.quality_l.isVisibleTo(app) == quality
    assert app.quality_sl.isVisibleTo(app) == quality
    assert app.quality_sb.isVisibleTo(app) == quality
    
    # Lossless
    assert app.lossless_cb.isVisibleTo(app) == lossless
    
    # Misc.
    assert app.jxl_modular_cb.isVisibleTo(app) == jxl_modular
    assert app.jxl_modular_l.isVisibleTo(app) == jxl_modular
    assert app.reconstruct_jpg_cb.isVisibleTo(app) == reconstruct_jpg

    assert app.chroma_subsampling_l.isVisibleTo(app) == chroma_subsampling
    assert (app.chroma_subsampling_jpegli_cmb.isVisibleTo(app) == chroma_subsampling) or \
            (app.chroma_subsampling_avif_cmb.isVisibleTo(app) == chroma_subsampling) or \
            (app.chroma_subsampling_jpg_cmb.isVisibleTo(app) == chroma_subsampling)

    assert app.smallest_lossless_png_cb.isVisibleTo(app) == smallest_lossless
    assert app.smallest_lossless_webp_cb.isVisibleTo(app) == smallest_lossless
    assert app.smallest_lossless_jxl_cb.isVisibleTo(app) == smallest_lossless
    assert app.max_compression_cb.isVisibleTo(app) == smallest_lossless

def test_onFormatChange_lossless_glitch(app):
    """Tests if an option set in one format affects others."""
    app.lossless_cb.setChecked(True)
    assert not app.quality_sl.isEnabled()

    app.format_cmb.setCurrentIndex(app.format_cmb.findText("WebP"))
    assert app.quality_sl.isEnabled()

    app.format_cmb.setCurrentIndex(app.format_cmb.findText("JPEG XL"))
    
def test_onFormatChange_int_e_glitch(app):
    app.int_effort_cb.setChecked(True)
    assert not app.effort_sb.isEnabled()

    app.format_cmb.setCurrentIndex(app.format_cmb.findText("AVIF"))
    assert app.effort_sb.isEnabled()

    app.format_cmb.setCurrentIndex(app.format_cmb.findText("JPEG XL"))
    assert not app.effort_sb.isEnabled()

def test_jpeg_xl_effort_10(app):
    app.format_cmb.setCurrentIndex(app.format_cmb.findText("JPEG XL"))
    
    assert app.effort_sb.maximum() == 9
    app.setJxlEffort10Enabled(True)
    assert app.effort_sb.maximum() == 10

@pytest.mark.parametrize("format, min, max", [
    ("JPEG XL", 1, 9),
    ("AVIF", 0, 10),
])
def test_effort_ranges(app, format, min, max):
    app.format_cmb.setCurrentIndex(app.format_cmb.findText(format))
    
    assert app.effort_sb.minimum() == min
    assert app.effort_sb.maximum() == max