import unittest
import sys
import shutil
import hashlib
from pathlib import Path
import platform

from PySide6.QtGui import (
    QDropEvent,
)
from PySide6.QtWidgets import (
    QApplication,
)
from PySide6.QtTest import (
    QTest,
)
from PySide6.QtCore import (
    Qt,
    QMimeData,
    QUrl,
    QPoint
)
from PIL import Image, ImageDraw

from main import MainWindow
from data.constants import *

# CONFIG
SAMPLE_IMG_FOLDER = Path(".").resolve() / "sample_img"
TMP_IMG_FOLDER = Path(".").resolve() / "unit_tests_tmp"
app = QApplication(sys.argv)

# ---------------------------------------------------------------
#                           Tools
# ---------------------------------------------------------------

def scan_dir(path):
    items = set()   # No duplicates
    for i in Path(path).rglob("*"):
        if i.is_file():
            items.add(i.resolve())
    return list(items)  # So it can be accessed by an index

def rmtree(path):
    path = Path(path).resolve()
    if path.is_dir():
        shutil.rmtree(path)

def blake2(path):
    hasher = hashlib.blake2b()

    with open(path, "rb") as file:
        buff_size = 8192
        for buf in iter(lambda: file.read(buff_size), b""):
            hasher.update(buf)
    
    return hasher.hexdigest()

def sleep(ms):
    QTest.qWait(ms)

def cmb_set_text(cmb, text):
    idx = cmb.findText(text)
    if idx != -1:
        cmb.setCurrentIndex(idx)
    else:
        print(f"[Error - cmb_set_text()] Could not find \"{text}\"")
    
def test_dict(data):
    """Recursively verify dictionary's integrity"""
    for key, value in data.items():
        if isinstance(value, dict):
            if test_dict(value) is None:
                return False
        else:
            if value is None:
                return False
    
    return True

def create_sample_img():
    sample_img_path = SAMPLE_IMG_FOLDER / "sample_img.png"

    if sample_img_path.exists():
        return

    w, h = 1920, 1080
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)

    for i in range(h):
        r = int(32 + (241 - 32) * i / h)
        g = int(33 + (128 - 33) * i / h)
        b = int(36 + (0 - 36) * i / h)
        draw.line([(0, i), (w, i)], fill=(r, g, b))
    
    SAMPLE_IMG_FOLDER.mkdir(exist_ok=True)
    img.save(sample_img_path)

class Data:
    """Sample data and tmp folder management system."""
    
    def __init__(self, sample_img_folder, tmp_img_folder):
        self.sample_img_folder = sample_img_folder
        self.tmp_img_folder = tmp_img_folder

        self.cleanup()

    def cleanup(self):
        rmtree(self.tmp_img_folder)
    
    # Tmp (output) Directory
    def get_tmp_folder_path(self, path = None):
        if path == None:
            return self.tmp_img_folder
        else:
            return Path(self.tmp_img_folder) / path

    def get_tmp_folder_content(self, subfolder=None):
        if subfolder:
            return scan_dir(Path(self.tmp_img_folder) / subfolder)
        else:
            return scan_dir(self.tmp_img_folder)

    def make_tmp_subfolder(self, name):
        path = Path(self.tmp_img_folder) / name
        path.mkdir(parents=True)
        return path

    # Samples Directory
    def get_sample_img(self):
        return scan_dir(self.sample_img_folder)[0]

    def get_sample_imgs(self):
        return scan_dir(self.sample_img_folder)
    
    def get_sample_img_folder(self):
        return self.sample_img_folder

