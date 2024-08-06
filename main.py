import sys
from data_classes import *

def run():
    # Check if argument provided
    if len(sys.argv) == 1:
        print('Please Provide the output currency, i.e. USD')
        exit()
    
    # Save currency if only the code is correct
    h.check_currency(sys.argv[1])
  
    # Store input data from csv file in a portfolio variable
    portfolio = Portfolio(h.read_input())

    # Display summary in a representative way
    h.display_summary(portfolio)

if __name__ == '__main__':
    run()
