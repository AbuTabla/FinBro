
import pickle 

## Building the User's portfolio 

portfolio = {}

# Ask the user for input in a loop
while True:
    # Ask for the stock abbreviation
    stock = input("Please enter the stock abbreviation (or 'quit' to finish): ")
    
    # Check if the user wants to quit
    if stock.lower() == 'quit':
        break
    
    # Ask for the number of shares
    num_shares = input("Please enter the number of shares: ")
    
    # Error checking: Make sure it's a positive integer
    try:
        num_shares = int(num_shares)
        if num_shares <= 0:
            print("Number of shares should be a positive integer.")
            continue
    except ValueError:
        print("Number of shares should be a positive integer.")
        continue

    # Add the stock and number of shares to the portfolio
    portfolio[stock] = num_shares

# Save the portfolio to a file
with open('./data/portfolio.pkl', 'wb') as f:
    pickle.dump(portfolio, f)