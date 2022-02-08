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
├── user --> methods=['POST', 'DELETE', 'PUT'] --> login, logout, and register users
│   ├── refresh --> methods=['PUT'] --> refresh access_token based on refresh token
├── stocks --> methods=['GET'] --> returns all stocks owned by a user
├── stock --> methods=['GET', 'POST', 'PATCH', 'DELETE'] --> get one stock, add a stock, update a stock, or delete a stock --> for a usr
├── cryptos --> methods=['GET'] --> returns all cryptos owned by a user
├── crypto --> methods=['GET', 'POST', 'PATCH', 'DELETE'] --> get one crypto, add a crypto, update a crypto, or delete a crypto --> for a user
```

### FinanceTrackingAPI features to implement

1. need to figure out how to remove old access_tokens from blocklist after they expire, maybe through flask-apscheduler
2. add super user or admin functionality to view all users and all user info, maybe through flask-praetorian
3. ability to delete users, or delete account
4. ability to change username, email, and password, maybe through flask-praetorian
5. block ips that try to send requests to often maybe using flask-limiter
6. switch from flask-jwt-extended to flask-praetorian
7. need to add bank/crypto/stock accounts
   1. for banks
      1. store transactional info
         1. amount
         2. name
         3. recurring + recurring date
         4. category
      2. bank account type savings/checking
      3. name
      4. get all account info together
   2. for crypto/stocks
      1. get all crypto and stocks info together
      2. get all crytpo info
      3. get all stock account info
8. store user category spending
9. user watchlist for stocks and crypto
