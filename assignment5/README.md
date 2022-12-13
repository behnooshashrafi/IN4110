# Assignment 5: Strømpris
In this assignment we will implement attain information from a website and plot that information in Website of our own



### Installing dependencies
By having a requirement.txt we can insure that the correct dependencies, the libraries, their versions, etc is always correct and our code can be rerun and recreated at any time
Installing requirements.txt:

```python
  $ pip install -r requirements.txt
```


### fetch_day_price
Takes in the date for the day we want the data retrieved. If no data is given, today’s date is automatically considered.
The date structure is: 2022-4-2
Meaning if the day or/and month is less than 10 it is not going to be for example, 04. 
We add zero padding to fix that problem. 


### fetch_prices
Takes the date, number of days and locations to get the data.
If the date is not specified, today’s date is automatically considered and the duration of 7 days. We also add the differences between values from past hour, day and week as delta of previous hour, day and week.

### plot_proces
Returns an altair chart based on our data.

### app.py
Creates the foundation of the web.

### Due to exams the rest is not implemented.