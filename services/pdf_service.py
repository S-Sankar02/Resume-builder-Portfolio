from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class PDFService:

    @staticmethod
    def generate_resume_pdf(resume, filename):

        c = canvas.Canvas(filename, pagesize=letter)
        y = 750

        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, y, resume.title or "Resume")

        y -= 40

        c.setFont("Helvetica", 12)
        c.drawString(100, y, resume.summary or "")

        y -= 40

        # Education / Experience / Skills (simple text export)
        for section in ["education", "experience", "skills", "projects"]:
            c.setFont("Helvetica-Bold", 14)
            c.drawString(100, y, section.upper())
            y -= 20

            c.setFont("Helvetica", 10)
            c.drawString(100, y, f"Exported {section} data...")
            y -= 40

        c.save()

        return filename
    