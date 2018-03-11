# -*- coding: utf-8 -*-
"""
@author: Michael Irvine

Unit test for PriceBasket.py
"""

from io import StringIO
import sys
import unittest
import PriceBasket

# Test the PriceLookup function
class PriceLookup(unittest.TestCase):
    
    def test_PriceBasket_PriceLookup_with_recognised_goods(self):
        
        # Test recognised goods written with a variety of cases
        result = PriceBasket.PriceLookup("Apples")
        self.assertAlmostEqual(result,1.0), "PriceLookup returns wrong price for apples"
        result = PriceBasket.PriceLookup("bread")
        self.assertAlmostEqual(result,0.8), "PriceLookup returns wrong price for bread" 
        result = PriceBasket.PriceLookup("MILK")
        self.assertAlmostEqual(result,1.3) , "PriceLookup returns wrong price for milk"
        result = PriceBasket.PriceLookup("SOup")
        self.assertAlmostEqual(result,0.65), "PriceLookup returns wrong price for soup"
        
    def test_PriceBasket_PriceLookup_with_unrecognised_goods(self):
        
        # Test unrecognised goods, only strings are tested because 'goodsList = list(sys.argv[1:])' always contains only strings
        result = PriceBasket.PriceLookup("cheese")
        assert result == None, "PriceLookup should return None for cheese"
        result = PriceBasket.PriceLookup("-\"-")
        assert result == None, "PriceLookup should return None for -\"-"
        result = PriceBasket.PriceLookup("123")
        assert result == None, "PriceLookup should return None for Integers"
        result = PriceBasket.PriceLookup("1.23")
        assert result == None, "PriceLookup should return None for Floats"

# Test the FormatCurrency function        
class FormatCurrency(unittest.TestCase):
    
    def test_PriceBasket_FormatCurrency(self):
        
        # Test the formatting of a variety of values
        result = PriceBasket.FormatCurrency(1.25)
        assert result == "£1.25", "FormatCurrency should return £1.25 for 1.25"
        result = PriceBasket.FormatCurrency(250.0)
        assert result == "£250.00", "FormatCurrency should return £250.00 for 250.0"
        result = PriceBasket.FormatCurrency(0.99)
        assert result == "99p", "FormatCurrency should retrun 99p for 0.99"
        result = PriceBasket.FormatCurrency(0.0)
        assert result == "0p", "FormatCurrency should retrun 0p for 0.0"
        
# Test the GoodsCount function        
class GoodsCount(unittest.TestCase):
    
    correctGoodsList = ["Apples",
                        "BRead",
                        "bread",
                        "SOUP"]
    
    incorrectGoodsList = ["ApplesSoup",
                          ",",
                          "123",
                          "---"]
    
    def test_PriceBasket_GoodsCount_with_correct_list(self):
        
        # Second argument in each call is not controlled by user, no need to test particularly bad inputs
        result = PriceBasket.GoodsCount(self.correctGoodsList, "BREAD")
        assert result == 2, "GoodsCount should return 2 for correctGoodsList and 'BREAD'"
        result = PriceBasket.GoodsCount(self.correctGoodsList, "Milk")
        assert result == 0, "GoodsCount should return 0 for correctGoodsList and 'Milk'"
        
    def test_PriceBasket_GoodsCount_with_incorrect_list(self):
        
        # Second argument in each call is not controlled by user, no need to test particularly bad inputs
        result = PriceBasket.GoodsCount(self.incorrectGoodsList, "apples")
        assert result == 0, "GoodsCount should return 0 for incorrectGoodsList and 'apples'"
        result = PriceBasket.GoodsCount(self.incorrectGoodsList, "SOUP")
        assert result == 0, "GoodsCount should return 0 for incorrectGoodsList and 'SOUP'"
        
# Test the Subtotal function        
class Subtotal(unittest.TestCase):
    
    # Recognised goods written with a variety of cases
    correctGoodsList = ["Apples",
                        "BRead",
                        "milk",
                        "SOUP"]
    
    # Mixture of recognised and unrecognised goods
    mixedGoodsList = ["Soup",
                      "Soupbread",
                      "apples",
                      "mlik"]
    
    # Unrecognised goods, only strings are tested because 'goodsList = list(sys.argv[1:])' always contains only strings
    incorrectGoodsList = ["ApplesSoup",
                          ",",
                          "123",
                          "---"]
    
    def test_PriceBasket_Subtotal_with_fully_correct_list(self):
        
        stringResult, floatResult, listResult = PriceBasket.Subtotal(self.correctGoodsList)
        assert stringResult == "Subtotal: £3.75\n", "Subtotal subtotalOutput should return 'Subtotal: £3.75' for correct goods list"
        self.assertAlmostEqual(floatResult,3.75), "Subtotal subtotalValue should return 3.75 for correct goods list"
        assert listResult == [], "Subtotal invalidGoodsList should return empty for correct goods list"
        
    def test_PriceBasket_Subtotal_with_partially_correct_list(self):
        
        stringResult, floatResult, listResult = PriceBasket.Subtotal(self.mixedGoodsList)
        assert stringResult == "Subtotal: £1.65\n", "Subtotal subtotalOutput should return 'Subtotal: £1.65' for mixed goods list"
        self.assertAlmostEqual(floatResult,1.65), "Subtotal subtotalValue should return 1.65 for mixed goods list"
        assert listResult == ["Soupbread", "mlik"], "Subtotal invalidGoodsList should return ['Soupbread', 'mlik'] for mixed goods list"
        
    def test_PriceBasket_Subtotal_with_fully_incorrect_list(self):

        stringResult, floatResult, listResult = PriceBasket.Subtotal(self.incorrectGoodsList)
        assert stringResult == "", "Subtotal subtotalOutput should return '' for incorrect goods list"
        self.assertAlmostEqual(floatResult,0), "Subtotal subtotalValue should return 0 for incorrect goods list"
        assert listResult == [], "Subtotal invalidGoodsList should return [] for incorrect goods list"

