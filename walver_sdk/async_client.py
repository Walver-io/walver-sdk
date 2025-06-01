import httpx
from httpx import HTTPStatusError
from dotenv import load_dotenv
import os
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from .models import(
    Folder,
    CustomField,
    ApiKey,
    VerificationResult,
    CreateVerificationRequest,
    CreateFolderRequest,
    DeleteFolderResponse,
    CreateApiKeyRequest,
    DeleteApiKeyResponse,
    CreateVerificationResponse
)

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
        custom_fields: Optional[List[CustomField]] = None
    ) -> Folder:
        """Create a new folder for organizing verifications.
        Args:
            name: The name of the folder.
            description: The description of the folder.
            custom_fields: The custom fields of the folder.
        Returns:
            Folder
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        data = CreateFolderRequest(
            name=name,
            description=description,
            custom_fields=custom_fields or []
        )

        response = await self._post("/creator/folders", data.model_dump())
        return Folder(**response)

    async def get_folders(self) -> List[Folder]:
        """Get all folders for the authenticated creator.
        Returns:
            List[Folder]
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        response = await self._get("/creator/folders")
        return [Folder(**folder) for folder in response]

    async def get_folder(self, folder_id: str) -> Folder:
        """Get a specific folder by ID.
        Args:
            folder_id: The ID of the folder.
        Returns:
            Folder
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        result = await self._get(f"/creator/folders/{folder_id}")
        return Folder(**result)

    async def get_folder_verifications(self, folder_id: str) -> List[VerificationResult]:
        """Get all verifications for a specific folder.
        Args:
            folder_id: The ID of the folder.
        Returns:
            List[VerificationResult]
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        result = await self._get(f"/creator/folders/{folder_id}/verifications")
        return [VerificationResult(**verification) for verification in result]

    async def delete_folder(self, folder_id: str) -> DeleteFolderResponse:
        """Delete a folder.
        Args:
            folder_id: The ID of the folder to delete.
        Returns:
            DeleteFolderResponse
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        result = await self._delete(f"/creator/folders/{folder_id}")
        return DeleteFolderResponse(**result)

    async def create_api_key(
        self,
        name: str,
        description: Optional[str] = None
    ) -> ApiKey:
        """Create a new API key.
        Args:
            name: The name of the API key.
            description: The description of the API key.
        Returns:
            ApiKey
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        data = CreateApiKeyRequest(
            name=name,
            description=description
        )
        result = await self._post("/creator/api-keys", data.model_dump())
        return ApiKey(**result)

    async def get_api_keys(self) -> List[ApiKey]:
        """Get all API keys for the authenticated creator. The api keys are trimmed for security reasons.
        Returns:
            A list of API keys.
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        result = await self._get("/creator/api-keys")
        return [ApiKey(**api_key) for api_key in result]

    async def delete_api_key(self, api_key_id: str) -> DeleteApiKeyResponse:
        """Delete an API key.
        Args:
            api_key_id: The ID of the API key to delete.
        Returns:
            DeleteApiKeyResponse
        Raises:
            HTTPStatusError: If the API returns an error.
        """
        result = await self._delete(f"/creator/api-keys/{api_key_id}")
        return DeleteApiKeyResponse(**result)

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
        custom_fields: Optional[List[CustomField]] = None,
        token_gate: bool = False,
        token_address: Optional[str] = None,
        token_amount: Optional[Union[int, float]] = None,
        is_nft: bool = False,
        force_email_verification: bool = False,
        force_telegram_verification: bool = False,
        force_twitter_verification: bool = False,
        force_telephone_verification: bool = False,
    ) -> CreateVerificationResponse:
        """Create a new verification link that can be shared with users.
        Args:
            id: The ID of the verification.
            service_name: The name of the service.
            chain: The chain of the verification.
            internal_id: The internal ID of the verification.
            webhook: The webhook of the verification.
            expiration: The expiration of the verification.
            secret: The secret of the verification.
            redirect_url: The redirect URL of the verification.
            one_time: Whether the verification is one-time.
            folder_id: The ID of the folder of the verification.
            custom_fields: The custom fields of the verification.
            token_gate: Whether the verification is a token gate.
            token_address: The address of the token for the token gate.
            token_amount: The amount of the token for the token gate.
            is_nft: Whether the verification is an NFT.
            force_email_verification: Whether the verification is a force email verification.
            force_telegram_verification: Whether the verification is a force telegram verification.
            force_twitter_verification: Whether the verification is a force twitter verification.
            force_telephone_verification: Whether the verification is a force telephone verification.
        Returns:
            CreateVerificationResponse
        Raises:
            ValueError: If the verification is invalid.
            HTTPStatusError: If the API returns an error.
        """

        if isinstance(expiration, datetime):
            expiration = expiration.isoformat()
            
        if not folder_id:
            if not webhook:
                raise ValueError("webhook is required when using folder_id")
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
            if "email" not in [field.type for field in custom_fields]:
                raise ValueError("custom_fields[email] is required when using force_email_verification")
        if force_telephone_verification:
            if not custom_fields:
                raise ValueError("custom_fields[telephone] is required when using force_telephone_verification")
            if "telephone" not in [field.type for field in custom_fields]:
                raise ValueError("custom_fields[telephone] is required when using force_telephone_verification")
            
        if force_telegram_verification:
            if not custom_fields:
                raise ValueError("custom_fields[telegram] is required when using force_telegram_verification")
            if "telegram" not in [field.type for field in custom_fields]:
                raise ValueError("custom_fields[telegram] is required when using force_telegram_verification")

        if force_twitter_verification:
            if not custom_fields:
                raise ValueError("custom_fields[twitter] is required when using force_twitter_verification")
            if "twitter" not in [field.type for field in custom_fields]:
                raise ValueError("custom_fields[twitter] is required when using force_twitter_verification")
            
        data = CreateVerificationRequest(
            id=id,
            service_name=service_name,
            chain=chain,
            internal_id=internal_id,
            webhook=webhook,
            expiration=expiration,
            secret=secret,
            redirect_url=redirect_url,
            one_time=one_time,
            folder_id=folder_id,
            custom_fields=custom_fields,
            token_gate=token_gate,
            token_address=token_address,
            token_amount=token_amount,
            is_nft=is_nft,
            force_email_verification=force_email_verification,
            force_telegram_verification=force_telegram_verification,
            force_twitter_verification=force_twitter_verification,
            force_telephone_verification=force_telephone_verification
        )

        # Remove None values
        data = {k: v for k, v in data.model_dump().items() if v not in [None, []]}
        try:
            result = await self._post("/new", data)
            return CreateVerificationResponse(**result)
        except HTTPStatusError as e:
            if e.response.status_code == 409:
                raise ValueError("ID for the verification already exists. Choose another ID.")
            else:
                raise e
