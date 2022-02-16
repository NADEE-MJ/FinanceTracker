# Logout User

Used to logout an existing user, adds access token to the token blocklist.

**URL**: `/user`

**Method**: `DELETE`

**Auth required**: YES

## Json Data

    None

## Success Response

**Code**: `200 - OK`

**Content example**:

```json
{
    "message": "user logged out, access token revoked"
}
```
