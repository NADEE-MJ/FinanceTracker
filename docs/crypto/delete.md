# Delete A Crypto

Delete a crypto from a user's account

**URL**: `/crypto`

**Method**: `DELETE`

**Auth required**: YES - FRESH

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
    "message": "[unique crypto symbol] successfully deleted"
}
```

## Error Responses

**Condition**: User does not own crypto.

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "user does not own that crypto"
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
