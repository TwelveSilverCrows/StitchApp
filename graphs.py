def radio_buttons():
    import yfinance as yf
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RadioButtons, Button

    # BTC
    # ETH
    # XRP
    # Solana

    cryptos = {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Ripple": "XRP-USD",
        "Cardano": "ADA-USD",
        "Dogecoin": "DOGE-USD"
    }

    periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "5y", "max"] 

    selected_crypto = cryptos['Bitcoin']
    selected_period = '6mo'

    def update_plot(crypto_ticker, time_period):
        global selected_crypto, selected_period
        selected_crypto = crypto_ticker
        selected_period = time_period

        # Fetch data
        data = yf.Ticker(crypto_ticker).history(period=time_period)

        # Clear and update the plot
        ax.clear()
        ax.plot(data.index, data['Close'], label=f"{crypto_ticker} Price (USD)", color='blue')
        ax.set_title(f"{crypto_ticker} Price Evolution")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        ax.grid(True)
        plt.draw()

    # Matplotlib figure setup
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(left=0.32, right=0.99)

    # Initial plot
    update_plot(selected_crypto, selected_period)

    ax_crypto = plt.axes([0.02, 0.4, 0.2, 0.4])  # Position for radio buttons
    crypto_radio = RadioButtons(ax_crypto, list(cryptos.keys()))

    # Function to update crypto selection
    def crypto_selected(label):
        update_plot(cryptos[label], selected_period)

    crypto_radio.on_clicked(crypto_selected)

    # Add buttons for period selection
    ax_periods = plt.axes([0.02, 0.1, 0.2, 0.2])
    period_buttons = RadioButtons(ax_periods, periods)

    # Function to update period selection
    def period_selected(label):
        update_plot(selected_crypto, label)

    period_buttons.on_clicked(period_selected)

    # Show the interactive plot
    plt.show()

def slider_button():
    import yfinance as yf
    import matplotlib.pyplot as plt
    from matplotlib.widgets import RadioButtons, Slider

    # Define available cryptocurrencies
    cryptos = {
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Ripple": "XRP-USD",
        "Cardano": "ADA-USD",
        "Dogecoin": "DOGE-USD"
    }

    # Define corresponding time periods (in days) for slider
    periods = {
        "1 Day": 1,
        "3 Days": 3,
        "7 Days": 7,
        "1 Month": 30,
        "3 Months": 90,
        "6 Months": 180,
        "1 Year": 365,
        "5 Years": 1825,
        "Max": None  # 'Max' will fetch all available data
    }

    # Default selection
    selected_crypto = "BTC-USD"
    selected_days = 365  # Default to 1 year

    # Function to fetch and update the graph
    def update_plot(crypto_ticker, days):
        global selected_crypto, selected_days
        selected_crypto = crypto_ticker
        selected_days = days

        # Fetch historical data
        period = f"{days}d" if days is not None else "max"
        data = yf.Ticker(crypto_ticker).history(period=period)

        # Clear and update the plot
        ax.clear()
        ax.plot(data.index, data['Close'], label=f"{crypto_ticker} Price (USD)", color='blue')

        ax.set_title(f"{crypto_ticker} Price Evolution")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()
        ax.grid(True)
        plt.draw()

    # Matplotlib figure setup
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(left=0.3, bottom=0.25)

    # Initial plot
    update_plot(selected_crypto, selected_days)

    # Add radio buttons for cryptocurrency selection
    ax_crypto = plt.axes([0.02, 0.4, 0.2, 0.4])  # Position for radio buttons
    crypto_radio = RadioButtons(ax_crypto, list(cryptos.keys()))

    # Function to update crypto selection
    def crypto_selected(label):
        update_plot(cryptos[label], selected_days)

    crypto_radio.on_clicked(crypto_selected)

    # Add slider for period selection
    ax_slider = plt.axes([0.3, 0.05, 0.6, 0.03])  # Position for the slider
    slider = Slider(ax_slider, "Time Period (Days)", 1, 1825, valinit=selected_days, valstep=30)

    # Function to update period selection
    def period_selected(val):
        days = int(val)
        update_plot(selected_crypto, days)

    slider.on_changed(period_selected)

    # Show the interactive plot
    plt.show()

slider_button()