# StockTradingBot
algorithmic stock trading bot using any tradingview indicator of choice; trades automated using webhook alerts and a c++ script

1. choose an indicator
   - using a custom indicator i made through tradingview's pinescript, code is in pinescript file
2. understanding the workflow
   - Webhook Alerts: TradingView sends HTTP POST requests to a specified URL when an alert is triggered.
   - C++ Script: The script listens for these webhook alerts, parses them, and sends trading instructions to TradingView's API (or other trading APIs).
   - Trading Execution: Use TradingView's paper trading integration or a broker's API to execute trades.
3. to set up webook alerts via tradingview
   - Create an indicator in TradingView and set up alerts.
   - Configure alerts to send webhook POST requests to a server you control.
   - Formatted alert as JSON:
   {
     "symbol": "{{ticker}}",
     "action": "buy",
     "price": "{{close}}",
     "time": "{{time}}"
   }
4. next we utilize a webhook listener, code can be found in webhook file (created using crow c++)
   FEATURES OF WEBHOOK
   Asynchronous Trade Processing:
      -Incoming alerts are added to a queue and processed in a separate thread.
      -This ensures the server remains responsive, even under heavy load.
   Logging:
      -All incoming alerts and trade executions are logged to webhook_logs.txt.
      -This helps with debugging and monitoring.
   Validation:
      -Ensures the incoming JSON contains the required fields (action, symbol, price).
      -Responds with a 400 Bad Request if validation fails.
   Error Handling:
      -Catches exceptions during JSON parsing or processing.
      -Logs errors and responds with a 500 Internal Server Error.
   Thread Safety:
      -Uses std::mutex to ensure thread-safe access to the log file and task queue.
5. Two pathways depending on whether we want to integrate brokerage API
   1. if using tradingview paper trading, we have to use browser automation tools like Selenium or Puppeteer to interact with TradingView's interface.
   2. Otherwise, we can use broker API; get a api key, we use the api key to obtain an access token; authentication involves sending a POST request to the /auth/oAuth/token endpoint; we can use the cURL library in c++ to get an access token, and create a script with the API, code is in file
6. deploy the script
   -host your webhook listener on a server (e.g., AWS, Heroku, or local machine with port forwarding).
   -ensure the webhook URL is accessible by TradingView.

SUMMARY FLOW
whats happening?

1. TradingView Alert Setup
   What Happens:
   
   You create an indicator or strategy in TradingView that generates buy/sell signals based on predefined conditions.
   Alerts are configured to send a webhook POST request to your webhook server when these conditions are met.
   The alert payload includes key information like the action (buy/sell), symbol, price, and other relevant data.
2. Webhook Server Receives the Alert
   What Happens:
   
   The webhook server listens for incoming POST requests at a specific endpoint (e.g., /webhook).
   When an alert is received, the server:
   Parses the JSON payload.
   Validates the data (e.g., ensures fields like action, symbol, and price are present).
   Logs the alert for monitoring/debugging.
3. Webhook Server Adds the Alert to a Queue
   What Happens:
   
   To avoid blocking the server, the webhook server places the alert into a task queue.
   This allows the server to immediately respond to TradingView with a success message (200 OK) while processing the trade asynchronously.
4. Trade Processing in a Separate Thread
   What Happens:
   
   A background thread continuously monitors the task queue for new alerts.
   When an alert is found:
   The thread extracts the trade details (e.g., action, symbol, price).
   It logs the trade and prepares to execute it via the Tradovate API.
5. Tradovate API Integration
   What Happens:
   
   The bot uses the Tradovate API to place the trade. This involves:
   Authenticating with Tradovate using an API key or OAuth token.
   Sending an HTTP POST request to Tradovate’s order placement endpoint with the trade details.
6. Trade Execution Logging
   What Happens:
   
   After receiving a response from the Tradovate API, the bot logs the result of the trade (success or failure).
   If the trade fails (e.g., due to insufficient funds or invalid data), the bot logs the error for troubleshooting.
