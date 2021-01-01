"""This program will focus on developing a program package for the application of RFM (Recency, Frequency, Monetary Value)
model and output the customer classification results into a new document.
Name: Shi Chen
Date:28/05/2020
"""

import csv
from datetime import datetime
from functools import wraps
from typing import List

from sqlalchemy import create_engine, func, literal, case, and_
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
from app.models.tables import Investment, Customers
from config import Config

__all__ = ['Dao']


def session_factory(echo: bool):
    """
    Design a session maker class SingletonMeta.
    """

    engine = create_engine('sqlite:///{0}'.format(Config.SQLT_DB), echo=echo)
    _SessionFactory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return _SessionFactory()


def _commit(fn):
    """Decorator to commit"""
    @wraps(fn)
    def helper(*args, **kwargs):
        res = fn(*args, **kwargs)
        args[0].session.commit()
        return res

    return helper


class SingletonMeta(type):
    """A metaclass to restricts the instantiation of a class
    to one "single" instance."""
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class Dao(metaclass=SingletonMeta):
    """Define a data access object pattern. """
    __slots__ = ['session']

    def __init__(self, echo=False):
        """Define initial state."""
        self.session = session_factory(echo)

    @_commit
    def reset_db(self) -> None:
        """Reset the initial state."""
        self.session.query(Investment).delete()
        self.session.query(Customers).delete()

    @_commit
    def import_csv(self):
        """Import the raw data and read"""
        def _investment_mapper(investment: List[str]):
            customer_id = int(investment[0])
            dt = datetime.strptime(investment[1], '%d/%m/%Y')
            amount = float(investment[2])
            return Investment(customer_id, dt, amount)

        with open(Config.SRC_CSV, 'r') as outfile:
            reader = csv.reader(outfile, delimiter='\t')
            # skip header
            next(reader, None)
            seq_object = [_investment_mapper(row) for row in reader]
            self.session.bulk_save_objects(seq_object)

    def count_investment(self):
        """Count number for test"""
        return self.session.query(func.count(Investment.id)).first()[0]

    def update_customer(self):
        """Store the results of recency, frequency and monetary into subquery."""
        # Subquery of customer information
        sub_customers = self.session.query(
            Investment.customer_id.label("customer_id"),
            func.max(Investment.invested_at).label("recency"),
            func.count(Investment.id).label("frequency"),
            func.sum(Investment.invested_amount).label("monetary")).group_by(
                Investment.customer_id).subquery()

        # Use the FRM model to calculate the classification standard
        sub_avg = self.session.query(
            func.avg(sub_customers.c.recency).label("recency"),
            func.avg(sub_customers.c.frequency).label("frequency"),
            func.avg(sub_customers.c.monitory).label("monetary")).subquery()

        # F, R, M label of each customer
        sub_flags = self.session.query(
            sub_customers.c.customer_id.label("customer_id"),
            sub_customers.c.recency.label("recency"),
            sub_customers.c.frequency.label("frequency"),
            sub_customers.c.monitory.label("monetary"),
            case([(sub_customers.c.recency >= sub_avg.c.recency, 1)],
                 else_=0).label("recency_flag"),
            case([(sub_customers.c.frequency >= sub_avg.c.frequency, 1)],
                 else_=0).label("frequency_flag"),
            case([(sub_customers.c.monitory >= sub_avg.c.monitory, 1)],
                 else_=0).label("monetary_flag")).join(
                     sub_avg, literal(True)).subquery()

        # Convert the label in to customer types
        seq = self.session.query(
            sub_flags.c.customer_id.label("customer_id"),
            sub_flags.c.recency.label("recency"),
            sub_flags.c.frequency.label("frequency"),
            sub_flags.c.monitory.label("monetary"),
            case([(and_(sub_flags.c.recency_flag == 1,
                        sub_flags.c.frequency_flag == 1,
                        sub_flags.c.monitory_flag == 1), '1. VIP'),
                  (and_(sub_flags.c.recency_flag == 0,
                        sub_flags.c.frequency_flag == 1,
                        sub_flags.c.monitory_flag == 1), '2. IP'),
                  (and_(sub_flags.c.recency_flag == 1,
                        sub_flags.c.frequency_flag == 0,
                        sub_flags.c.monitory_flag == 1), '3. Low Activity'),
                  (and_(sub_flags.c.recency_flag == 0,
                        sub_flags.c.frequency_flag == 0,
                        sub_flags.c.monitory_flag == 1), '4. Low Loyalty'),
                  (and_(sub_flags.c.recency_flag == 1,
                        sub_flags.c.frequency_flag == 1,
                        sub_flags.c.monitory_flag == 0), '5. General'),
                  (and_(sub_flags.c.recency_flag == 0,
                        sub_flags.c.frequency_flag == 1,
                        sub_flags.c.monitory_flag == 0), '6. Growth'),
                  (and_(sub_flags.c.recency_flag == 1,
                        sub_flags.c.frequency_flag == 0,
                        sub_flags.c.monitory_flag == 0), '7. Primary Plus'),
                  (and_(sub_flags.c.recency_flag == 0,
                        sub_flags.c.frequency_flag == 0,
                        sub_flags.c.monitory_flag == 0), '8. Primary')],
                 else_="????").label("category")).all()

        # Combine the customer FRM information and the type together to be a object
        seq_object = [Customers(i[0], i[1], i[2], i[3], i[4]) for i in seq]
        return self.session.bulk_save_objects(seq_object)

    def count_customers(self):
        """
        Count the number of customers.
        """
        return self.session.query(func.count(Customers.id)).first()[0]

    def all_customers(self):
        """Return a complete customer classification which will be used in the output results. """
        return self.session.query(Customers.id.label('ID'),
                                  Customers.customer_id.label('Customer ID'),
                                  Customers.recency.label('Recency'),
                                  Customers.frequency.label('Frequency'),
                                  Customers.monitory.label('Total Amount'),
                                  Customers.category.label('Category')).all()
