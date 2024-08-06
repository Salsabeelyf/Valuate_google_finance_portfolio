# Google Finance Project

## About:

* Scrape price information from google finance, given some ticker and exchange from positions_input.csv input file

* Summerize portfolio valuation for an arbitrary number of positions

* Display Portfolio Summary in Table format

* Store Summary in Portfolio_Summary.csv output file


## Installing

#### Download the code from Github
#### Open CLI and Go to the code folder
#### Run the following command

```
pip install -r requirements.txt
```

## Running
To run the google finance scraper, open the 'positions_input.csv' file and add your stock data as follows:

![positions_input](<Screenshot from 2024-08-06 14-50-52.png>)

Save the file, then run the following command:

Pass the currency code you want the prices in as an argument

```
py main.py USD
```

## Output should look like this:

| Ticker   | Exchange   |   Quantity |   Price |   Market Value |   % Allocation |
|----------|------------|------------|---------|----------------|----------------|
| GOOGl    | NASDAQ     |        100 |  157.11 |       15711.00 |          90.99 |
| BNS      | TSE        |         30 |   44.86 |        1345.80 |           7.79 |
| SHOP     | TSE        |          4 |   52.69 |         210.76 |           1.22 |

Total portfolio value: USD 17,267.56

#### Also all the summary data should be stored in an output csv file called 'Portfolio_Summary.csv' as follows:

![portfolio_summary](<Screenshot from 2024-08-06 15-02-03.png>)