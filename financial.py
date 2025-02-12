import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = yf.download("AAPL", start="2023-01-01", end="2024-01-01")
print("Columns:", data.columns)
if "Adj Close" in data.columns:
    data["Return"] = data["Adj Close"].pct_change()
else:
    data["Return"] = data["Close"].pct_change()
data.dropna(inplace=True)
print("\nSummary:")
print(data.describe())
data["MA50"] = data["Close"].rolling(50).mean()
data["MA200"] = data["Close"].rolling(200).mean()
plt.figure(figsize=(12, 6))
plt.plot(data["Close"], label="Close", color="blue")
plt.plot(data["MA50"], label="50-day MA", color="red")
plt.plot(data["MA200"], label="200-day MA", color="green")
plt.title("AAPL Price & Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()
plt.show()
plt.figure(figsize=(10, 5))
sns.histplot(data["Return"], bins=50, kde=True, color="purple")
plt.title("AAPL Daily Returns")
plt.xlabel("Return")
plt.ylabel("Frequency")
plt.grid()
plt.show()
plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("AAPL Data Correlation")
plt.show()