# Test the Savings function        
class Savings(unittest.TestCase):
    
    # List with no possible deals
    noDealsList = ["Bread",
                   "bread",
                   "MILK",
                   "soup"]
    
    # List with deals
    dealsList1 = ["apples",
                  "Apples",
                  "soup",
                  "soup",
                  "soup",
                  "SOUP",
                  "Soup",
                  "bread",
                  "Bread"]
    # List with deals
    dealsList2 = ["SOup",
                  "Soup",
                  "soup",
                  "soup",
                  "soup",
                  "SOUP",
                  "BREAD",
                  "bread",
                  "bread",
                  "Bread"]
    # List with deals
    dealsList3 = ["soup",
                  "soup",
                  "soup",
                  "SOUP",
                  "Bread"]

    def test_PriceBasket_Savings_with_no_possible_deal(self):
        
        stringResult, floatResult = PriceBasket.Savings(self.noDealsList)
        assert stringResult == "(no offers available)\n", "Savings savingsOutput should return '(no offers available)\n' for no deals list"
        self.assertAlmostEqual(floatResult,0), "Savings savingsValue should return 0 for no deals List"
                                
    def test_PriceBasket_Savings_with_possible_deals(self):
        
        # Test with list containing just "Apples"
        stringResult, floatResult = PriceBasket.Savings(["Apples"])
        assert stringResult == "Apples 10% off: -10p\n", "Savings savingsOutput should return 'Apples 10% off: -10p\n' for 'Apples'"
        self.assertAlmostEqual(floatResult,0.1), "Savings savingsValue should return 0.1 for 'Apples'"
        # Test with list containing 2 apples, 5 soups and 2 breads. Possible deals: 2 x apples deal, 2 x bread/soup deal 
        stringResult, floatResult = PriceBasket.Savings(self.dealsList1)
        assert stringResult == "Apples 10% off: -20p\nBread 50% off with 2 tins of soup: -80p\n", "Savings savingsOutput should return 'Apples 10% off: -20p\nBread 50% off with 2 tins of soup: -80p\n' for deals list 1"
        self.assertAlmostEqual(floatResult,1.0), "Savings savingsValue should return 1.0 for deals list 1"
        # Test with list containing 6 soups and 4 breads. Possible deals: 3 x bread/soup deal
        stringResult, floatResult = PriceBasket.Savings(self.dealsList2)
        assert stringResult == "Bread 50% off with 2 tins of soup: -£1.20\n", "Savings savingsOutput should return 'Bread 50% off with 2 tins of soup: -£1.20\n' for deals list 2"
        self.assertAlmostEqual(floatResult,1.2), "Savings savingsValue should return 1.2 for deals list 2"
        # Test with list containing 4 soups and 1 bread. Possible deals: 1 x bread/soup deal
        stringResult, floatResult = PriceBasket.Savings(self.dealsList3)
        assert stringResult == "Bread 50% off with 2 tins of soup: -40p\n", "Savings savingsOutput should return 'Bread 50% off with 2 tins of soup: -40p\n' for deals list 3"
        self.assertAlmostEqual(floatResult,0.4), "Savings savingsValue should return 0.4 for deals list 3"

# Test the Total function        
class Total(unittest.TestCase):
    
    def test_PriceBasket_Total(self):
        
        # Test with value for subtotal but no value for savings
        result = PriceBasket.Total(0.50, 0)
        assert result == "Total: 50p\n"
        # Test with values for subtotal and savings
        result = PriceBasket.Total(18.70, 5.35)
        assert result == "Total: £13.35\n"

# Test the Output function        
class Output(unittest.TestCase):
    
    # Test with example subtotal, savings and total outputs
    def test_PriceBasket_Output(self):
        capturedOutput = StringIO()
        oldOutput = sys.stdout
        # "try" used to prevent fuction failure from preventing reassignment of sys.stdout
        try:
            sys.stdout = capturedOutput
            PriceBasket.Output("Subtotal: £2.00\n", "Apples 10% off: -20p\n", "Total: £1.80\n")
            assert capturedOutput.getvalue() == "Subtotal: £2.00\nApples 10% off: -20p\nTotal: £1.80\n\n", "Output text does not match component outputs"
        finally:
            sys.stdout = oldOutput
        
if __name__ == "__main__":
    unittest.main()