from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='webhook.log', level=logging.INFO, format='%(asctime)s %(message)s')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Parse the incoming JSON payload
        data = request.json
        if not data:
            return jsonify({"error": "Invalid payload"}), 400

        # Log the incoming request
        logging.info(f"Received webhook: {data}")

        # Process the payload (customize this for your use case)
        action = data.get("action")
        symbol = data.get("symbol")
        price = data.get("price")

        if not all([action, symbol, price]):
            return jsonify({"error": "Missing required fields"}), 400

        # Respond to the client
        return jsonify({"message": "Webhook received successfully"}), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
