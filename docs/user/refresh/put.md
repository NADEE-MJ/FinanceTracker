# Refresh Access Token

Create a new access token from a refresh token. This can only create stale access tokens.

**URL**: `/user/refresh`

**Method**: `PUT`

**Auth required**: YES - REFRESH

## Json Data

    None

## Success Response

**Code** : `200 - OK`

**Content example**:

```json
{
    "access_token": "[stale access token string]"
}
```

## Error Responses

**Condition**: User was deleted from database.

**Code** : `404 - Not Found`

**Content** :

```json
{
    "message": "user does not exist"
}
```
