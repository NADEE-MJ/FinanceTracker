# Retrieve All Stocks

Get all stocks owned by a user.

**URL**: `/stocks`

**Method**: `GET`

**Auth required**: YES

## Json Data

    None

## Success Response

**Condition**: user owns no stocks

**Code**: `200 - OK`

**Content example**:

```json
[]
```

**Condition**: user owns stocks

**Code**: `200 - OK`

**Content example**:

```json
[
    {
        "id": [Integer],
        "ticker": "[unique stock ticker]",
        "number_of_shares": [Float],
        "cost_per_share": [Float],
    },
    {
        "id": [Integer],
        "ticker": "[unique stock ticker]",
        "number_of_shares": [Float],
        "cost_per_share": [Float],
    },
    ...
]
```

## Error Responses

**Condition**: User was deleted from database.

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "user does not exist"
}
```
