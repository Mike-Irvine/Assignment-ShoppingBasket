# -*- coding: utf-8 -*-
"""
@author: Michael Irvine

Calculate subtotals, savings and totals from a list of goods
"""

import sys

def main():
    
    # Retrieve user arguments
    goodsList = list(sys.argv[1:])
    
    # Check if list is empty (no arguments submitted)
    if len(goodsList) == 0:
        print("User list must contain at least one item.")
    else:
        
        # Calculate Subtotal and retrieve list of unrecognised inputs
        subtotalOutput, subtotalValue, invalidGoodsList = Subtotal(goodsList)
        
        # Check if subtotal function found any recognisable items (at least some costs added to subtotal)
        if subtotalValue == 0:
            print("No recognised items on list.")
        else:
            
            # Calculate Savings
            savingsOutput, savingsValue = Savings(goodsList)
            
            # Calculate Total
            totalOutput = Total(subtotalValue, savingsValue)
            
            # Before output print list of unrecognised items.
            if invalidGoodsList != []:
                print("The following items were not recognised: %s" % ", ".join(invalidGoodsList))
            
            # Print output
            Output(subtotalOutput, savingsOutput, totalOutput)

# Calculate subtotal of goods listed        
def Subtotal(goodsList):
    
    # Initialise subtotal value
    subtotalValue = 0
    
    # Initialise list for storing invalid goods
    invalidGoodsList = []
    
    # Return cost for each item
    for goods in goodsList:
        
        # Error catching used to prevent unrecognised goods from causing an exception
        try:

            # Add value of goods to subtotal value
            subtotalValue += PriceLookup(goods)
            
        # Catches errors relating to the addition of an Int and a NoneValue (which appear when the dictionary receives an unrecognised Key)
        except TypeError:

            # Unrecognised item added to tracking list
            invalidGoodsList.append(goods)
            # Proceed with next item in goodsList
            continue
    
    if subtotalValue > 0:
        # At least some recognised goods were provided
        subtotalOutput = "Subtotal: " + FormatCurrency(subtotalValue) + "\n"
        return subtotalOutput, subtotalValue, invalidGoodsList
    else:
        # no recognised goods were provided, return nothing
        # No return is necessary as standard error message will be printed from main() when subtotalValue == 0
        return "", 0, []

# Calculate savings for goods listed
def Savings(goodsList):
    
    # Initialise savings text and values
    savingsOutput = ""
    savingsValue = 0
    soupSavingsValue = 0
    
    # Calculate item counts
    applesCount = GoodsCount(goodsList, "apples")
    breadCount = GoodsCount(goodsList, "bread")
    soupCount = GoodsCount(goodsList, "soup")

    # Initialise temporary item count variables
    breadCountTemp = breadCount
    soupCountTemp = soupCount
    
    # Initialise savings count
    soupSavingsCount = 0
    
    # Calculate total savings on apples (10% of total cost of apples)
    applesSavingsValue = applesCount * PriceLookup("apples") * 0.1
                                         
    # Calculate total savings for soup/bread combo. For every 2 soup, 1 bread is half price
    if soupCount > 1 and breadCount > 0:
        # if at least 1 bread left deal still possible
        while breadCountTemp > 0 and soupCountTemp > 1:
            # if at least 2 soup also left deal can be applied
#            if soupCountTemp > 1:
            # reduce the remaining numbers of bread and soup
            soupSavingsCount += 1
            breadCountTemp -= 1
            soupCountTemp -= 2
        
        # Savings value = number of possible savings multiplied by half the price of bread
        soupSavingsValue = soupSavingsCount * PriceLookup("bread") * 0.5
    
    if applesSavingsValue != 0:
        
        # Add value saved to savings total
        savingsValue += applesSavingsValue
        # Add savings description to savings string
        savingsOutput += "Apples 10% off: -" + FormatCurrency(applesSavingsValue) + "\n"
    
    if soupSavingsValue != 0:
        
        # Add value saved to savings total
        savingsValue += soupSavingsValue
        # Add savings description to savings string
        savingsOutput += "Bread 50% off with 2 tins of soup: -" + FormatCurrency(soupSavingsValue) + "\n"
    
    if savingsValue == 0:
        
        # If no savings have been made update savings string
        savingsOutput = "(no offers available)\n"
    
    # Return combined savings string and total value saved
    return savingsOutput, savingsValue

# Calculate final cost based on subtotal and savings
def Total(subtotalValue, savingsValue):
    
    # Calculate Total cost and construct "Total" line of output
    return "Total: " + FormatCurrency(subtotalValue-savingsValue) + "\n"

# Print final output
def Output(subtotalOutput, savingsOutput, totalOutput):
    
    # Construct and print final output
    print(subtotalOutput + savingsOutput + totalOutput)

# Retrieve price from list of known goods
def PriceLookup(goods):
    
    # Dictionary of known goods with prices
    knownGoods = {"apples": 1.0,
                  "bread": 0.8,
                  "milk": 1.3,
                  "soup": 0.65}
    
    # Return the price of the specified good (converted to lowercase)
    return knownGoods.get(goods.lower())

# Format costs to correctly display either "£" or "p"
def FormatCurrency(currencyValue):
    # Values greater than or equal to £1
    if currencyValue >= 1:
        currencyString = "£" + str(format(currencyValue, ".2f"))
    # Values less than £1
    else:
        currencyString = str(format(currencyValue*100, ".0f") + "p")
    return currencyString

# Case insensitive counting of matching items in a list
def GoodsCount(goodsList, goods):
    
    # Initialise list
    goodsLower = []
    
    # Duplicate list provided in argument all in lowercase
    for g in goodsList:
        goodsLower.append(g.lower())
    
    # Return count of lowercase goods in lowercase list
    return goodsLower.count(goods.lower())

if __name__ == "__main__":
    main()