class Interact:
    """Translation layer between unit tests and the application."""
    def __init__(self, main_window):
        self.main_window = main_window
        self.root = self.main_window.input_tab.file_view.invisibleRootItem()

    def add_item(self, path):
        path = Path(path)
        self.main_window.input_tab._addItems(
            [
                (path, path.parent)
            ]
        )
        
    def add_items(self, paths):
        tmp = []
        for i in paths:
            path = Path(i)
            tmp.append(
                (
                    path,
                    path.parent,
                )
            )
        self.main_window.input_tab._addItems(tmp)

    def get_items(self):
        return [self.root.child(i).text(2) for i in range(self.root.childCount())]

    def get_item_count(self):
        return self.main_window.input_tab.file_view.invisibleRootItem().childCount()

    def clear_list(self):
        self.main_window.input_tab.clearInput()

    def set_custom_output(self, path):
        self.main_window.output_tab.wm.getWidget("choose_output_ct_rb").setChecked(True)
        path = str(path.resolve())
        self.main_window.output_tab.wm.getWidget("choose_output_ct_le").setText(path)
    
    def set_lossless(self, checked):
        self.main_window.output_tab.wm.getWidget("lossless_cb").setChecked(checked)

    def reset_to_default(self):
        self.main_window.output_tab.resetToDefault()
        self.main_window.modify_tab.resetToDefault()
        self.main_window.settings_tab.resetToDefault()
        self.main_window.output_tab.wm.getWidget("threads_sl").setValue(self.main_window.output_tab.MAX_THREAD_COUNT)   # To speed up testing

    def convert_preset(self, src, dst, format, lossless=False, effort=7, jpg_encoder="JPEGLI"):
        self.clear_list()
        self.set_format(format)
        self.set_custom_output(dst)
        self.add_item(src)
        self.set_lossless(lossless)
        self.set_effort(effort)
        if format == "JPEG":
            self.set_jpg_encoder(jpg_encoder)
        self.convert()

    def convert(self):
        self.main_window.convert()
        self.wait_for_done()

    def wait_for_done(self):
        while True:
            sleep(100)
            if self.main_window.items.getCompletedItemCount() == self.main_window.items.getItemCount():
                break

    def set_effort(self, effort):
        self.main_window.output_tab.effort_sb.setValue(effort)
    
    def set_duplicate_handling(self, mode):
        cmb_set_text(self.main_window.output_tab.duplicates_cmb, mode)
    
    def set_format(self, _format):
        cmb_set_text(self.main_window.output_tab.format_cmb, _format)

    def set_preserve_attributes(self, enabled):
        self.main_window.modify_tab.date_time_cb.setChecked(enabled)
    
    def set_jpg_encoder(self, encoder: str):
        cmb_set_text(self.main_window.settings_tab.jpg_encoder_cmb, encoder)

    def drag_and_drop(self, urls):
        mime_data = QMimeData()
        mime_data.setUrls([QUrl.fromLocalFile(url) for url in urls])

        drop_event = QDropEvent(QPoint(), Qt.CopyAction, mime_data, Qt.LeftButton, Qt.NoModifier)

        QTest.mousePress(self.main_window, Qt.LeftButton, pos=QPoint(), delay=100)
        self.main_window.dropEvent(drop_event)
        QTest.mouseRelease(self.main_window, Qt.LeftButton, pos=QPoint(), delay=100)
        QTest.qWait(100)
    
    def get_settings(self, tab):
        match tab:
            case "output_tab":
                return self.main_window.output_tab.getSettings()
            case "modify_tab":
                return self.main_window.modify_tab.getSettings()
            case "settings_tab":
                return self.main_window.settings_tab.getSettings()
    
    def set_metadata_mode(self, mode):
        cmb_set_text(self.main_window.modify_tab.metadata_cmb, mode)
    
    def set_downscaling_mode(self,
            mode,
            width=None,
            height=None,
            percent=None,
            shortest=None,
            longest=None,
            file_size=None,
        ):

        self.main_window.modify_tab.downscale_cb.setChecked(True)
        cmb_set_text(self.main_window.modify_tab.mode_cmb, mode)

        def set_value(widget, value):
            if value is not None:
                widget.setValue(value)
        
        set_value(self.main_window.modify_tab.pixel_w_sb, width)
        set_value(self.main_window.modify_tab.pixel_h_sb, height)
        set_value(self.main_window.modify_tab.percent_sb, percent)
        set_value(self.main_window.modify_tab.shortest_sb, shortest)
        set_value(self.main_window.modify_tab.longest_sb, longest)
        set_value(self.main_window.modify_tab.file_size_sb, file_size)
        
# ---------------------------------------------------------------
#                         Unit Tests
# ---------------------------------------------------------------

