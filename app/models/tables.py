
"""This program will focus on developing a program package for the application of RFM (Recency, Frequency, Monetary Value)
model and output the customer classification results into a new document.
Name: Shi Chen
Date:28/05/2020
"""


from datetime import date

import sqlalchemy as sa

from app.models.base import Base


class Investment(Base):
    """Define a table class Investment which is used to store the source data.
    """
    __tablename__ = 'investment'

    id = sa.Column(sa.Integer, primary_key=True)
    customer_id = sa.Column(sa.BigInteger)
    invested_at = sa.Column(sa.Date)
    invested_amount = sa.Column(sa.Float)

    def __init__(self, customer_id: int, invested_at: date,
                 invested_amount: float):
        """Define initial state."""
        self.customer_id = customer_id
        self.invested_at = invested_at
        self.invested_amount = invested_amount


class Customers(Base):
    """Define a table class Customers to store the result of customer classification data.
    """
    __tablename__ = 'customers'

    id = sa.Column(sa.Integer, primary_key=True)
    customer_id = sa.Column(sa.BigInteger)
    recency = sa.Column(sa.Date)
    frequency = sa.Column(sa.Integer)
    monitory = sa.Column(sa.Float)
    category = sa.Column(sa.String)

    def __init__(self, customer_id: int, recency: date, frequency: int,
                 monetary: float, category: str):
        self.customer_id = customer_id
        self.recency = recency
        self.frequency = frequency
        self.monetary = monetary
        self.category = category
