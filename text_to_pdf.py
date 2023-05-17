from fpdf import FPDF
import uuid
 
def gen_pdf(text_array, array_ids):
	pdf = FPDF()
	print(len(array_ids))
	pdf.add_font('NTR', '', "fonts/TNR.ttf", uni=True)
	pdf.set_font('NTR', size=15)

	 
	for line in text_array:
		pdf.add_page()
		pdf.multi_cell(0, 10, line, 0, 'L', False)

	name = f"files/{uuid.uuid4().hex.upper()}.pdf"
	pdf.output(name)
	return name