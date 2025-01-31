from fpdf import FPDF

def generate_feedback(text, scores, mode, part):
    feedback = f"Fluency: {scores['fluency']}\nGrammar: {scores['grammar']}\nVocabulary: {scores['vocabulary']}"
    if mode == 'test':
        feedback += f"\n\nPart {part + 1} Feedback: You did well, but try to improve your vocabulary."
    return feedback

def generate_pdf_report(feedback, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="IELTS Speaking Test Report", ln=True, align="C")
    pdf.multi_cell(0, 10, txt=feedback)
    pdf.output(file_path)