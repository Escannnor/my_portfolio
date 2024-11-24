import requests
import os
import time
import pandas as pd
from dotenv import load_dotenv
import customtkinter as ctk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


load_dotenv()

# CoinMarketCap API setup
CMC_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
CMC_BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Gemini API setup
GEMINI_BASE_URL = "https://api.gemini.com/v1"

# Fetching cryptocurrency data with error handling
def fetch_cryptocurrency_data():
    try:
        headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": CMC_API_KEY}
        params = {"start": "1", "limit": "10", "convert": "USD"}
        response = requests.get(CMC_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("data")
    except requests.RequestException:
        messagebox.showerror("Error", "Failed to fetch data from CoinMarketCap.")
        return None

# Gemini trading insights
def fetch_gemini_trading_insight(symbol):
    url = f"{GEMINI_BASE_URL}/pubticker/{symbol.lower()}usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"Bid Price": data["bid"], "Ask Price": data["ask"], "Last Price": data["last"]}
    except requests.RequestException:
        return {"Bid Price": None, "Ask Price": None, "Last Price": None}

# Format data
def format_cryptocurrency_data(data):
    rows = []
    for item in data:
        gemini_data = fetch_gemini_trading_insight(item["symbol"])
        rows.append({
            "Name": item["name"],
            "Symbol": item["symbol"],
            "Price (USD)": item["quote"]["USD"]["price"],
            "Market Cap": item["quote"]["USD"]["market_cap"],
            "24h Change (%)": item["quote"]["USD"]["percent_change_24h"],
            "Bid Price (Gemini)": gemini_data["Bid Price"],
            "Ask Price (Gemini)": gemini_data["Ask Price"],
            "Last Price (Gemini)": gemini_data["Last Price"]
        })
    return pd.DataFrame(rows)

class CryptoTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cryptocurrency Tracker")
        self.geometry("800x700")
        
        # Title
        self.title_label = ctk.CTkLabel(self, text="Cryptocurrency Tracker", font=("Arial", 24))
        self.title_label.pack(pady=10)
        
        # Table
        self.tree = ttk.Treeview(self, columns=("Symbol", "Price", "Market Cap", "24h Change", "Bid Price", "Ask Price"), show="headings")
        self.tree.heading("Symbol", text="Symbol")
        self.tree.heading("Price", text="Price (USD)")
        self.tree.heading("Market Cap", text="Market Cap")
        self.tree.heading("24h Change", text="24h Change (%)")
        self.tree.heading("Bid Price", text="Bid Price (Gemini)")
        self.tree.heading("Ask Price", text="Ask Price (Gemini)")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Buttons
        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.update_data)
        self.refresh_button.pack(pady=5)
        self.plot_price_change_button = ctk.CTkButton(self, text="Plot 24h Price Change", command=self.plot_price_change)
        self.plot_price_change_button.pack(pady=5)
        self.plot_market_cap_button = ctk.CTkButton(self, text="Plot Market Cap Distribution", command=self.plot_market_cap)
        self.plot_market_cap_button.pack(pady=5)
        self.plot_bid_ask_button = ctk.CTkButton(self, text="Plot Bid-Ask Spread", command=self.plot_bid_ask)
        self.plot_bid_ask_button.pack(pady=5)

        # Initial Load
        self.update_data()
        self.auto_refresh()

    def update_data(self):
        self.tree.delete(*self.tree.get_children())
        data = fetch_cryptocurrency_data()
        if data:
            self.data_df = format_cryptocurrency_data(data)
            for _, row in self.data_df.iterrows():
                self.tree.insert("", "end", values=(
                    row["Symbol"], f"${row['Price (USD)']:.2f}", f"${row['Market Cap']:.2e}", 
                    f"{row['24h Change (%)']:.2f}%", row["Bid Price (Gemini)"], row["Ask Price (Gemini)"]
                ))

    def auto_refresh(self):
        self.update_data()
        self.after(60000, self.auto_refresh)  # Refresh every minute

    # Graph for 24h price change
    def plot_price_change(self):
        if hasattr(self, 'data_df'):
            symbols = self.data_df['Symbol']
            price_changes = self.data_df['24h Change (%)']
            fig, ax = plt.subplots()
            ax.bar(symbols, price_changes, color="skyblue")
            ax.set_title("24h Price Change (%)")
            ax.set_xlabel("Cryptocurrency")
            ax.set_ylabel("24h Change (%)")
            self.display_graph(fig)

    # Market cap distribution pie chart
    def plot_market_cap(self):
        if hasattr(self, 'data_df'):
            fig, ax = plt.subplots()
            ax.pie(self.data_df['Market Cap'], labels=self.data_df['Symbol'], autopct='%1.1f%%')
            ax.set_title("Market Cap Distribution")
            self.display_graph(fig)

    # Bid-Ask spread
    def plot_bid_ask(self):
        if hasattr(self, 'data_df'):
            symbols = self.data_df['Symbol']
            bid_prices = [float(bid) if bid else 0 for bid in self.data_df['Bid Price (Gemini)']]
            ask_prices = [float(ask) if ask else 0 for ask in self.data_df['Ask Price (Gemini)']]
            fig, ax = plt.subplots()
            ax.bar(symbols, bid_prices, label="Bid Price")
            ax.bar(symbols, ask_prices, label="Ask Price", alpha=0.5)
            ax.set_title("Bid-Ask Spread")
            ax.set_xlabel("Cryptocurrency")
            ax.set_ylabel("Price (USD)")
            ax.legend()
            self.display_graph(fig)

    def display_graph(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
        
if __name__ == "__main__":
    app = CryptoTrackerApp()
    app.mainloop()
