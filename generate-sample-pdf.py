#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from os import listdir
from os.path import dirname, join
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generate_pdf_from_template_with_text(render_text="Some Name",
                                         font_size=32,
                                         footer_text="Poznań, ",
                                         footer_size=12):
    template_dir = join(dirname(__file__), 'template')
    for template_name in listdir(template_dir):
        print(template_name)

        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        text_width = stringWidth(render_text, 'Arial', 32)
        existing_pdf = PdfFileReader(open(join(template_dir, template_name), "rb"))
        page = existing_pdf.getPage(0)

        packet = io.BytesIO()
        # create a new PDF with Reportlab
        can = canvas.Canvas(packet, pagesize=letter)
        # print(can.getAvailableFonts())
        can.setFont('Arial', font_size)
        can.setFontSize(font_size)
        can.drawString((float(page.mediaBox.width) - text_width) / 2, 280, render_text)
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
        outputStream = open(join("output", f"{template_name.split('.')[0]}_{render_text.replace(' ','_')}.pdf"), "wb")
        output.write(outputStream)
        outputStream.close()

if __name__ == '__main__':
    with open('names.txt', 'r', encoding='utf-8') as names_file:
        for name in names_file.read().split('\n'):
            generate_pdf_from_template_with_text(render_text=name)
