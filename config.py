import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # path
    DB_DIR = ''.join([basedir, '/data'])
    SRC_CSV = ''.join([DB_DIR, '/COSC480_project_data.txt'])
    SQLT_DB = ''.join([DB_DIR, '/app.db'])
    CUSTOMERS_CSV = ''.join([DB_DIR, '/customers.csv'])
    CHART_CUSTOMER = ''.join([DB_DIR, '/customer_by_category.png'])
