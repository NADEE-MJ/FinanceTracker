# Auth

## Fresh vs Stale

----------------------------------------------------------------

This API uses fresh and stale access tokens. When a user logs in it creates a fresh access token that expires after 30 minutes and a refresh token that expires after 30 days.

The refresh token can be used to create new access tokens however they will be stale access tokens.

Certain functions in the API require a fresh access token and are marked in the documentation. Please see the table below to see what each auth option means.

## Auth Required

----------------------------------------------------------------

| Auth Option | What to use in header |
| ----------- | ------------- |
| YES | FRESH or STALE access token |
| FRESH | only FRESH access token |
| REFRESH | refresh token |

## Example request with Auth

----------------------------------------------------------------

### Using Auth in a curl request example

```bash
    curl -H 'Authorization: Bearer [TOKEN]' -X [HTTP METHOD] '[URL]' -d 'PARAM=VALUE&PARAM=VALUE'
```
