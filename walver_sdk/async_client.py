import httpx
from dotenv import load_dotenv
import os
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

load_dotenv()

class AsyncWalver:
    def __init__(
        self,
        api_key: str = None, 
        base_url: str = "https://walver.io/",
        timeout: int = 10):
        """
        Initialize the AsyncClient
        Args:
            api_key: The API key to use for the client. If not provided, the client will use the API key from the environment variable WALVER_API_KEY.
            base_url: The base URL for the API. Defaults to "https://walver.io/api/".
            timeout: The timeout for the client. Defaults to 10 seconds.
        """
        if not api_key:
            api_key = os.getenv("WALVER_API_KEY")
            if not api_key:
                raise ValueError("API key is required. Either pass it as an argument or set the WALVER_API_KEY environment variable on .env file")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-API-Key": api_key}
        self.timeout = timeout

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url + path,
                params=params,
                headers=self.headers,
                timeout=self.timeout)
            response.raise_for_status()
            await client.aclose()

        return response.json()

    async def _post(self, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url + path,
                json=data,
                headers=self.headers,
                timeout=self.timeout)
            response.raise_for_status()
            await client.aclose()
        return response.json()
    
    async def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                self.base_url + path,
                params=params,
                headers=self.headers,
                timeout=self.timeout)
            response.raise_for_status()
            await client.aclose()
        return response.json()

    async def create_folder(
        self,
        name: str,
        description: Optional[str] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a new folder for organizing verifications."""
        data = {
            "name": name,
            "description": description,
            "custom_fields": custom_fields or []
        }
        return await self._post("/creator/folders", data)

    async def get_folders(self) -> List[Dict[str, Any]]:
        """Get all folders for the authenticated creator."""
        return await self._get("/creator/folders")

    async def get_folder(self, folder_id: str) -> Dict[str, Any]:
        """Get a specific folder by ID."""
        return await self._get(f"/creator/folders/{folder_id}")

    async def get_folder_verifications(self, folder_id: str) -> List[Dict[str, Any]]:
        """Get all verifications for a specific folder."""
        return await self._get(f"/creator/folders/{folder_id}/verifications")

    async def create_api_key(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new API key"""
        data = {
            "name": name,
            "description": description
        }
        return await self._post("/creator/api-keys", data)

    async def get_api_keys(self) -> List[Dict[str, Any]]:
        """Get all API keys for the authenticated creator. The api keys are trimmed for security"""
        return await self._get("/creator/api-keys")

    async def delete_api_key(self, api_key_id: str) -> None:
        """Delete an API key.
        Args:
            api_key_id: The ID of the API key to delete.
        """
        return await self._delete(f"/creator/api-keys/{api_key_id}")

    async def create_verification(
        self,
        id: str,
        service_name: str,
        chain: str,
        internal_id: Optional[str] = None,
        webhook: Optional[str] = None,
        expiration: Optional[Union[str, datetime]] = None,
        secret: Optional[str] = None,
        redirect_url: Optional[str] = None,
        one_time: bool = False,
        folder_id: Optional[str] = None,
        custom_fields: Optional[List[Dict[str, Any]]] = None,
        token_gate: bool = False,
        token_address: Optional[str] = None,
        token_amount: Optional[Union[int, float]] = None,
        is_nft: bool = False,
        force_email_verification: bool = False,
        force_telegram_verification: bool = False,
        force_twitter_verification: bool = False,
    ) -> Dict[str, Any]:
        """Create a new verification link that can be shared with users."""
        if isinstance(expiration, datetime):
            expiration = expiration.isoformat()

        data = {
            "id": id,
            "service_name": service_name,
            "chain": chain,
            "internal_id": internal_id,
            "webhook": webhook,
            "expiration": expiration,
            "secret": secret,
            "redirect_url": redirect_url,
            "one_time": one_time,
            "folder_id": folder_id,
            "custom_fields": custom_fields or [],
            "token_gate": token_gate,
            "token_address": token_address,
            "token_amount": token_amount,
            "is_nft": is_nft,
            "force_email_verification": force_email_verification,
            "force_telegram_verification": force_telegram_verification,
            "force_twitter_verification": force_twitter_verification
        }

        if webhook:
            if not secret:
                print("Warning: secret is highly recommended when using webhooks")
        if token_gate:
            if not token_address:
                raise ValueError("token_address is required when using token gate")
            if not token_amount:
                raise ValueError("token_amount is required when using token gate")
        if force_email_verification:
            if not custom_fields:
                raise ValueError("custom_fields[email] is required when using force_email_verification")
            if "email" not in [field["type"] for field in custom_fields]:
                raise ValueError("custom_fields[email] is required when using force_email_verification")
                
        if force_telegram_verification:
            if not custom_fields:
                raise ValueError("custom_fields[telegram] is required when using force_telegram_verification")
            if "telegram" not in [field["type"] for field in custom_fields]:
                raise ValueError("custom_fields[telegram] is required when using force_telegram_verification")

        if force_twitter_verification:
            if not custom_fields:
                raise ValueError("custom_fields[twitter] is required when using force_twitter_verification")
            if "twitter" not in [field["type"] for field in custom_fields]:
                raise ValueError("custom_fields[twitter] is required when using force_twitter_verification")

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        try:
            return await self._post("/new", data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                raise ValueError("ID for the verification already exists. Choose another ID.")
            else:
                raise e
