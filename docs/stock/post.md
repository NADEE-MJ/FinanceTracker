# Add A Stock

Add a stock to the user's account

**URL**: `/stock`

**Method**: `POST`

**Auth required**: YES - FRESH

## Json Data

```json
{
    "ticker": "[unique stock ticker]",
    "number_of_shares": [Float],
    "cost_per_share": [Float]
}
```

## Success Response

**Code**: `201 - Created`

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

**Condition**: User already owns that stock.

**Code**: `400 - Bad Request`

**Content**:

```json
{
    "message": "user already owns that stock, try a patch request to update number of shares or delete to remove it"
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
