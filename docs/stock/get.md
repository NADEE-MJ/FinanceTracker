# Retrieve A Stock

Get a stock owned by a user.

**URL**: `/stock`

**Method**: `GET`

**Auth required**: YES

## Json Data

```json
{
    "ticker": "[unique stock ticker]"
}
```

## Success Response

**Code**: `200 - OK`

**Content example**:

```json
{
    "id": [Integer],
    "ticker": "[unique stock ticker]",
    "number_of_shares": [Float],
    "cost_per_share": [Float],
}
```

## Error Responses

**Condition**: User does not own that stock.

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "stock not found"
}
```

**Condition**: User was deleted from database.

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "user does not exist"
}
```
