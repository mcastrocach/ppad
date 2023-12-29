# KrakenPythonMarcosRodrigo

This project is a tool for analyzing currency pairs on the Kraken cryptocurrency exchange. 

It fetches real-time price data for various currency pairs using the Kraken API and visualizes this data using the Plotly library. Additionally, it calculates technical analysis indicators such as the stochastic oscillator and its moving average, which can assist in trading decisions.

The project is written in Python and uses several libraries, including pandas for data manipulation, plotly for data visualization, krakenex for interacting with the Kraken API and streamlit for the web application functionality.

## Project Structure

The main code for the project is located in `main.py`, which imports and uses functions and classes defined in other modules. These modules include `graphs.py`, which contains the Graph class for creating candlestick charts and stochastic oscillators, and `front.py`, which contains the Front class for handling the user interface of the application.

The project also includes a `pyproject.toml` file that lists the Python packages required to run the project. The project can be run in a Docker container using the provided Dockerfile.

The project includes a `tests.py` file for unit testing and integration testing. The tests cover the initialization of the Front and Graph classes, the retrieval of currency pairs from the Kraken API, and the creation of Plotly graphs.

## How to Run the Project

To run the project, you need to have Python installed on your machine. You can then install the required packages using poetry:

poetry install

After installing the required packages, you can run the project using the following command:

streamlit run main.py

This will start the Streamlit app and open it in your web browser.

## Documentation

The project includes a docs folder that contains several text files providing more details about the project and its requirements.

## Authors

This project was created by Rodrigo de la Nuez Moraleda and Marcos Castro Cacho.
