# Login User

Used to login an existing user.

**URL**: `/user`

**Method**: `PUT`

**Auth required**: NO

## Json Data

```json
{
    "email": "[valid existing email address]",
    "password": "[valid user password]"
}
```

## Success Response

**Code**: `200 - OK`

**Content example**:

```json
{
    "message": "successfully logged in",
    "access_token": "[access token string]",
    "refresh_token": "[refresh token string]",
}
```

## Error Responses

**Condition**: Email not in database

**Code**: `404 - Not Found`

**Content**:

```json
{
    "message": "Email not found"
}
```

**Condition**: Incorrect password supplied

**Code**: `400 - Bad Request`

**Content**:

```json
{
    "message": "Password is incorrect."
}
```
