# Retrieve A Crypto

Get a crypto owned by a user.

**URL**: `/crypto`

**Method**: `GET`

**Auth required**: YES

## Json Data

```json
{
    "symbol": "[unique crypto symbol]"
}
```

## Success Response

**Code**: `200 - OK`

**Content example**:

```json
{
    "id": [Integer],
    "symbol": "[unique crypto symbol]",
    "number_of_coins": [Float],
    "cost_per_coin": [Float],
}
```

## Error Responses

**Condition**: User does not own that crypto.

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "crypto not found"
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
