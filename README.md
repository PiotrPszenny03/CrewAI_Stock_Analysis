# Multi-Agent AI Investment Committee (CrewAI)

🎯 Project Goal

The primary objective of this project was to build an automated, AI-driven financial analysis system using the Multi-Agent framework CrewAI.
Unlike standard script-based automation, this project utilizes autonomous AI agents that communicate, share context, and utilize external tools to simulate a real-world investment committee. It allows for:

Data-Driven Benchmarking: Fetching real-time stock market data and calculating historical volatility.

Macroeconomic Risk Assessment: Dynamically surfing the web for the latest news and potential regulatory or market risks.

Automated Synthesis: Synthesizing hard numerical data with qualitative risk reports to generate a final, actionable investment recommendation (BUY / HOLD / SELL) formatted in Markdown.

💻 Technologies & Tools
Python – The core programming language used for the backend logic.

CrewAI & LangChain – Orchestration frameworks used to define agent roles, goals, and sequential task execution.

Google Gemini 2.5 Flash API – The underlying Large Language Model (LLM) powering the agents' reasoning and decision-making capabilities.

yfinance – A custom Python tool built for the Data Analyst agent to fetch historical market data and calculate 3-year volatility.

DuckDuckGo Search – Integrated web search tool for the Risk Manager agent to perform real-time sentiment and news analysis.

python-dotenv – Used for secure environment variable management (protecting API keys).

📊 Key Features & Agent Architecture
1. Data Fetcher (Junior Analyst)
The Insight: I created a custom @tool that takes a stock ticker (e.g., AAPL, MSFT), connects to Yahoo Finance, retrieves 3 years of historical data, and mathematically calculates the annualized volatility.

Business Value: Ensures the decision-making process is grounded in hard, factual numbers rather than LLM hallucinations.

2. Risk Manager
The Insight: Equipped with web-search capabilities, this agent acts as a pessimist, specifically instructed to look for industry risks, lawsuits, or macroeconomic headwinds.

Business Value: Provides a qualitative counterweight to the raw data, ensuring "blind spots" are covered before any money is invested.

3. Chief Investment Officer (CIO)
The Insight: The final agent synthesizes the numerical report and the risk analysis to output a final Markdown recommendation.

Engineering Value: The system handles API Rate Limits (Google's 429 Resource Exhausted) by utilizing CrewAI's built-in max_rpm (Requests Per Minute) throttling mechanism, ensuring stable and continuous execution in a Free-Tier environment.

📂 Project Structure
The repository is organized as follows:

main.py - The core application script containing agent definitions, custom tools, and the task pipeline.

requirements.txt - List of necessary Python dependencies (specifically curated to avoid Pydantic/LangChain version conflicts).

.env.example - A template file showing how to structure the hidden environment variables.

README.md - Project documentation (This file).

🚀 How to Run
Clone this repository to your local machine.

It is highly recommended to use a virtual environment (Python 3.11 or 3.12) to avoid dependency conflicts:

python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

Create a .env file in the root directory and add your Google AI Studio API key:

GOOGLE_API_KEY="your_api_key_here"

Run the investment committee simulation:

python main.py

👤 Author
Piotr Pszenny
Aspiring Risk & Data Analyst
