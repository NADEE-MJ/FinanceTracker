# Delete User

Delete user from database

**URL**: `/user/delete`

**Method**: `DELETE`

**Auth required**: YES - FRESH

## Json Data

    None

## Success Response

**Code**: `200 - OK`

**Content example**:

```json
{
    "message": "user deleted successfully"
}
```

## Error Responses

**Condition**: User was already deleted from database.

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "user does not exist"
}
```
