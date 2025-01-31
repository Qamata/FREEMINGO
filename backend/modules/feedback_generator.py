from fpdf import FPDF

def generate_feedback(scores):
    feedback = f"Fluency: {scores['fluency']}\nGrammar: {scores['grammar']}\nVocabulary: {scores['vocabulary']}"
    return feedback

def generate_pdf_report(scores, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="IELTS Speaking Test Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Fluency: {scores['fluency']}", ln=True)
    pdf.cell(200, 10, txt=f"Grammar: {scores['grammar']}", ln=True)
    pdf.cell(200, 10, txt=f"Vocabulary: {scores['vocabulary']}", ln=True)
    pdf.output(file_path)
