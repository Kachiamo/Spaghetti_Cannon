# Project Code Name Spaghetti Cannon
*Throw it at the wall and see what sticks!*

The goal of the is project is to provide a set of APIs for the analysis and comparison of trading strategies for stocks.

## How to run the project
- `docker-compose build`
- `docker-compose up`

## Dependencies
All dependencies are included as part of the Dockerfile, docker-compose file, and requirements file.
- Dockerfile
    - [python debian slim bookworm 3.9.18](https://hub.docker.com/layers/library/python/3.9-slim-bookworm/images/sha256-4342ac0e2b5d9c982e4d1f588d259b8a256b77e5979bef5ac557100d73fe27ec)
    - [postgresql](https://postgresql.org/)
    - [bash](https://www.gnu.org/software/bash/)
- requirements.txt
    - [bokeh 3.3.0](https://bokeh.org/)
    - [Django 4.2.6](https://www.djangoproject.com/)
    - [django-filter 23.5](https://github.com/carltongibson/django-filter/)
    - [djangorestframework 3.14.0](https://www.django-rest-framework.org/)
    - [hvplot 0.9.0](https://hvplot.holoviz.org/)
    - [pandas 2.1.1](https://pandas.pydata.org/)
    - [psycopg2-binary 2.9.9](https://www.psycopg.org/)
    - [scikit-learn 1.3.2](https://scikit-learn.org/)
    - [yfinance 0.2.31](https://github.com/ranaroussi/yfinance)
- docker-compose
    - [postgresql](https://postgresql.org/)


## Architecture

### Stocks
The list of stock data was saved in csv from [NASDAQ Screener](https://www.nasdaq.com/market-activity/stocks/screener) and saved to the local postgres database using Django migrations.  The list of stocks was saved locally in order to render stock choices in the browsable API drop downs.  The stock data contains symbol, name, country, ipo year, sector, and industry.  The stock data is searchable and sortable.

### Trading Strategies
Trading strategies were developed in external Jupyter Notebook files and then integrated into Django using classes.  The base TradingStrategy class allows for the generalization of various computation, features, and plotting.  Among the shared functionality are the computation of holdings, strategy position, stock profits, and strategy profits.  The class provides shared plotting functionality for the stock, buy/sell signals, holdings, and profit.  Adding a new trading strategy requires implementing the new class, selecting the features, and adding it to the list of strategies to be rendered in the UI.

### Back Testing
The API provides a quick and simple way to quickly back test and visualize a trading strategy.  The user needs to pick the stock symbol, the trading strategy, and the duration.  The api will render the stock close with buy/sell indicators of the duration, the returns from the stock and the strategy, and the holdings of the stock and the strategy.

### Trading Models (Machine Learning Models)
There is a postgres database table to store trading model data.  Trading models are a combination of a stock, a trading strategy, a machine learning model, and a duration.  This data structure and code module can be used to back test the strategy, the machine learning model, and the basic stock.  It will store the profit for all three back tests in addition to the accuracy, precision, and recall of the machine learning model.  The collection of trading models is searchable and sortable.

#### Future Improvements for Trading Models
- RabbitMQ with a cluster of machines to train machine learning models asynchronously.
- Calculate and store the Sharpe and Sortino ratios
- Add higher level analysis to the trading model results based in market cap, industry, and volume.


#### General Future Improvements
- Integrate time series data storage and portfolio management from [Athena](https://github.com/devinrosen/project1_group1/tree/main/webapp)
- User Accounts and Auth
- Trade triggers
- Email, push, and Slack notifications
- OpenAPI Spec
