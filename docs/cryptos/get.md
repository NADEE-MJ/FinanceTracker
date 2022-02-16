# Retrieve All Cryptos

Get all cryptos owned by a user.

**URL**: `/cryptos`

**Method**: `GET`

**Auth required**: YES

## Json Data

    None

## Success Response

**Condition**: user owns no cryptos

**Code**: `200 - OK`

**Content example**:

```json
[]
```

**Condition**: user owns cryptos

**Code**: `200 - OK`

**Content example**:

```json
[
    {
        "id": [Integer],
        "symbol": "[unique crypto symbol]",
        "number_of_coins": [Float],
        "cost_per_coin": [Float],
    },
    {
        "id": [Integer],
        "symbol": "[unique crypto symbol]",
        "number_of_coins": [Float],
        "cost_per_coin": [Float],
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