def windows_only(test_func):
    def wrapper(*args, **kwargs):
        if os.name != 'nt':
            raise unittest.SkipTest()
        return test_func(*args, **kwargs)
    return wrapper

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = Interact(MainWindow())
        self.data = Data(SAMPLE_IMG_FOLDER, TMP_IMG_FOLDER)
        self.app.reset_to_default()
        self.app.clear_list()
    
    def tearDown(self):
        self.data.cleanup()

    def test_dependencies(self):
        FILES = (
            ICON_SVG,
            LICENSE_PATH,
            LICENSE_3RD_PARTY_PATH,
            CJXL_PATH,
            DJXL_PATH,
            JXLINFO_PATH,
            IMAGE_MAGICK_PATH,
            AVIFENC_PATH,
            AVIFDEC_PATH,
            OXIPNG_PATH,
            EXIFTOOL_PATH,
        )

        for i in FILES:
            if platform.system() == "Linux" and i == EXIFTOOL_PATH:
                continue
            assert Path(i).is_file(), f"File not found ({i})"

    def test_clear_list(self):
        self.app.add_items(self.data.get_sample_imgs())
        assert self.app.get_item_count() > 0, "List shouldn't be empty"
        self.app.clear_list()
        assert self.app.get_item_count() == 0, "List should be empty"

    def test_drag_n_drop_files(self):
        self.app.drag_and_drop(self.data.get_sample_imgs())
        assert self.app.get_item_count() == len(self.data.get_sample_imgs())
    
    def test_drag_n_drop_folders(self):
        self.app.drag_and_drop([self.data.get_sample_img_folder()])
        assert self.app.get_item_count() == len(self.data.get_sample_imgs())

    def test_duplicate_detection(self):
        items = self.data.get_sample_imgs()
        self.app.add_items(items)
        self.app.add_items(items)
        assert self.app.get_item_count() == len(items)

    def test_jpeg_xl_lossy(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG XL")
        assert len(self.data.get_tmp_folder_content() ) > 0, "Converted image not found"
    
    def test_jpeg_xl_effort(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG XL", effort=7)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG XL", effort=9)

        converted = self.data.get_tmp_folder_content()
        assert blake2(converted[0]) != blake2(converted[1]), "Images should not be the same"

    def test_jpg_reconstruction(self):
        # Source -> JPG
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("jpg"), "JPEG")

        # JPG -> JXL
        self.app.convert_preset(self.data.get_tmp_folder_content("jpg")[0], self.data.make_tmp_subfolder("jxl"), "Lossless JPEG Recompression")

        # JXL -> JPG
        self.app.convert_preset(self.data.get_tmp_folder_content("jxl")[0], self.data.make_tmp_subfolder("reconstructed"), "JPEG Reconstruction")

        assert blake2(self.data.get_tmp_folder_content("jpg")[0]) == blake2(self.data.get_tmp_folder_content("reconstructed")[0]), "Hash mismatch for reconstructed JPG"

    def test_avif(self): 
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("avif"), "AVIF")
        assert Path(self.data.get_tmp_folder_content()[0]).suffix == ".avif", "AVIF file not found"
    
    def test_webp(self): 
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("webp"), "WebP")
        assert Path(self.data.get_tmp_folder_content()[0]).suffix == ".webp", "WebP file not found"
    
    def test_jpg(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("jpg"), "JPEG")
        assert Path(self.data.get_tmp_folder_content()[0]).suffix == ".jpg", "JPG file not found"

    def test_jpeg_xl_decode(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("jxl"), "JPEG XL")
        self.app.convert_preset(self.data.get_tmp_folder_content("jxl")[0], self.data.make_tmp_subfolder("jxl_decoded"), "PNG")
        assert len(self.data.get_tmp_folder_content("jxl_decoded")) > 0, "Decoded JPEG XL file not found"

    def test_avif_decode(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("avif"), "AVIF")
        self.app.convert_preset(self.data.get_tmp_folder_content("avif")[0], self.data.make_tmp_subfolder("avif_decoded"), "PNG")
        assert len(self.data.get_tmp_folder_content("avif_decoded")) > 0, "Decoded AVIF file not found"

    def test_webp_decode(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("webp"), "WebP")
        self.app.convert_preset(self.data.get_tmp_folder_content("webp")[0], self.data.make_tmp_subfolder("webp_decoded"), "PNG")
        assert len(self.data.get_tmp_folder_content("webp_decoded")) > 0, "Decoded WebP file not found"

    def test_decode_jpg(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("jpg"), "JPEG")
        self.app.convert_preset(self.data.get_tmp_folder_content("jpg")[0], self.data.make_tmp_subfolder("jpg_decoded"), "PNG")
        assert len(self.data.get_tmp_folder_content("jpg_decoded")) > 0, "Decoded JPG file not found"
    
    def test_proxy(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("jpg"), "JPEG")
        assert Path(self.data.get_tmp_folder_content("jpg")[0]).suffix == ".jpg", "JPG file not found"

        self.app.convert_preset(self.data.get_tmp_folder_content("jpg")[0], self.data.make_tmp_subfolder("webp"), "WebP")
        assert Path(self.data.get_tmp_folder_content("webp")[0]).suffix == ".webp", "WebP file not found"

        self.app.convert_preset(self.data.get_tmp_folder_content("webp")[0], self.data.make_tmp_subfolder("jxl"), "JPEG XL")
        assert Path(self.data.get_tmp_folder_content("jxl")[0]).suffix == ".jxl", "JPEG XL file not found"

        self.app.convert_preset(self.data.get_tmp_folder_content("jxl")[0], self.data.make_tmp_subfolder("avif"), "AVIF")
        assert Path(self.data.get_tmp_folder_content("avif")[0]).suffix == ".avif", "AVIF file not found"

    def test_smallest_lossless(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "Smallest Lossless")
        assert len(self.data.get_tmp_folder_content()) > 0, "Smallest Lossless did not generate any files"
    
    def test_rename(self):
        self.app.set_duplicate_handling("Rename")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        assert len(self.data.get_tmp_folder_content()) == 2, "File amount mismatch"

    def test_replace(self):
        self.app.set_duplicate_handling("Replace")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        assert len(self.data.get_tmp_folder_content()) == 1, "File amount mismatch"

    def test_skip(self):
        self.app.set_duplicate_handling("Skip")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        assert len(self.data.get_tmp_folder_content()) == 1, "File amount mismatch"

    def test_get_settings(self):
        assert test_dict(self.app.get_settings("output_tab")), "output_tab.getSettings contains None"
        assert test_dict(self.app.get_settings("modify_tab")), "modify_tab.getSettings contains None"
        assert test_dict(self.app.get_settings("settings_tab")), "settings.getSettings contains None"

    def test_preserve_attributes(self):
        self.app.set_preserve_attributes(True)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.set_preserve_attributes(False)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")

        # If modification times are more than 15 sec apart
        files = self.data.get_tmp_folder_content()
        assert abs(files[0].stat().st_mtime - files[1].stat().st_mtime) > 15, "Range too narrow"

    def test_metadata_exiftool(self):
        self.app.set_metadata_mode("ExifTool - Preserve")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.set_metadata_mode("ExifTool - Wipe")
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")

        files = self.data.get_tmp_folder_content()
        assert files[0].stat().st_size != files[1].stat().st_size, "No change detected" # This is expected to fail if your Windows username contains Unicode specific characters. See core/metadata.py for more info.

    def test_downscaling_resolution(self):
        self.app.set_downscaling_mode("Resolution", width = 100, height = 2000)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.set_downscaling_mode("Resolution", width = 2000, height = 100)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")

        converted = self.data.get_tmp_folder_content()
        assert converted[0].stat().st_size != converted[1].stat().st_size, "No change detected"

    def test_downscaling_percent(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.set_downscaling_mode("Percent", percent=50)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")

        converted = self.data.get_tmp_folder_content()
        assert converted[0].stat().st_size != converted[1].stat().st_size, "No change detected"
    
    def test_downscaling_shortest(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.set_downscaling_mode("Shortest Side", shortest=1)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")

        converted = self.data.get_tmp_folder_content()
        assert converted[0].stat().st_size != converted[1].stat().st_size, "No change detected"

    def test_downscaling_longest(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")
        self.app.set_downscaling_mode("Longest Side", longest=1)
        self.app.convert_preset(self.data.get_sample_img(), self.data.get_tmp_folder_path(), "JPEG")

        converted = self.data.get_tmp_folder_content()
        assert converted[0].stat().st_size != converted[1].stat().st_size, "No change detected"
    
    # POSIX is fine
    @windows_only
    def test_jxl_utf8_support(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("漢字0"), "JPEG XL")
        converted = self.data.get_tmp_folder_content()
        assert "jxl" == str(converted[0])[-3:]

        self.app.convert_preset(converted[0], self.data.make_tmp_subfolder("漢字1"), "PNG")
        assert len(self.data.get_tmp_folder_content()) == 2

    @windows_only
    def test_avif_utf8_support(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("漢字0"), "AVIF")
        converted = self.data.get_tmp_folder_content()
        assert "avif" == str(converted[0])[-4:]

        self.app.convert_preset(converted[0], self.data.make_tmp_subfolder("漢字1"), "PNG")
        assert len(self.data.get_tmp_folder_content()) == 2

    @windows_only
    def test_jpegli_utf8_support(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("漢字0"), "JPEG", jpg_encoder="JPEGLI")
        converted = self.data.get_tmp_folder_content()
        assert "jpg" == str(converted[0])[-3:]

        self.app.convert_preset(converted[0], self.data.make_tmp_subfolder("漢字1"), "PNG")
        assert len(self.data.get_tmp_folder_content()) == 2

    @windows_only
    def test_imagemagick_utf8_support(self):
        self.app.convert_preset(self.data.get_sample_img(), self.data.make_tmp_subfolder("漢字0"), "WebP")
        converted = self.data.get_tmp_folder_content()
        assert "webp" == str(converted[0])[-4:]

        self.app.convert_preset(converted[0], self.data.make_tmp_subfolder("漢字1"), "PNG")
        assert len(self.data.get_tmp_folder_content()) == 2

if __name__ == "__main__":
    create_sample_img()
    unittest.main(failfast=True)