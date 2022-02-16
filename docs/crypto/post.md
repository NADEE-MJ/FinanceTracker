# Add A Crypto

Add a crypto to the user's account

**URL**: `/crypto`

**Method**: `POST`

**Auth required**: YES - FRESH

## Json Data

```json
{
    "symbol": "[unique crypto symbol]",
    "number_of_coins": [Float],
    "cost_per_coin": [Float]
}
```

## Success Response

**Code**: `201 - Created`

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

**Condition**: User already owns that crypto.

**Code**: `400 - Bad Request`

**Content**:

```json
{
    "message": "user already owns that crypto, try a patch request to update number of coins or delete to remove it"
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
