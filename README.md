# FinanceTracker

This is the API for a budgeting app I would like to create, possible features for the app are talked about at the bottom of the page. Possible names for the app are BudgetApp or SafeBets.

## How to set up the API

still need to write this...

## How to use the API

still need to write this...

## Currently Working on

### API Tree Diagram

(not final)

```
/ --> methods=['GET'] --> returns github page for this project
│── user --> methods=['POST', 'DELETE', 'PUT'] --> login, logout, and register users
│   │── refresh --> methods=['PUT'] --> refresh access_token based on refresh token
│── stocks --> methods=['GET'] --> returns all stocks owned by a user
│── stock --> methods=['GET', 'POST', 'PATCH', 'DELETE'] --> get one stock, add a stock, update a stock, or delete a stock --> for a usr
│── cryptos --> methods=['GET'] --> returns all cryptos owned by a user
│── crypto --> methods=['GET', 'POST', 'PATCH', 'DELETE'] --> get one crypto, add a crypto, update a crypto, or delete a crypto --> for a user
```

### FinanceTrackingAPI features to implement

1. need to figure out how to remove old access_tokens from blocklist after they expire, maybe through a super user command
2. add super user or admin functionality to view all users and all user info, maybe create a custom decorator
3. ability to delete users
4. ability to change username, email, and password

## Future Budget App Features

I plan on creating this app in dart using flutter, creating back end api now, will implement front-end later.

### Budgeting Features to Implement

1. given monthly income and amount to save/spend in different catagories (food, shopping, rent, etc...) it will show you how much you have to spend each month and where/what to spend it on
    1. manually enter transactions in different accounts
    2. set recurring payments, deposits, and transactions
    3. add different bank/savings/stock/crypto accounts to track different account all in one app
    4. ability to jump ahead month by month to see how much money you will have saved up
2. ability to add custom spending categories
3. customize amounts to spend/save by exact amounts or changing %
4. display a pie/bar chart on home screen to show current monthly spending
5. can view previous monthly/yearly spending in pie/bar chart form
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

1. use banking apis to auto import user transactions or investments from accounts (for now it will just be manual)
2. back up data to web services like google drive
3. create paper trading accounts
