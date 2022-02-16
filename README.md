# FinanceTracker

## About

----------------------------------

This is the API for a [budgeting app](docs/budgetapp.md) I would like to create.

## Setup

----------------------------------

please see [setup](docs/setup.md) page

## Endpoints

----------------------------------

| Endpoint | HTTP METHODS | WHAT IT DOES |
| -------- | ------------ | ------------ |
| `/` | [GET](/docs/get.md) | returns this github repo |
| `/user` | [POST](/docs/user/post.md), [PUT](/docs/user/put.md), [DELETE](/docs/user/delete.md) | register, login, and logout user |
| `/user/refresh` | [PUT](/docs/user/refresh/put.md) | refresh users access token |
| `/user/delete` | [DELETE](/docs/user/delete/delete.md) | delete user from database |
| `/stocks` | [GET](/docs/stock/get.md) | gets all stocks owned by a user |
| `/stock` | [GET](/docs/stock/get.md), [POST](/docs/stock/post.md), [PATCH](/docs/stock/patch.md), [DELETE](/docs/stock/delete.md) | view, add, update, and remove a stock |
| `/cryptos` | [GET](/docs/cryptos/get.md) | gets all cryptos owned by a user |
| `/crypto` | [GET](/docs/crypto/get.md), [POST](/docs/crypto/post.md), [PATCH](/docs/crypto/patch.md), [DELETE](/docs/crypto/delete.md) | view, add, update, and remove a crypto |

## Authentication

----------------------------------

Please see [auth](docs/auth.md) page.

## FinanceTrackingAPI features to implement

----------------------------------

1. add email validation to user registration
2. switch from flask-jwt-extended to flask-praetorian
3. add super user or admin functionality to view all users and all user info, maybe through flask-praetorian
4. ability to change username, email, and password, maybe through flask-praetorian
5. need to add bank/crypto/stock accounts
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
      2. get all crypto info
      3. get all stock account info
6. store user category spending
7. user watch list for stocks and crypto
