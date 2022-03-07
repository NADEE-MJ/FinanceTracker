# FinanceTracker

## About

This is the API for a [budgeting app](docs/budgetapp.md) I would like to create.

## Setup

please see [setup](docs/setup.md) page

## Endpoints

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

This API uses [flask-jwt-extended](https://flask-jwt-extended.readthedocs.io/en/stable/) to authenticate users.

Please see [auth](docs/auth.md) page.
