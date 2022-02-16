# Register User

Used to register a new user.

**URL**: `/user`

**Method**: `POST`

**Auth required**: NO

## Json Data

```json
{
    "email": "[valid unique email address]",
    "username": "[valid unique username]",
    "password1": "[valid matching password]",
    "password2": "[valid matching password]"
}
```

## Success Response

**Code**: `200 - OK`

**Content example**:

```json
{
    "message": "the user has been created"
}
```

## Error Responses

**Condition**: Email already in database

**Code**: `409 - Conflict`

**Content**:

```json
{
    "message": "Email is already in use."
}
```

**Condition**: Username already in database

**Code**: `409 - Conflict`

**Content**:

```json
{
    "message": "Username is already in use."
}
```

**Condition**: password1 and password2 are not matching

**Code**: `400 - Bad Request`

**Content**:

```json
{
    "message": "Passwords don't match!"
}
```

**Condition**: Username is too short

**Code**: `400 - Bad Request`

**Content**:

```json
{
    "message": "Username is too short."
}
```

**Condition**: Password is too short

**Code**: `400 - Bad Request`

**Content**:

```json
{
    "message": "Password is too short."
}
```

**Condition**: Email not valid

**Code**: `400 - Bad Request`

**Content**:

```json
{
    "message": "Email is invalid."
}
```
