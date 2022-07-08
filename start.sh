#!/bin/sh

mkdir -p ~/.streamlit/

# echo "\
# [general]\n\
# email = \"your-email@domain.com\"\n\
# " > ~/.streamlit/credentials.toml

# echo "\
# [server]\n\
# headless = true\n\
# enableCORS=false\n\
# port = 8501\n\
# " > ~/.streamlit/config.toml


# echo "-------------------------------------- Starting stream_data process in background"
# python Thalassa_Regime_Classifier/stream_data.py &

echo "-------------------------------------- Starting streamlit web server"
streamlit run Thalassa_Regime_Classifier/app.py --server.port=8501 --browser.serverAddress="0.0.0.0"
