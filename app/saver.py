"""This program will focus on developing a program package for the application of RFM (Recency, Frequency, Monetary Value)
model and output the customer classification results into a new document.
Name: Shi Chen
Date:28/05/2020
"""



import csv
import shutil

import pandas as pd

from config import Config
from app.models.dao import Dao

__all__ = ['Saver']


class SingletonMeta(type):
    """
        Design a session maker class SingletonMeta.
        """
    _instance = None

    def __call__(cls, *args, **kwargs):
        """Define a call function"""
        if cls._instance is None:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class Saver(metaclass=SingletonMeta):
    """Design a Saver class.
            """
    __slots__ = ['dao']

    def __init__(self):
        """"Define initial state."""

        self.dao = Dao()

    def reset(self):
        """Reset the initial state."""
        self.dao.reset_db()
        self.dao.import_csv()
        self.dao.update_customer()

    def customer_to_csv(self):
        """Save the customer classification result in to output .csv file"""
        shutil.rmtree(Config.CUSTOMERS_CSV, ignore_errors=True)
        records = self.dao.all_customers()
        with open(Config.CUSTOMERS_CSV, 'w') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(records[0].keys())
            csv_writer.writerows(records)

    def customer_by_cate_chart(self):
        """Save the customer classification pie chart into the output data folder"""
        shutil.rmtree(Config.CHART_CUSTOMER, ignore_errors=True)
        df = pd.DataFrame(self.dao.all_customers()).groupby('Category').agg(
            {'ID': 'count'})
        plot = df.plot.pie(y='ID', autopct='%1.1f%%')
        plot.get_figure().savefig(Config.CHART_CUSTOMER)
