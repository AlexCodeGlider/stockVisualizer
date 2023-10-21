# Stock Visualizer

Stock Visualizer is a Dash application designed to provide visualizations of stock information.

## Features

- **Dashboard Interface**: A central dashboard that allows users to navigate between different views.
- **Daily View**: Visualize stock data on a daily basis.
- **Intraday View**: Dive deep into intraday stock data.
- **Ticker View**: Get a quick glance at specific stock tickers.

## Getting Started

1. **Clone the Repository**:

```
git clone https://github.com/AlexCodeGlider/stockVisualizer.git
```

2. **Navigate to the Directory**:

```
cd stockVisualizer
```

3. **Set Up a Python 3.9 Virtual Environment**:
First, ensure you have Python 3.9 installed. Then, create a virtual environment using `venv`:

```
python3.9 -m venv venv_name
```
Replace `venv_name` with your desired name for the virtual environment. To activate the virtual environment:

- On Windows:
  ```
  .\venv_name\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv_name/bin/activate
  ```

4. **Install Required Packages**:
With the virtual environment activated, run:

```
pip install -r requirements.txt
```

5. **Create the dataset**:

```
python create_dataset.py
```

6. **Run the App**:

```
python index.py
```

7. Open a web browser and navigate to `http://127.0.0.1:8050/` to view the app.

## Usage

- **Dashboard**: The main interface of the app. Use the navigation bar to switch between different views.
- **Daily View**: Select a stock ticker and date range to visualize daily stock data.
- **Intraday View**: Choose a stock ticker and date to visualize intraday stock data.
- **Ticker View**: Enter a stock ticker to get a quick overview.

## Contributing

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

## License

This project is open-source and available under the [MIT License](LICENSE).
