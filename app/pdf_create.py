from fpdf import FPDF
 
class RFI_PDF(FPDF):
    def header(self):
        # Logo
        #self.image('/static/logobw3-r.jpg', 175, 12.5, 25)
        # Arial bold 15
        self.set_font('Arial', 'B', 18)
        
        # Title
        self.ln(6)
        self.cell(80)
        self.cell(30, 10, 'RFI RESPONSE', 0, 0, 'C')

 
    # Page footer
    def footer(self):
        # Position at 0.75 cm from bottom
        self.set_y(-7.5)
        # Arial italic 6
        self.set_font('Arial', 'I', 6)
        # Footer Text
        self.cell(0, 10, 'Generated automatically by RFI Web App', 0, 0, 'L')

    def borders(self):
        self.set_line_width(2)
        self.set_fill_color(255,255,255)
        self.rect(10,10,195,260)
        self.set_line_width(0.5)
        self.rect(22.5,90,175,150)

        
    def headers(self, rfi_number, title, date_received, date_response, dwg_refer,spec_refer,response,reviewer, unit_name, project_title):
        
        self.set_y(25)
        self.cell(80)
        self.set_font('Arial', '', 12)
        self.cell(30, 10, unit_name , 0, 0, 'C')
        self.ln(6)
        self.cell(80)
        self.cell(30, 10, project_title, 0, 0, 'C')

        self.set_y(40)
        self.cell(12.5)
        self.set_font('Arial', 'B', 12)
        self.cell(40,10, 'RFI Number: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', 'U', 12)
        self.cell(5)
        self.cell(25,10,str(rfi_number),0,0,'L')
        #################################
        self.ln(10)
        self.cell(12.5)
        self.set_font('Arial', 'B', 12)
        self.cell(40,10, 'Title: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', 'U', 12)
        self.cell(5)
        self.cell(25,10,title,0,0,'L')
        #################################
        self.ln(10)
        self.cell(12.5)
        self.set_font('Arial', 'B', 12)
        self.cell(40,10, 'Drawing Reference: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', 'U', 12)
        self.cell(5)
        self.cell(25,10,dwg_refer,0,0,'L')
        #################################
        self.cell(30)
        self.set_font('Arial', 'B', 12)
        self.cell(50,10, 'Specification Reference: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', 'U', 12)
        self.cell(5)
        self.cell(25,10,spec_refer,0,0,'L')
        #################################
        self.ln(10)
        self.cell(12.5)
        self.set_font('Arial', 'B', 12)
        self.cell(40,10, 'Date Recieved: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', 'U', 12)
        self.cell(5)
        self.cell(25,10,date_received,0,0,'L')
        #################################
        self.cell(30)
        self.set_font('Arial', 'B', 12)
        self.cell(50,10, 'Response Date: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', 'U', 12)
        self.cell(5)
        self.cell(50,10,date_response,0,0,'L')
        #################################
        self.ln(10)
        self.cell(12.5)
        self.set_font('Arial', 'B', 12)
        self.cell(25,10, 'Response: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', '', 12)
        self.ln(10)
        self.cell(14)
        self.multi_cell(170,8,response,0,0,'L',False)
        #################################
        self.set_y(245)
        self.cell(12.5)
        self.set_font('Arial', 'B', 12)
        self.cell(25,10, 'Reviewer: ',0,0,'L')
        ###### Add actual RFI Info ######
        self.set_font('Arial', 'U', 12)
        self.cell(5)
        self.cell(25,10,reviewer,0,0,'L')
        #################################
        


