import platform

from data.constants import (
    EXIFTOOL_PATH,
    IMAGE_MAGICK_PATH,
    CJXL_PATH,
    AVIFENC_PATH,
    OXIPNG_PATH
)
from core.process import runProcess, runProcessOutput

class Data:
    exiftool_available = None   # None - unchecked; False - not available; True - available;

def copyMetadata(src, dst):
    """Copy all metadata from one file onto another."""
    _runExifTool('-tagsfromfile', src, '-overwrite_original', dst)

def deleteMetadata(dst):
    """Delete all metadata except color profile from a file."""
    _runExifTool("-all=", "-tagsFromFile", "@", "--icc_profile:all", "--ColorSpace:all", "-overwrite_original", dst)

def deleteMetadataUnsafe(dst):
    """Delete every last bit of metadata, even color profile. May mess up an image. Potentially destructive."""
    _runExifTool("-all=", "-overwrite_original", dst)

def runExifTool(src, dst, mode):
    """ExifTool wrapper."""
    match mode:
        case "ExifTool - Wipe":
            deleteMetadata(dst)
        case "ExifTool - Preserve":
            copyMetadata(src, dst)
        case "ExifTool - Unsafe Wipe":
            deleteMetadataUnsafe(dst)

def isExifToolAvailable() -> bool | None:
    """Checks if ExifTool is available. Unix-only."""
    if Data.exiftool_available is not None:
        return Data.exiftool_available

    match platform.system():
        case "Linux":
            Data.exiftool_available = not "not found" in runProcessOutput("bash", "-c", "type exiftool")[0]
        case _:
            Data.exiftool_available = True
   
    return Data.exiftool_available

def _runExifTool(*args):
    """For internal use only."""
    if platform.system() == "Windows":
        runProcess(EXIFTOOL_PATH, *args)
    elif platform.system() == "Linux":
        runProcess("exiftool", *args)
        # ExifTool is no longer included due to a bug in its handling of JPEG XL.
        # If you try to process JPEG XL from Worker, you get:
        # (stderr): Warning: Install IO::Uncompress::Brotli to decode Brotli-compressed metadata
        # To reproduce it, checkout `v1.0.1` tag and copy the binaries over from the official release.
        
def getArgs(encoder, mode, jpg_to_jxl_lossless=False) -> list:
    """Return metadata arguments for the specified encoder.

    Example Usage:
        args = []
        args.extend(getArgs(encoder, mode))
    """
    match mode:
        case "Encoder - Wipe":
            if encoder == CJXL_PATH:
                if not jpg_to_jxl_lossless:
                    return ["-x strip=exif", "-x strip=xmp", "-x strip=jumbf"]    
                else:
                    return []
            elif encoder == IMAGE_MAGICK_PATH:
                return ["-strip"]
            elif encoder == AVIFENC_PATH:
                return  ["--ignore-exif", "--ignore-xmp"]
            elif encoder == OXIPNG_PATH:
                return ["--strip safe"]
            else:
                return []   # DJXL, CJPEGLI, AVIFDEC - unavailable or undocumented
        case "Encoder - Preserve":
            return []   # Encoders preserve metadata by default
        case _:
            return []