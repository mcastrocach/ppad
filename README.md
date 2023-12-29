# KrakenPythonMarcosRodrigo

This project serves as an analytical tool designed for examining currency pairs on the Kraken cryptocurrency exchange platform. The application retrieves up-to-date pricing information for a range of currency pairs through the Kraken API, presenting this data in a clear and interactive format. 

Furthermore, it computes key technical analysis indicators, including the stochastic oscillator and its moving average. These features are designed to support and enhance trading decision-making.

This project is developed in Python and leverages a variety of libraries to enhance its functionality. 

It utilizes pandas for data manipulation, plotly for dynamic data visualization, krakenex for seamless interaction with the Kraken API, and streamlit to provide the web application capabilities.

## Project Structure

The main file of our project is `main.py`. It uses functions and classes from other files. For example, `graphs.py` has the `class Graph`, which we use to make candlestick charts and stochastic oscillators. Another important file is `front.py`, which has the `class Front` for the user interface part of our app.

The project also has a `pyproject.toml` file that names all the Python packages required to run the project. The project can be executed in a Docker container. using the provided Dockerfile.

The project also includes a `tests.py` file for testing different parts of the project, using unit-testing and integration-testing. The tests cover (amongst other functionalities) the initialization of the Front and Graph classes, the retrieval of currency pairs from the Kraken API, and the creation of Plotly graphs.


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
