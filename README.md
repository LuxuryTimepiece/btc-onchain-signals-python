# Bitcoin On-Chain Signals Engine

![Project Screenshot](https://raw.githubusercontent.com/LuxuryTimepiece/btc-onchain-signals-python/refs/heads/master/dashboard.png)  
![Project Screenshot](https://raw.githubusercontent.com/LuxuryTimepiece/btc-onchain-signals-python/refs/heads/master/about.png)

## Overview

The Bitcoin On-Chain Signals Engine is a full-stack web application that provides real-time insights into Bitcoin's on-chain metrics and generates trading signals based on technical indicators like the Relative Strength Index (RSI). The app fetches data from multiple APIs (CoinGecko, Blockchain.com, and mempool.space) and displays key metrics such as Bitcoin price, transaction volume, active addresses, block height, fee rates, and historical trends over the last 30 days. The frontend features an interactive dashboard with charts and a historical data table, while the backend handles data fetching and WebSocket communication for live updates.

This project is a work-in-progress and was built to demonstrate skills in full-stack development, API integration, real-time data processing, and data visualization. It’s currently hosted live for portfolio purposes (add the live URL here if deployed).

---

## Features

- **Real-Time Data**: Fetches and displays Bitcoin price, on-chain metrics (transaction volume, active addresses), block height, and fee rates in real time.
- **Trading Signals**: Generates Buy/Sell/Hold signals based on RSI (14-period).
- **Interactive Dashboard**: Visualizes price and RSI trends over the last 30 days using Chart.js.
- **Historical Data**: Displays a table of historical data, including price, RSI, transactions, and unique addresses.
- **Responsive Design**: Built with Tailwind CSS for a clean, modern UI that works on desktop and mobile.
- **WebSocket Updates**: Uses Flask-SocketIO to push live updates to the frontend every 120 seconds.
- **Error Handling**: Implements caching to handle API rate limits and displays user-friendly error messages when data fetching fails.

---

## Tech Stack

- **Backend**: 
  - Flask (Python) for the server
  - Flask-SocketIO for real-time WebSocket communication
  - Pandas for data processing
  - Requests for API calls
- **Frontend**:
  - Vue.js (Vue 3) for the single-page application
  - Vue Router for navigation
  - Chart.js for data visualization
  - Tailwind CSS for styling
  - Socket.IO-client for WebSocket communication
- **APIs**:
  - CoinGecko (price data)
  - Blockchain.com (on-chain data: transactions, unique addresses)
  - mempool.space (block height, fee rates)
- **Deployment**: COMING SOON!

---

## Project Structure

```
bitcoin-onchain-signals/
├── backend/
│   ├── app.py                 # Flask-SocketIO server
│   ├── data_fetcher.py        # Logic for fetching and processing data
│   ├── requirements.txt       # Python dependencies
├── frontend/
│   ├── btc-onchain-signals-frontend/
│   │   ├── src/
│   │   │   ├── assets/        # Static assets (e.g., images)
│   │   │   ├── components/    # Vue components
│   │   │   ├── views/         # Vue pages (Dashboard.vue, About.vue)
│   │   │   ├── services/      # WebSocket service (socket.js)
│   │   │   ├── App.vue        # Main Vue app component
│   │   │   └── main.js        # Entry point
│   │   ├── public/            # Static files
│   │   ├── package.json       # Node.js dependencies and scripts
│   │   └── vite.config.js     # Vite configuration
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

---

## Known Issues

This project is a work-in-progress, and there are a few issues that are being addressed:

- **Historical Data Consistency**: The historical data table may show repeated values for transaction volume and unique addresses due to timestamp misalignment between APIs. A fix is in progress to better align the data.


---

## Setup and Installation

Follow these steps to set up and run the project locally.

### Prerequisites

- **Python 3.8+**: For the backend.
- **Node.js 18+**: For the frontend.
- **npm**: For managing frontend dependencies.
- **Git**: For cloning the repository.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/bitcoin-onchain-signals.git
cd bitcoin-onchain-signals
```

Replace `your-username` with your GitHub username.

### 2. Set Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5000`.

### 3. Set Up the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend/btc-onchain-signals-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:5173` (or another port if specified by Vite).

### 4. Access the App

- Open your browser and go to `http://localhost:5173`.
- You should see the Dashboard page with real-time Bitcoin data and trading signals.

---

## Usage

- **Dashboard**: The main page displays real-time Bitcoin metrics, including price, 24-hour price change, transaction volume, active addresses, RSI, and a trading signal (Buy/Sell/Hold). It also includes a chart showing price and RSI trends over the last 30 days, and a table of historical data.
- **About Page**: Provides information about the project and its purpose.
- **Error Handling**: If the app fails to fetch data due to API rate limits, it will display a message like “Rate limit exceeded. Showing cached data.” A refresh may be required if navigating between pages causes issues (see [Known Issues](#known-issues)).

---

## Deployment

The app can be deployed to various platforms. Here’s an example for deploying on Render:

### Deploy on Render

1. **Backend (Web Service)**:
   - Create a new Web Service on Render.
   - Connect your GitHub repository (backend folder).
   - Set the runtime to Python and the start command to `python app.py`.
   - Choose the free tier plan.
   - Deploy to get a URL (e.g., `your-backend.onrender.com`).
2. **Frontend (Static Site)**:
   - Create a new Static Site on Render.
   - Connect your GitHub repository (frontend folder).
   - Set the build command to `npm run build` and publish directory to `dist`.
   - Choose the free tier plan.
   - Deploy to get a URL (e.g., `your-frontend.onrender.com`).
3. **Update Frontend Configuration**:
   - Update the frontend to use the backend URL for WebSocket connections (e.g., in `src/services/socket.js`).

---

## API Rate Limiting and Caching

The app fetches data from CoinGecko, Blockchain.com, and mempool.space. To handle API rate limits (especially CoinGecko’s 10-50 requests/minute limit), the backend implements caching:
- Data is fetched every 120 seconds.
- If an API call fails due to rate limiting, the backend serves cached data and logs the error.
- The frontend displays a message like “Rate limit exceeded. Showing cached data.” when cached data is used.

---

## Future Improvements

- **Fix Navigation Bug**: Resolve the WebSocket reconnection issue when navigating between pages.
- **Improve Historical Data**: Align on-chain data timestamps with price data for more accurate historical metrics.
- **Add Sorting to Historical Data Table**: Allow users to sort the table by columns like Timestamp or Price.
- **Implement Backtesting**: Add a feature to simulate trades based on historical signals.
- **Optimize API Calls**: Explore paid API plans or alternative data sources to avoid rate limits.
- **Add Authentication**: Secure the app with user authentication for personalized features.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


## Acknowledgements

- **CoinGecko API**: For providing Bitcoin price data.
- **Blockchain.com API**: For on-chain metrics like transaction volume and unique addresses.
- **mempool.space API**: For block height and fee rate data.
- **Vue.js and Flask Communities**: For their amazing frameworks and documentation.
- **Chart.js and Tailwind CSS**: For making data visualization and styling easy.
