from models import db
from models.portfolio import Portfolio

class PortfolioService:

    @staticmethod
    def create(user_id, data=None):
        data = data or {}

        p = Portfolio(
            user_id=user_id,
            title=data.get("title", "My Portfolio"),
            template=data.get("template", "modern"),
            data=data
        )

        db.session.add(p)
        db.session.commit()
        return p.id

    @staticmethod
    def get(pid):
        return Portfolio.query.get_or_404(pid)

    @staticmethod
    def update(pid, data):
        p = Portfolio.query.get_or_404(pid)
        p.data = data
        db.session.commit()
        return p
    