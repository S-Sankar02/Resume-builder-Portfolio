import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from flask import current_app
from models.portfolio import Portfolio


class ExportService:

    @staticmethod
    def export_pdf(portfolio_id):

        # 🔥 SAFE FETCH
        portfolio = Portfolio.query.get(portfolio_id)

        if not portfolio:
            raise Exception("Portfolio not found")

        # 🔥 SAFE DATA
        data = portfolio.data or {}
        hero = data.get("hero", {})

        title = hero.get("name", "My Portfolio")
        bio = hero.get("bio", "No bio available")

        # 🔥 SAFE PATH (NO E:/ EVER)
        base_path = current_app.root_path
        export_dir = os.path.join(base_path, "static", "export")

        os.makedirs(export_dir, exist_ok=True)

        file_path = os.path.join(export_dir, f"portfolio_{portfolio_id}.pdf")

        # PDF GENERATION
        c = canvas.Canvas(file_path, pagesize=letter)

        y = 750

        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, y, title)

        y -= 40

        c.setFont("Helvetica", 12)
        c.drawString(100, y, bio)

        c.save()

        # return URL
        return f"/static/export/portfolio_{portfolio_id}.pdf"