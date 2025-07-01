Description of PR that completes issue here...

## Changes

- Item 1
- Item 2
- Item 3

## Requests / Responses

If this PR contains code that defines a new request/response, or changes an existing one, please put the JSON representations here.

**Request**

POST `/products` Creates a new product

```json
{
    "title": "Kite",
    "product_type_id": 1,
    "description": "Red. It flies high.",
    "quantity": 5
}
```

**Response**

HTTP/1.1 201 OK

```json
{
    "id": 54,
    "title": "Kite",
    "product_type_id": 1,
    "description": "Red. It flies high.",
    "quantity": 5
}
```

## Testing

Description of how to test code...

- [ ] Run migrations
- [ ] Run test suite
- [ ] Seed database


## Related Issues

- Fixes #85
- Fixes #22