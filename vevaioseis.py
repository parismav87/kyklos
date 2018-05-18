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
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

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
            alignment=TA_CENTER,
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
            alignment=TA_CENTER,
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
    def createPDF(self, firstname, lastname, index, startfrom, webinarTitle, webinarSubtitle, date):
        """
        Create a PDF based on the XML data
        """
        if not os.path.exists("vevaioseis"):
            os.makedirs("vevaioseis", 0755)
        pdfFile =  "vevaioseis/" +lastname + ".pdf"
        self.canvas = canvas.Canvas(pdfFile, pagesize=letter)
        width, self.height = letter
        styles = self.stylesheet()


        
        title = """<font face="Georgia" size="16">
        ΒΕΒΑΙΩΣΗ ΠΑΡΑΚΟΛΟΥΘΗΣΗΣ ΣΕΜΙΝΑΡΙΟΥ</font>
        """

        


        tax1 = """
        <font face="Georgia" size="10">
        Εργαστήριο Λογοθεραπείας και<br/>
        <br/>Εικαστικών "Κύκλος"<br/>
        <br/>Αναξιμάνδρου 57, Θεσσαλονίκη<br/>
        <br/><br/>
        </font>
        """ 

        main = """
        <font face="Georgia" size="13">
        Βεβαιώνεται ότι ο/η %s %s <br/>
        <br/>παρακολούθησε το διαδικτυακό σεμινάριο με τίτλο<br/>
        <br/>"%s<br/>
        <br/>%s"<br/>
        <br/>δίωρης διάρκειας που διοργάνωσε το εργαστήριο Λογοθεραπείας και Εικαστικών <br/>
        <br/>"Κύκλος" στις %s.<br/>
        </font>
        """ %(firstname, lastname, webinarTitle, webinarSubtitle, date)


        botLeft1 = """
        <font face="Georgia" size="10">
        Η υπεύθυνη του Εργαστηρίου<br/>
        <br/>Λογοθεραπείας και Εικαστικών<br/>
        <br/>"Κύκλος"<br/>
        <br/><br/>
        </font>
        """ 

        botLeft2 = """
        <font face="Georgia" size="10">
        Theodora Blom<br/>
        <br/><br/>
        </font>
        """ 

        botRight1 = """
        <font face="Georgia" size="10">
        O/H εισηγητής<br/>
        <br/><br/>
        </font>
        """ 

        botRight2 = """
        <font face="Georgia" size="10">
        Δημοσθένης Ψηφίδης<br/>
        <br/><br/>
        </font>
        """ 


        ##########LEFT SIDE TOP###########        
        p = Paragraph(title, styles["title"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 400, 50)
        p.drawOn(self.canvas, *self.coord(38, 70, mm))


        ############RIGHT SIDE TOP##########

        p = Paragraph(tax1, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 500, 50)
        p.drawOn(self.canvas, *self.coord(77, 50, mm))

        p = Paragraph(main, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 500, 50)
        p.drawOn(self.canvas, *self.coord(18, 140, mm))

        p = Paragraph(botLeft1, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 200, 50)
        p.drawOn(self.canvas, *self.coord(18, 230, mm))

        p = Paragraph(botLeft2, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 200, 50)
        p.drawOn(self.canvas, *self.coord(18, 270, mm))

        p = Paragraph(botRight1, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 200, 50)
        p.drawOn(self.canvas, *self.coord(128, 220, mm))

        p = Paragraph(botRight2, styles["default2"])
        # p.wrapOn(self.canvas, width, self.height)
        p.wrapOn(self.canvas, 200, 50)
        p.drawOn(self.canvas, *self.coord(128, 270, mm))

        logo = "logo.png"
        im = Image(logo, 1.3*inch, 1.3*inch)
        im.drawOn(self.canvas, *self.coord(27, 50, mm))

        logo = "sigDore.png"
        im = Image(logo, 1*inch, 1*inch)
        im.drawOn(self.canvas, *self.coord(40, 250, mm))

        logo = "sig.png"
        im = Image(logo, 1*inch, 1*inch)
        im.drawOn(self.canvas, *self.coord(153, 250, mm))

        

    #----------------------------------------------------------------------
    def getCSV(self):
        """
        Open the XML document and return an lxml XML document
        """
        
        with open(self.csvFile) as f:
            csvf = csv.reader(f, delimiter=',')
            realIndex = 0
            for index, item in enumerate(csvf):
                
                if index != 0 and not (item[4] == "ΟΧΙ" or item[4] == "OXI") :
                    # print item[0]
                    realIndex +=1
                    webinarTitle = "Αγκυλογλωσσία (βραχύς χαλινός γλώσσας): Η σημασία της"
                    webinarSubtitle = "έγκαιρης διάγνωσης και αντιμετώπισής της πριν τη λογοθεραπευτική παρέμβαση"
                    date= "6 Μαΐου 2018"
                    self.createPDF(item[0], item[1], realIndex, 1, webinarTitle, webinarSubtitle, date)
                    self.savePDF();
    
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















