#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
from os import listdir
from os.path import dirname, join
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime


def generate_pdf_from_template_with_text(pdf_template_path='./template/template.pdf',
                                         text_to_insert="Some Name",
                                         output_pdf_path='./output/output.pdf',
                                         font_size=32,
                                         add_footer=True,
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
    :param footer_text: text to insert into the footer
    :param footer_font_size: font size of the text to insert into the footer
    :param footer_date: date to insert into the footer
    :return:
    """
    
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    text_width = stringWidth(text_to_insert, 'Arial', 32)
    existing_pdf = PdfFileReader(open(pdf_template_path, "rb"))
    page = existing_pdf.getPage(0)

    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    # print(can.getAvailableFonts())
    can.setFont('Arial', font_size)
    can.setFontSize(font_size)
    can.drawString((float(page.mediaBox.width) - text_width) / 2, 280, text_to_insert)
    can.save()


    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF

    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page.mergePage(new_pdf.getPage(0))
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
                    output_pdf_path=join("output", f"{template_name.split('.')[0]}_{name}.pdf".replace(' ','_')),
                    font_size=32,
                    add_footer=True,
                    footer_text="Poznań",
                    footer_font_size=12,
                    footer_date=datetime.now().strftime("%Y.%m.%d")
                )
