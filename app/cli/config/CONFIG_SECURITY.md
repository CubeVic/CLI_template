# 🔐 Secure Configuration with Pydantic

This project uses Pydantic models and SecretStr types to safely handle configuration values, including sensitive data like API keys, tokens, and passwords.

## Why Use SecretStr?

`SecretStr` ensures:

- Secrets are never accidentally printed or logged
- You must explicitly retrieve their value when needed
- Output like print() or log.debug() will mask the value

## 📄 Example Configuration

### config.toml

```toml
[env]
APP_ENV = "development"
```

### .env

```sh
API_TOKEN=super-secret-token
```

### config.py

```python
from pydantic import BaseModel, SecretStr

class EnvSettings(BaseModel):
    API_TOKEN: SecretStr
    APP_ENV: str = "production"
```

## 🛡 Safe Output Example

```python
from app.config import get_config
from rich.pretty import pprint

config = get_config()

# This is safe – token will be masked
pprint(config.model_dump())
```

Output:

```json
{
    'env': {
        'API_TOKEN': '**********',
        'APP_ENV': 'development'
    }
}
```

## ⚠️ Accessing Secrets

You must intentionally unwrap secrets using `.get_secret_value()`:

```python
token = config.env.API_TOKEN.get_secret_value()
```

Use this only when sending to an API or injecting into headers — never log or print the raw value.

## 🚫 Unsafe Usage (Don’t Do This)

```python
print(config.env.API_TOKEN.get_secret_value())  # ❌ Don't print raw secrets
```

## 🔐 Best Practices

| Practice                  | Recommendation                                 |
| ------------------------- | ---------------------------------------------- |
| Use `.env` for secrets    | Do not hardcode secrets in source files        |
| Use `SecretStr` in models | Ensures secrets are masked when logged/printed |
| Use `.get_secret_value()` | Only when you need the raw value               |
| Don't log secrets         | Avoid printing tokens, keys, passwords         |
| Validate early            | Let Pydantic fail fast if config is invalid    |

## 🧪 Optional: CI Dump with Secrets (Debug Only)

If you really need raw values (e.g., in CI pipelines):

```python
config.model_dump(mode="json", include_secrets=True)
```

> ⚠️ Use with extreme caution — this bypasses the masking behavior.

## 🔚 Summary

Use `SecretStr` and proper config modeling to safely manage sensitive data in your CLI tool.
