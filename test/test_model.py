
"""This program will focus on developing a program package for the application of RFM (Recency, Frequency, Monetary Value)
model and output the customer classification results into a new document.
Name: Shi Chen
Date:28/05/2020
"""



import unittest

from app.models.dao import Dao


class TestModel(unittest.TestCase):
    """Define a test class TestModel"""

    dao = None
    COUNT_INVESTMENT = 55
    COUNT_CUSTOMER = 9

    @classmethod
    def setUpClass(cls) -> None:
        """Prepare for testing the class action"""
        print('setUpClass started')
        cls.dao = Dao(echo=True)
        cls.dao.reset_db()
        print('setUpClass ended')

    @classmethod
    def tearDownClass(cls) -> None:
        """Finish the testing of the class action"""
        print('tearDownClass started')
        cls.dao.reset_db()
        print('tearDownClass ended')

    def setUp(self):
        """Prepare for testing the self action"""
        print('setUp started')
        self.dao.import_csv()
        print('setUp ended')

    def tearDown(self):
        """Finish the testing of self action"""
        print('tearDown started')
        self.dao.reset_db()
        print('tearDown ended')

    def test_import_csv(self):
        """Test the import function
        """
        self.dao.import_csv()
        self.assertEqual(2 * self.COUNT_INVESTMENT,
                         self.dao.count_investment())

    def test_customers(self):
        """
        Test the update_customer function.
        """
        self.dao.update_customer()
        self.assertEqual(self.COUNT_CUSTOMER, self.dao.count_customers())


if __name__ == '__main__':
    unittest.main(verbosity=2)
