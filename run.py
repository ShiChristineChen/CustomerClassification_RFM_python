
"""This program will focus on developing a program package for the application of RFM (Recency, Frequency, Monetary Value)
model and output the customer classification results into a new document.
Name: Shi Chen
Date:28/05/2020
"""

from app.saver import Saver

if __name__ == '__main__':
    saver = Saver()
    saver.reset()
    saver.customer_to_csv()
    saver.customer_by_cate_chart()
