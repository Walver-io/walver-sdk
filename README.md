# Walver.io SDK

A Python SDK for interacting with the Walver API, providing both synchronous and asynchronous clients for creating and managing wallet verification links.

## Installation

```bash
pip install walver-sdk
```

## Quick Start

### Getting an API Key

Go to walver.io, register for an account and get an api key in the creator dashboard

### Using the Synchronous Client

```python
from walver_sdk import Walver

# Initialize the client
walver = Walver(api_key="your-api-key")

# Create a verification
verification = walver.create_verification(
    id="verification_123",
    service_name="My Service", #Users will see this
    chain="solana",
    custom_fields=[
        {
            "id": "email",
            "type": "email",
            "name": "Email Address",
            "required": True
        }
    ]
)

# Create a folder
folder = walver.create_folder(
    name="My Folder",
    description="A folder for organizing verifications",
    custom_fields=[
        {
            "id": "discord",
            "type": "discord",
            "name": "Discord Username",
            "required": True
        }
    ]
)

# Get all folders
folders = walver.get_folders()

# Get verifications in a folder
verifications = walver.get_folder_verifications(folder_id="folder_123")

# Create an API key
api_key = walver.create_api_key(
    name="My API Key",
    description="API key for production use"
)

# Get all API keys
api_keys = walver.get_api_keys()

# Delete an API key
walver.delete_api_key(api_key_id="the-api-key-id")
```

### Using the Asynchronous Client

```python
import asyncio
from walver_sdk import AsyncWalver

async def main():
    # Initialize the client
    walver = AsyncWalver(api_key="your-api-key")

    # Create a verification with token gating
    verification = await walver.create_verification(
        id="verification_123",
        service_name="My Service", #Users will see this
        chain="solana",
        token_gate=True,
        token_address="So11111111111111111111111111111111111111112",
        token_amount=1.0,
        force_email_verification=True,
        custom_fields=[
            {
                "id": "email",
                "type": "email",
                "name": "Email Address",
                "required": True
            }
        ]
    )

    # Create a folder
    folder = await walver.create_folder(
        name="My Folder",
        description="A folder for organizing verifications"
    )

    # Get all folders
    folders = await walver.get_folders()

    # Get verifications in a folder
    verifications = await walver.get_folder_verifications(folder_id="folder_123")

    # Create an API key
    api_key = await walver.create_api_key(
        name="My API Key",
        description="API key for production use"
    )

    # Get all API keys
    api_keys = await walver.get_api_keys()

    # Delete an API key
    await walver.delete_api_key(api_key_id="the-api-key-id")

# Run the async code
asyncio.run(main())
```

## Configuration

### API Key

You can provide the API key in two ways:

1. Pass it directly when initializing the client:
```python
walver = Walver(api_key="your-api-key")
```

2. Set it as an environment variable in your `.env` file:
```env
WALVER_API_KEY=your-api-key
```

### Base URL

By default, the client uses `https://walver.io/api/`. You can change this by passing the `base_url` parameter:

```python
walver = Walver(
    api_key="your-api-key",
    base_url="https://walver.io/our-next-url"
)
```

### Timeout

The default timeout is 10 seconds. You can change this by passing the `timeout` parameter:

```python
walver = Walver(
    api_key="your-api-key",
    timeout=30  # 30 seconds timeout
)
```

## Features

### Verification Creation

Create verifications with various options:

```python
verification = walver.create_verification(
    id="verification_123",
    service_name="My Service", #Users will see this
    chain="solana",
    webhook="https://your-webhook-url.com/webhook",
    secret="your-webhook-secret",
    redirect_url="https://your-redirect-url.com",
    one_time=True,
    force_telegram_verification=True,
    force_email_verification=True,
    custom_fields=[
        {
            "id": "email",
            "type": "email",
            "name": "Email Address",
            "required": True
        },
        {
            "id": "tg",
            "type": "telegram",
            "name": "Telegram Username",
            "required": True
        }
    ]
)
```

### Token Gating

Create verifications with token gating:

```python
verification = walver.create_verification(
    id="verification_123",
    service_name="My Service", #Users will see this
    chain="solana",
    token_gate=True,
    token_address="So11111111111111111111111111111111111111112",
    token_amount=1.0,
    is_nft=True  # Set to True for NFT verification
)
```

### Email Verification

Require email verification using OTP:

```python
verification = walver.create_verification(
    id="verification_123",
    service_name="My Service",
    chain="solana",
    force_email_verification=True,
    custom_fields=[
        {
            "id": "email",
            "type": "email",
            "name": "Email Address",
            "required": True
        }
    ]
)
```

## Error Handling

The client raises exceptions for various error conditions:

```python
try:
    verification = walver.create_verification(
        id="verification_123",
        service_name="My Service",
        chain="solana",
        token_gate=True  # Missing token_address and token_amount
    )
except ValueError as e:
    print(f"Validation error: {e}")
except requests.exceptions.RequestException as e:
    print(f"API error: {e}")
```

## Best Practices

1. **Webhook Security**: Always provide a secret when using webhooks:
```python
verification = walver.create_verification(
    webhook="https://your-webhook-url.com/webhook",
    secret="your-webhook-secret"
)
```

2. **Async Context Manager**: Use the async client with a context manager:
```python
async with AsyncWalver(api_key="your-api-key") as walver:
    verification = await walver.create_verification(...)
```

## License

MIT License
