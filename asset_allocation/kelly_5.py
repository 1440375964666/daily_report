from risk_4 import losing_percentage, risk
import random

losing_percentage = risk / 100
winning_percentage = (100 - risk) / 100
net_odd = 4.336129

def kelly_fraction(winning_probability, net_odd):
    """
    p: Probability of winning
    b: Net odds (b to 1, e.g., 1 if you double your money)
    """
    return (winning_probability*net_odd - (losing_percentage)) / net_odd
kelly = kelly_fraction(winning_percentage, net_odd) * 100

if kelly < 0:
    asset_allocation = f"⁜⁜⁜ KELLY CRITERION ASSET ALLOCATION: Short {abs(kelly):.2f}% VN30 || Hold 0% stocks || Hold {100 - abs(kelly):.2f}% cash"
else:
    asset_allocation = f"⁜⁜⁜ KELLY CRITERION ASSET ALLOCATION: Short 0% VN30 || Hold {kelly:.2f}% stocks || Hold {100 - kelly:.2f}% cash"
# print(kelly)