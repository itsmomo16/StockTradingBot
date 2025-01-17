#include <curl/curl.h>

void placeTrade(const std::string& symbol, const std::string& action, double price) {
    CURL* curl = curl_easy_init();
    if (curl) {
        std::string url = "https://broker-api.com/place-order"; // Replace with broker's API URL
        std::string postData = "{\"symbol\":\"" + symbol + "\",\"action\":\"" + action + "\",\"price\":" + std::to_string(price) + "}";

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postData.c_str());
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, {"Content-Type: application/json"});
        
        CURLcode res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "Failed to place trade: " << curl_easy_strerror(res) << "\n";
        }
        curl_easy_cleanup(curl);
    }
}
