user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "repositories": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["username", "repositories"],
    "additionalProperties": False
}