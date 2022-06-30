#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Module to generate a PDF file from a template PDF file with a text and footer inserted.
"""
import io
from os import listdir
from os.path import dirname, join
from datetime import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_pdf_from_template_with_text(pdf_template_path='./template/template.pdf',
                                         text_to_insert="Some Name",
                                         text_vertical_position=280,
                                         output_pdf_path='./output/output.pdf',
                                         font_size=32,
                                         add_footer=False,
                                         add_date_to_footer=False,
                                         footer_vertical_position=15,
                                         footer_horizontal_alignment='exact',
                                         footer_horizontal_position_value=280,
                                         footer_text="Poznań",
                                         footer_font_size=12,
                                         footer_date=datetime.now().strftime("%Y.%m.%d")):
    """
    Generates a PDF file from a template PDF file with a text inserted.
    :param pdf_template_path: path to the template PDF file
    :param text_to_insert: text to insert into the PDF file
    :param output_pdf_path: path to the output PDF file
    :param font_size: font size of the text to insert
    :param add_footer: boolean flag to add a footer to the PDF file
    :param add_date_to_footer: boolean flag to add a date to the footer
    :param footer_vertical_position: vertical position of the footer
    :param footer_horizontal_alignment: horizontal position of the footer,
        allowed values: 'left', 'center', 'right', 'exact'
    :param footer_horizontal_position_value: horizontal position
        of the footer to be used when footer_horizontal_alignment is 'exact'
    :param footer_text: text to insert into the footer
    :param footer_font_size: font size of the text to insert into the footer
    :param footer_date: date to insert into the footer
    :return:
    """
    valid = {'left', 'center', 'right', 'exact'}
    if footer_horizontal_alignment not in valid:
        raise ValueError(f"footer_horizontal_position must be one of ({valid}).")

    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    text_width = stringWidth(text_to_insert, 'Arial', font_size)

    # read your existing PDF
    existing_pdf = PdfFileReader(open(pdf_template_path, "rb"))
    page = existing_pdf.getPage(0)

    # create a new PDF with overlay text with Reportlab
    overlay_packet = io.BytesIO()
    overlay_canvas = canvas.Canvas(overlay_packet, pagesize=landscape(A4))
    # print(can.getAvailableFonts())
    overlay_canvas.setFont('Arial', font_size)
    overlay_canvas.setFontSize(font_size)
    overlay_canvas.drawString((float(page.mediaBox.width) - text_width) / 2,
                              text_vertical_position,
                              text_to_insert)
    overlay_canvas.save()
    #move to the beginning of the StringIO buffer
    overlay_packet.seek(0)
    overlay_pdf = PdfFileReader(overlay_packet)

    if add_footer:
        if add_date_to_footer:
            footer_text = footer_text + ", " + footer_date
        footer_text_width = stringWidth(footer_text, 'Arial', footer_font_size)
        # create a new PDF with footer text with Reportlab
        footer_packet = io.BytesIO()
        footer_canvas = canvas.Canvas(footer_packet, pagesize=landscape(A4))
        # print(can.getAvailableFonts())
        footer_canvas.setFont('Arial', footer_font_size)
        footer_canvas.setFontSize(footer_font_size)
        if footer_horizontal_alignment == 'left':
            footer_horizontal_position_value = 25
        elif footer_horizontal_alignment == 'center':
            footer_horizontal_position_value = (float(page.mediaBox.width) - footer_text_width) / 2
        elif footer_horizontal_alignment == 'right':
            footer_horizontal_position_value = float(page.mediaBox.width) - footer_text_width - 25
        footer_canvas.drawString(footer_horizontal_position_value,
                                 footer_vertical_position,
                                 footer_text)
        footer_canvas.save()
        #move to the beginning of the StringIO buffer
        footer_packet.seek(0)
        footer_pdf = PdfFileReader(footer_packet)


    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page.mergePage(overlay_pdf.getPage(0))
    if add_footer:
        # add the footer pdf on the existing page
        page.mergePage(footer_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    output_stream = open(output_pdf_path, "wb")
    output.write(output_stream)
    output_stream.close()

if __name__ == '__main__':
    template_dir = join(dirname(__file__), 'template')

    with open('names.txt', 'r', encoding='utf-8') as names_file:
        for name in names_file.read().split('\n'):
            for template_name in listdir(template_dir):
                generate_pdf_from_template_with_text(
                    pdf_template_path=join(template_dir, template_name),
                    text_to_insert=name,
                    text_vertical_position=275,
                    output_pdf_path=join("output",
                                        f"{template_name.split('.')[0]}_{name}.pdf".replace(' ','_')
                                        ),
                    font_size=32,
                    footer_horizontal_alignment='exact',
                    footer_horizontal_position_value=550,
                    footer_vertical_position=155,
                    add_footer=True,
                    add_date_to_footer=True,
                    footer_text="Poznań",
                    footer_font_size=12,
                    footer_date=datetime.now().strftime("%Y.%m.%d")
                )
