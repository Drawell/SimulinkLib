import cairo


class TextSizeHelper:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 0, 0)
    cr = cairo.Context(surf)
    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    @staticmethod
    def get_text_size(text: str, font_size : float):
        TextSizeHelper.cr.set_font_size(font_size)
        return TextSizeHelper.cr.text_extents(text)
