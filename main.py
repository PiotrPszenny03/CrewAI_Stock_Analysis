import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
import yfinance as yf
from duckduckgo_search import DDGS

# --- 1. CONFIGURATION ---
load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found! Make sure you have a .env file with this key.")

# Using the native LLM engine from CrewAI, without LangChain!
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.environ.get("GOOGLE_API_KEY")
)

# --- 2. TOOLS (Native CrewAI) ---
@tool("Fetch_stock_data")
def fetch_stock_data(ticker_symbol: str) -> str:
    """Fetches historical data for the given stock ticker (e.g., AAPL) for 3 years and calculates volatility."""
    try:
        stock = yf.Ticker(ticker_symbol)
        history = stock.history(period="3y")
        history['Returns'] = history['Close'].pct_change()
        volatility = history['Returns'].std() * (252 ** 0.5)
        current_price = history['Close'].iloc[-1]
        return f"Data for {ticker_symbol}: Price: {current_price:.2f}, Volatility (3y): {volatility:.2%}"
    except Exception as e:
        return f"Error fetching data: {e}"

@tool("News_search")
def search_news(query: str) -> str:
    """Searches the internet for the latest news on a given topic."""
    try:
        # Using the pure DuckDuckGo library
        results = DDGS().text(query, max_results=3)
        return str(results)
    except Exception as e:
        return f"Search error: {e}"

# --- 3. AGENTS ---
analyst_agent = Agent(
    role='Senior Data Analyst',
    goal='Retrieve price and volatility data.',
    backstory="You trust only numbers. You report dry facts.",
    verbose=True,
    allow_delegation=False,
    tools=[fetch_stock_data],
    llm=gemini_llm  
)

risk_agent = Agent(
    role='Macroeconomic Risk Manager',
    goal='Find market threats in the news.',
    backstory="You are a pessimist. You look for market risks.",
    verbose=True,
    allow_delegation=False,
    tools=[search_news],
    llm=gemini_llm  
)

cio_agent = Agent(
    role='Chief Investment Officer',
    goal='Issue a recommendation based on the analyst’s data and the risk manager’s findings.',
    backstory="You make BUY/SELL/HOLD decisions based on your subordinates’ reports.",
    verbose=True,
    allow_delegation=False,
    llm=gemini_llm  
)

# --- 4. TASKS AND EXECUTION ---
def run_analysis(query: str):
    task_analysis = Task(
        description=f"Based on the user inquiry: '{query}'. Extract the companies involved. Use the tool to fetch stock data for them, and calculate their volatility.",
        expected_output="Report with price and volatility for the requested companies.",
        agent=analyst_agent
    )

    task_risk = Task(
        description=f"Based on the user inquiry: '{query}'. Search for news about risks in the involved sector or companies. Assess the analyst's report.",
        expected_output="Report on 3 main market risks.",
        agent=risk_agent
    )

    task_recommendation = Task(
        description=f"Read both reports. Write the final investment recommendation in Markdown format regarding the user inquiry: '{query}'.",
        expected_output="Markdown report with the final decision (BUY/SELL/HOLD) and justification.",
        agent=cio_agent
    )

    investment_crew = Crew(
        agents=[analyst_agent, risk_agent, cio_agent],
        tasks=[task_analysis, task_risk, task_recommendation],
        verbose=True,
        process=Process.sequential,
        max_rpm=4  # <-- NEW: Limit CrewAI to 4 requests per minute (Google’s limit is 5)
    )

    result = investment_crew.kickoff()
    return getattr(result, 'raw', str(result))

if __name__ == "__main__":
    print("### Starting ###")
    res = run_analysis("Fetch financial data for Apple and Microsoft for the last 3 years and calculate their volatility")
    print("\n\n### FINAL REPORT ###\n")
    print(res)