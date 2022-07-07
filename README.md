# ecs-github-actions
[![Deploy to AWS ECS](https://github.com/fipm/Thalassa_Regime_Classifier/actions/workflows/aws-ecs.yml/badge.svg?branch=master)](https://github.com/fipm/Thalassa_Regime_Classifier/actions/workflows/aws-ecs.yml/badge.svg?branch=master)


# Title
Thalassa trading tool: predicting the volatility of a cryptocurrency.

# Problem
Experience traders' perception of risk (volatility) will affect their decision-making process, and hence their expected returns if they do not accurately infer future risk.

# Solution
To help traders in their decision-making process, we build an application to predict in real-time a cryptocurrency's volatility and its regime.

# Technical details
- By using data engineering, we gather, clean, and deliver high-frequency data (the order book) to feed models in a pipeline.
- By using statistics, we process the data to a frequency of seconds and construct financial features from the order book data. We employ the method of principal component analysis as a feature reduction.- By using machine learning, we train, validate and test both a  time series model that uses as features the historical volatility and financial data to predict volatility in the next 30 seconds, and a gaussian mixture model to predict its regime. 
- By using cloud platforms, we create and deploy a webpage to inform traders about the expected volatility and its regime.

# Key technologies
Websocket, Pandas, Scikit-Learn, Streamlit, Doker, Google Cloud Platform.

# Install requirements
pip install -r requirements.txt

# To run the website locally
streamlit run Thalassa_Regime_Classifier/app.py