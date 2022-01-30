# FinanceTracker
This is the API for a budgeting app I would like to create, possible features are talked about at the bottom of the page. Possible names for the app are BudgetApp or SafeBets.

## How to setup the API
still need to write this...

## How to use the API
still need to write this...

## Currently Working on
### Finance tracker API Tree
not final, just some thoughts
```
/
+--user
|  +--login
|  +--logout
|  +--refresh_key
+--stocks
+--stock
|  +--add_stock
|  +--remove_stock
|  +--update_stock
|  +--get_stock_info
+--cryptos
+--crypto
|  +--add_crypto
|  +--remove_crypto
|  +--update_crypto
|  +--get_crypto_info
```
### FinanceTrackingAPI features to implement
1. use Flask-JWT-extended to authenticate API users
    1. give users ability to login, logout using token based access system
    2. users register their info into the database and when they login they are given an access and refresh key to access the api
2. create user model and link to stock and crypto db models
3. update stock model
4. add crypto model and views in API

## Budget App Features (Will work on in the future)
I plan on creating this app in dart using flutter, but am trying to figure out how the backend would work first, then will learn how to create the frontend.
### Budgeting Features to Implement
1. given monthly income and amount to save/spend in different catagories (food, shopping, rent, etc...) it will show you how much you have to spend each month and where/what to spend it on
    1. manually enter transactions in different accounts
    2. set recurring payments, deposits, and transcations
    3. add different bank/savings/stock/crypto accounts to track different account all in one app
    4. ability to jump ahead month by month to see how much money you will have saved up
2. ability to add custom spending categories
3. customize amounts to spend/save by exact amounts or changing %
4. display a pie/bar chart on home screen to show current monthly spending
5. can view previoous monthly/yearly spending in pie/bar chart form
6. ability to compare month-to-month and year-to-year spending

### Saving Features to Implement
1. ability to track investments from multiple accounts in one app
    1. manually add investments in stocks and crypto to a different number of accounts
    2. can view accounts individually or with an all account view
    3. see a graph showing total/individual account growth
2. set saving/investing goals and *earn badges* (maybe)
3. ability to add savings accounts, but recommend investing and talk about investing/stock growth
4. long term investment calculator
    1. based on initial and/or recurring investments and estimated growth per year show overall growth over a period of time on a graph
5. create stock and crypto watch lists

### Long Term Features
1. use banking apis to auto import user transcations or investments from accounts (for now it will just be manual)
2. back up data to web services like google drive
3. create paper trading accounts
