import streamlit as st
from main import run_analysis

st.set_page_config(page_title="Investment Committee AI", page_icon="📈", layout="centered")

st.title("📈 Multi-Agent Investment Committee")
st.markdown("""
Welcome! This application uses **CrewAI** with 3 collaborating agents:
1. **Data Fetcher**: Fetches stock data and calculates volatility using `yfinance`.
2. **Risk Manager**: Searches for macroeconomic risks using `duckduckgo_search`.
3. **Chief Investment Officer**: Formulates the final investment recommendation.
""")

st.write("---")

query = st.text_input("Ask a question (e.g., 'Fetch financial data for Apple and Microsoft for the last 3 years and calculate their volatility'):")

if st.button("Run Analysis", type="primary"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("The AI Committee is deciding... (This may take 1-2 minutes, please be patient)"):
            try:
                result = run_analysis(query)
                st.success("The Committee has finished its work!")
                
                st.markdown("### 📄 Final CIO Recommendation")
                st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred during the analysis: {e}")
