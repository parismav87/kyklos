# -*- coding: UTF-8 -*-
from decimal import Decimal
from lxml import etree, objectify
import csv
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
# from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle


pdfmetrics.registerFont(TTFont('Georgia', 'Georgia.ttf'))


########################################################################
class PDFOrder(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, csvFile):
        """Constructor"""
        self.csvFile = csvFile
        
        # self.csvObj = self.getCSV()
        # print(self.csvObj)
        
    #----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        # http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height -  y * unit
        return x, y  
        

    def stylesheet(self):
        styles= {
            'default': ParagraphStyle(
            'default',
            fontName='Georgia',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Georgia',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= colors.black,
            backColor="rgba(5, 168, 170, 0.5)",
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 5,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
            ),
        }

        styles['default2'] = ParagraphStyle(
            'default2',
            parent=None,
            fontName='Georgia',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Georgia',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= colors.black,
            backColor="rgba(11, 122, 117, 0.5)",
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 5,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,        )

        styles['title'] = ParagraphStyle(
            'title',
            parent=None,
            fontName='Georgia',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Georgia',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= colors.black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 3,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,        )

        styles['alert'] = ParagraphStyle(
            'alert',
            parent=styles['default'],
            leading=14,
            backColor=colors.yellow,
            borderColor=colors.black,
            borderWidth=1,
            borderPadding=5,
            borderRadius=2,
            spaceBefore=10,
            spaceAfter=10,
        )
        return styles


    #---------------------------------------------------------------------
    def createPDF(self, firstname, lastname, index, startfrom, date):
        """
        Create a PDF based on the XML data
        """
        if not os.path.exists("apodeikseis"):
            os.makedirs("apodeikseis", 0755)
        pdfFile =  "apodeikseis/" +lastname + ".pdf"
        self.canvas = canvas.Canvas(pdfFile, pagesize=letter)
        width, self.height = letter
        styles = self.stylesheet()
        
        title = """<font face="Georgia" size="16">
        ΘΕΟΔΩΡΑ ΜΠΛΟΜ</font>
        """

        address1 = """
        <font face="Georgia" size="10">
        Αναξιμάνδρου 57<br/>
        <br/>ΑΦΜ: 042961034<br/>
        <br/>info@kyklostherapy.gr<br/>
        <br/>Τηλ: 2310320619<br/>
        </font>
        """

        address2 = """
        <font face="Georgia" size="10">
        TΚ: 54250 Θεσσαλονίκη<br/>
        <br/>ΔΟΥ: Ζ' Θεσσαλονίκης<br/>
        <br/>www.kyklostherapy.gr<br/>
        <br/>Fax: 2310320619<br/>
        </font>
        """


        taxTitle = """<font face="Georgia" size="16">
        ΑΠΟΔΕΙΞΗ ΠΑΡΟΧΗΣ ΥΠΗΡΕΣΙΩΝ</font>
        """

        tax1 = """
        <font face="Georgia" size="10"><br/>
        <br/>Αριθμός Απόδειξης:<br/>
        <br/>Ημερομηνία Απόδειξης:<br/>
        <br/>Τρόπος Πληρωμής:
        </font>
        """

        correctNum = startfrom-1+index
        tax2 = """
        <font face="Georgia" size="10"><br/>
        <br/>%d<br/>
        <br/>%s<br/>
        <br/>Μετρητοίς<br/>
        </font>
        """ %(correctNum, date)
        #int(startfrom)-1+int(index)
        customer1 = """
        <font face="Georgia" size="10">
        Όνομα Πελάτη:
        </font>
        """

        customer2 = """
        <font face="Georgia" size="10">
        %s %s
        </font>
        """ %(firstname, lastname)


        ##########LEFT SIDE TOP###########        
        p = Paragraph(title, styles["title"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 200, 50)
        p.drawOn(self.canvas, *self.coord(18, 20, mm))

        p = Paragraph(address1, styles["default"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 114.8, 50)
        p.drawOn(self.canvas, *self.coord(18, 63, mm))

        p = Paragraph(address2, styles["default"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 199.8, 50)
        p.drawOn(self.canvas, *self.coord(62, 63, mm))

        ############RIGHT SIDE TOP##########

        p = Paragraph(taxTitle, styles["title"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 500, 50)
        p.drawOn(self.canvas, *self.coord(107, 20, mm))

        p = Paragraph(tax1, styles["default"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 114.8, 50)
        p.drawOn(self.canvas, *self.coord(136, 63, mm))

        p = Paragraph(tax2, styles["default"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 60, 50)
        p.drawOn(self.canvas, *self.coord(180, 63, mm))

        ###########CUSTOMER LEFT###############
        p = Paragraph(customer1, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 114.8, 50)
        p.drawOn(self.canvas, *self.coord(18, 70.8, mm))

        ###########CUSTOMER RIGHT###############
        p = Paragraph(customer2, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 394.7, 50)
        p.drawOn(self.canvas, *self.coord(62, 70.8 , mm))


                
        data = []
        data.append(["Ποσότητα", "Περιγραφή", "Τιμή Μονάδας Ευρώ", "Μερικό Σύνολο Ευρώ"])
        grand_total = 30
        row = []
        row.append("1")
        row.append('Webinar: "Αγκυλογλωσσία (βραχύς \nχαλινός γλώσσας): \nΗ σημασία της έγκαιρης διάγνωσης και \nαντιμετώπισής της πριν απο τη \nλογοθεραπευτική παρέμβαση."')
        row.append("30")
        row.append("30")
        data.append(row)
        data.append(["", "", "Σύνολο Ευρώ:", grand_total])
        t = Table(data, 1.835 * inch)
        t.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('FONTNAME', (0,0), (-1,-1), 'Georgia'),
            ('FONTSIZE', (0,0), (-1,-1), 7),
        ]))
        t.wrapOn(self.canvas, width, self.height)
        t.drawOn(self.canvas, *self.coord(16.4, 110.2, mm))
        

    #----------------------------------------------------------------------
    def getCSV(self):
        """
        Open the XML document and return an lxml XML document
        """
        with open(self.csvFile) as f:
            csvf = csv.reader(f, delimiter=',')
            realIndex = 0
            for index, item in enumerate(csvf):
                if(index != 0 and item[4] == "OK"):
                    # print item[0]
                    realIndex +=1
                    date = "16/5/2018"
                    self.createPDF(item[0], item[1], realIndex, startfrom=25, date=date)
                    self.savePDF()
    
    #----------------------------------------------------------------------
    def savePDF(self):
        """
        Save the PDF to disk
        """
        self.canvas.save()
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    csv_file = "file.csv"    
    doc = PDFOrder(csv_file)
    csvObject = doc.getCSV()















