# Google Finance Project

## About:

* Scrape price information from google finance, given some ticker and exchange from positions_input.csv input file

* Summerize portfolio valuation for an arbitrary number of positions

* Display Portfolio Summary in Table format

* Store Summary in Portfolio_Summary.csv output file


## Installing

#### * Download the code from Github
#### * Open CLI, go to the code folder and run the following command

```
pip install -r requirements.txt
```



## Output should look like this:

|  Ticker   |  Exchange  |  Quantity  |  Price  |  Market Value  |  % Allocation  |
|  -------  |  -------  |  -------  |  -------  |  -------  |  -------  |
|  BNS      |  TSE      |    100    |   54.72   |  5472.00  |   56.64   |
|  GOOGL    |  NASDAQ   |     30    |  104.78   |  3143.40  |   32.54   |
|  SHOP     |  TSE      |     10    |   52.91   |   529.10  |    5.48   |
|  MSFT     |  NASDAQ   |      2    |  258.35   |   516.70  |    5.35   |

Total portfolio value: $9,661.20.