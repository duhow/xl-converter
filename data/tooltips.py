TOOLTIPS = {
    # Output tab
    "duplicates": "What to do when an output image of the same name already exists.",
    "threads": "How many CPU threads to use for conversion.\n\nHigher means faster, but leaves less resources for other processes.\n\nLeave at least one unused or more if you're actively using your computer.",
    "output_src": "Save the resulting image next to the one you are converting from.",
    "output_ct": """Save the resulting image in the specified location. There are 2 types of paths:\n\n1. Absolute path (e.g. C:/Images/Converted)\n\n2. Relative path (e.g. Converted). Choosing it will save output to a folder located next to the source image.""",
    "keep_dir_struct": "Preserves folder hierarchy when saving images.",
    "delete_original": "Delete the input image after conversion.",
    "clear_after_conv": "Clear the file list (in the input tab) after conversion.",
    "format": "Which format are you converting to.\n\nHow should the image be processed.",
    "jxl_modular": "Enables lossy modular. It can increase quality and/or lower file size. \n\nEnabled - best for images with sharp edges and flat areas, like documents, digital art, or screenshots.\n\nDisabled - best for photos.",
    "jxl_png_fallback": "Image will be decoded to PNG if reconstruction data is not found.",
    "lossless": "Enables lossless compression.\n\nPixel data will stay the same if given bit depth is supported.",
    "lossless_jpeg_xl": "Enables lossless compression.\n\nPixel data will stay the same if given bit depth is supported.\n\nIt does not perform Lossless JPEG Recompression by default.",
    "int_effort": "Prioritizes smaller file size.",
    "effort": "Higher means better quality and/or smaller file size but slower.\n\nLossy: higher values result in higher quality. File size may end up larger, especially for non-photographic images.\n\nLossless: higher values always result in lower file size.\n\nLossy (Modular): higher values result in better quality and smaller file size but only for non-photographic images.\n\nTypical values: 7 or 9",
    "effort_jpeg_recomp": "Higher values always result in lower file size after recompression.\n\nTypical values: 7 or 9",
    "speed": "Lower is better quality but slower." ,
    "method": "Higher means better quality and/or smaller file size.\n\nLossless: higher values result in lower file size.\n\nLossy: higher value result in lower file size and typically higher quality. The latter can be subjective.\n\nTypical values: 4 - 6",
    "chroma_subsampling_jpeg": "Controls color compression. Lower number means less color information and smaller file size.\n\nDefault - matches the input or 4:4:4\n\n4:4:4 - full color, the highest quality and file size\n\n4:2:2 - less color (small visual difference) and significant space-saving\n\n4:2:0 - colors may appear washed out",
    "chroma_subsampling_avif": "Controls color compression. Lower number means less color information and smaller file size.\n\nDefault - matches the input or 4:4:4\n\n4:4:4 - full color, the highest quality and file size\n\n4:2:2 - less color (small visual difference) and significant space-saving\n\n4:2:0 - colors may appear washed out\n\n4:0:0 - grayscale",
    "quality_jpeg_xl": "Higher values result in higher quality and higher file size.\n\n90 - visually lossless\n\n80 - high quality and reasonable file size\n\n70 - medium-high quality and small file size\n\n60 - space-saving, noticeable blurriness",
    "quality_avif": "Higher values result in higher quality and higher file size.\n\n90 - visually lossless\n\n80 - high quality and file size\n\n70 - good balance between quality and file size\n\n60 - space-saving",
    "quality_webp": "Higher values result in higher quality and higher file size.\n\n90 - high quality and large file size\n\n80 - reasonable quality and file size\n\n60 - looks fine only from far away",
    "quality_jpeg": "Higher values result in higher quality and higher file size.\n\n95 - high quality and very large file size\n\n90 - reasonably high quality and large file size\n\n80 - reasonable quality and file size\n\n60 - looks fine only from far away",
    "smallest_lossless_png": "Uses OxiPNG.\n\nSupported bit depth: 16",
    "smallest_lossless_webp": "Supported bit depth: 8",
    "smallest_lossless_jpeg_xl": "Supported bit depth: 16",
    "smallest_lossless_max_comp": "Transcoding will be slower but may result in lower file size.",

    # Modify tab
    "date_time": "Preserves date and time.",
    "date_time_linux": "Preserves date and time.\n\nOn Linux, it also preserves permission bits and extended attributes.",
    "metadata": "Controls how metadata is handled.\n\nEncoder modes are faster and recommended. ExifTool is more thorough but more error-prone.\n\nEncoder - Wipe - wipes metadata. Works well for encoding everything except PNG, where it depends on the input format.\n\nEncoder - Preserve - preserves metadata. Works on common input formats, may not work for less popular ones.\n\nExifTool - Wipe - deletes all metadata except that which affects the final image.\n\nExifTool - Preserve - preserves all metadata.\n\nExifTool - Unsafe Wipe - deletes every last bit of metadata, including color profile. It can potentially alter the final image, but is the most effective.\n\nExifTool - Custom - empty. It allows you to specify custom behavior (in the settings).\n\nView and edit ExifTool commands in the settings (Settings -> Advanced -> ExifTool Arguments).",
    "downscaling": "Scales down the resolution of your image.",
    "downscaling_file_size": "Scales image to approximated file size in kibibytes.\n\nIt is about 4 times slower than regular conversion. Its accuracy varies.\n\nYou can preserve higher resolution by decreasing the quality (output tab). Use other modes whenever possible\n\nThe algorithm uses linear regression to predict image scale.",
    "downscaling_percent": "Scales to that percentage.\n\nExample: 80% will result in both width and height being 80% of the original resolution.",

    # Settings tab
    "disable_delete_startup": "Disables \"delete original\" (output tab) when you launch the application.",
    "disable_downscaling_startup": "Disables \"downscaling\" (modify tab) when you launch the application.",
    "dark_theme": "The intended look of XL Converter.",
    "quality_prec_snap": "Enabled - snaps to individual values.\n\nDisabled - snaps to intervals of every 5 points.",
    "sorting": "Disables file list sorting (input tab), has no impact on performance.",
    "play_sound_on_finish": "Plays a sound when conversion finishes.",
    "jxl_lossless_jpeg": "Enabled - the program will use \"Lossless JPEG Recompression\" instead of regular lossless compression when converting JPEG to JPEG XL.\n\nThis saves a lot of space but prevents metadata from being stripped. It affects the following formats:\n\n  - JPEG XL with \"Lossless\" enabled.\n\n  - Smallest Lossless (JPEG XL).\n\nDisabled - JPEG will be transcoded the same as any other file. That means a huge file size, but metadata can be stripped.",
    "jpeg_encoder": "JPEGLI - The new state of the art in JPEG encoding. Fast and high quality.\n\nlibjpeg - the original JPEG encoder. Well-tested, stable, and great at preserving noise. Use it when JPEGLI cannot convert a particular image.",
    "progressive_jpegli": "Enabled - generated JPEGs will be compatible with very old devices, but their file size will increase.\n\nDisabled - generated JPEGs will smaller and load faster.",
    "keep_if_larger": "Prevents \"Delete Original\" and \"Replace\" options (output tab) from deleting the original image if the result is larger",
    "copy_if_larger": "Copies the original image to the output folder when the result is larger.",
    "enable_jxl_effort_10": "Raises Effort limit from 9 to 10. Effort 10 is very slow but can produce smaller files in lossless.",
    "resample": "Enables resampling mode selection in the modify tab.",
    "no_exceptions": "The pop-up displaying exceptions encountered during conversion will no longer appear.",
    "exiftool_args": "Arguments used for handling metadata, correspond to the options is the modify tab.\n\nSupported variables:\n\n$src - source image path.\n\n$dst - destination image path.\n\nRemember to add \"-overwrite_original\" to avoid leftover files.",
    "encoder_args": "Additional arguments for the encoders.\n\nMake sure all arguments you add are valid; otherwise, the encoder will stop working.",
}