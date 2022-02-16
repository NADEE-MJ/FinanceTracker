# Delete A Stock

Delete a stock from a user's account

**URL**: `/stock`

**Method**: `DELETE`

**Auth required**: YES - FRESH

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
    "message": "[unique stock ticker] successfully deleted"
}
```

## Error Responses

**Condition**: User does not own stock.

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "user does not own that stock"
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
