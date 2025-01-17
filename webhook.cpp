#include "crow_all.h"
#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <mutex>
#include <queue>
#include <nlohmann/json.hpp> // For JSON parsing (https://github.com/nlohmann/json)

// Mutex for thread-safe logging and task queue
std::mutex logMutex;
std::mutex queueMutex;

// Task queue for asynchronous trade execution
std::queue<nlohmann::json> taskQueue;

// Function to log messages to a file
void logToFile(const std::string& message) {
    std::lock_guard<std::mutex> lock(logMutex);
    std::ofstream logFile("webhook_logs.txt", std::ios::app);
    if (logFile.is_open()) {
        logFile << message << std::endl;
    }
    logFile.close();
}

// Function to process trade tasks
void processTrades() {
    while (true) {
        nlohmann::json task;
        {
            std::lock_guard<std::mutex> lock(queueMutex);
            if (!taskQueue.empty()) {
                task = taskQueue.front();
                taskQueue.pop();
            }
        }

        if (!task.empty()) {
            // Simulate trade processing
            std::string action = task["action"];
            std::string symbol = task["symbol"];
            double price = task["price"];

            std::cout << "Processing trade: " << action << " " << symbol << " at " << price << std::endl;

            // Log trade execution
            logToFile("Trade executed: " + action + " " + symbol + " at " + std::to_string(price));
        }

        // Sleep briefly to avoid busy waiting
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

int main() {
    crow::SimpleApp app;

    // Start trade processing thread
    std::thread tradeProcessor(processTrades);
    tradeProcessor.detach();

    // Define the webhook route
    CROW_ROUTE(app, "/webhook").methods("POST"_method)([](const crow::request& req) {
        try {
            // Parse incoming JSON
            auto json = nlohmann::json::parse(req.body);

            // Validate required fields
            if (!json.contains("action") || !json.contains("symbol") || !json.contains("price")) {
                return crow::response(400, "Missing required fields (action, symbol, price)");
            }

            std::string action = json["action"];
            std::string symbol = json["symbol"];
            double price = json["price"];

            // Log the incoming request
            logToFile("Received alert: " + action + " " + symbol + " at " + std::to_string(price));

            // Add task to the queue for asynchronous processing
            {
                std::lock_guard<std::mutex> lock(queueMutex);
                taskQueue.push(json);
            }

            return crow::response(200, "Alert received and queued for processing");
        } catch (const std::exception& e) {
            // Handle JSON parsing or other errors
            std::string errorMsg = "Error processing webhook: ";
            errorMsg += e.what();
            logToFile(errorMsg);
            return crow::response(500, errorMsg);
        }
    });

    // Start the server
    std::cout << "Webhook listener running on port 8080..." << std::endl;
    app.port(8080).multithreaded().run();

    return 0;
}
