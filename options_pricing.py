import math
import numpy as np
from tabulate import tabulate

#Main function
def main():
    #Calling option pricing functions with example values:
    """
    Current Stock Price: S = 100
    Strike Price: K = 95
    Risk-Free Interest Rate: r = 0.05 (5%)
    Volatility: sigma = 0.2
    Time until Expiry: T = 1 (year)
    Number of Time Steps in the Binomial Tree: N = 100 time steps in the binomial tree
    """
    option_type = input("Would you like to price a call or put option? ")
    print()
    
    # Calculate option prices for varying volatility values 
    headers = ["Volatility (σ)", "Black-Scholes Model Option Price (USD)", "Binomial Model Option Price (USD)"]
    table = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    i = 0
    sigma_values = np.linspace(0.1, 1.0, 10)
    for sigma in sigma_values:
        row = [0, 1, 2]
        bs_price = black_scholes_option_price(100, 95, 0.05, sigma, 1.0, option_type)
        binom_price = binomial_option_price(100, 95, 0.05, sigma, 1.0, 100, option_type)
        row[0] = sigma
        row[1] = round(bs_price, 2)
        row[2] = round(binom_price, 2)
        table[i] = row
        i = i + 1
        
    #Display results in a table
    print(f"{option_type.title()} Option Pricing with Varying Volatilities:\n")
    print(tabulate(table, headers, tablefmt="simple"))
    print()
    

#Binomial Option Pricing Model
def binomial_option_price(S, K, r, sigma, T, N, option_type):
    """
    Description:
    This function calculates and returns the price of a European option using the binomial option pricing model.
    
    Arguments:
    S: Current stock price
    K: Option strike price
    r:  Risk-free interest rate (as a decimal)
    sigma: Volatility of the underlying asset
    T: Time to expiration (in years)
    N: Number of time steps in the binomial tree
    option_type: "call" or "put"
    """
    delta_t = T / N
    u = math.exp(sigma * math.sqrt(delta_t))
    d = 1 / u
    p = (math.exp(r * delta_t) - d) / (u - d)
    q = 1 - p
    
    # Initialize the option values at expiration
    option_values = [
        max(0, (S * u**j * d**(N-j) - K) if option_type == 'call' else (K - S * u**j * d**(N-j)))
        for j in range(N + 1)
    ]
    
    # Work backwards through the tree to calculate the option value at each node
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            option_values[j] = math.exp(-r * delta_t) * (p * option_values[j + 1] + q * option_values[j])
    return option_values[0]


#Black-Scholes Option Pricing Model function
def black_scholes_option_price(S, K, r, sigma, T, option_type):
    """
    Description:
    This function calculates and returns the price of a European option using the 
    Black-Scholes stochastic differential equation option pricing model.
    
    Arguments:
    S: Current stock price
    K: Option strike price
    r:  Risk-free interest rate (as a decimal)
    sigma: Volatility of the underlying asset
    T: Time to expiration (in years)
    option_type: "call" or "put"
    """
    d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call":
        price = S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)
    elif option_type == "put":
        price = K * math.exp(-r * T) * norm_cdf(-d2) - S * norm_cdf(-d1)
    else:
        raise ValueError("Invalid option type! Must be either 'call' or 'put'.")
    return price


#Normal Cumulative Distribution Function
def norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


if __name__ == "__main__":
    main()



