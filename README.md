# Snowball API Generation [FastAPI](https://fastapi.tiangolo.com/) (this is just for now. dashboard incoming)

## Getting Started

### Virtual Environment

| Command | Task |
| --- | --- |
| `python -m venv venv` | create |
| `. venv/bin/activate` | activate |
| `deactivate` | deactivate |

### Dependencies

```sh
pip install -r requirements.txt
```

### Run Locally

```sh
hypercorn main:app --reload
```

### Test Locally
  
```sh
curl -X POST "http://127.0.0.1:8000/generate_key/?adminapikey=<adminApiKey>" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "jonDoe@example.com"}'
```

## Documentation

- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [Hypercorn](https://hypercorn.readthedocs.io/)
