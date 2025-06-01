from pydantic import BaseModel
from typing import Optional, Literal, List, Union, Dict, Any

class CustomField(BaseModel):
    id: str
    type: Literal["text", "email", "url", "twitter", "telegram", "discord", "number", "telephone", "date", "wallet"]
    name: str
    required: bool = False
    placeholder: Optional[str] = None
    createdAt: Optional[str] = None #Don't use this field

class CreateFolderRequest(BaseModel):
    name: str
    description: Optional[str] = None
    custom_fields: Optional[List[CustomField]] = None

class ApiKey(BaseModel):
    id: str
    key: str
    name: str
    description: Optional[str] = None
    created_at: str
    creator: str
    
class DeleteApiKeyResponse(BaseModel):
    success: bool
    message: str

class Verification(BaseModel):
    id: str
    webhook: Optional[str] = None
    secret: Optional[str] = None
    internal_id: Optional[str] = None
    expiration: Optional[str] = None
    created_at: str
    chain: str
    public_uuid: str
    redirect_url: Optional[str] = None
    one_time: bool = False
    used: bool = False
    service_name: str
    folder_id: str
    custom_fields: Optional[List[CustomField]] = None
    token_gate: bool = False
    token_address: Optional[str] = None
    token_amount: Optional[int] = None
    is_nft: bool = False
    force_email_verification: bool = False
    force_telegram_verification: bool = False
    force_twitter_verification: bool = False
    force_telephone_verification: bool = False

class VerificationResult(BaseModel):
    id: str
    name: str
    blockchain: str
    verification_id: str
    wallet_address: str
    message: str
    signature: Union[str, List[int]]
    timestamp: str
    custom_fields: Dict[str, Any]
    folder_id: Optional[str] = None
    verification_data: Verification
    

class Folder(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    creator: str
    created_at: str
    custom_fields: Optional[List[CustomField]] = None
    verifications: Optional[List[Verification]] = None
    verification_count: int = 0


class CreateApiKeyRequest(BaseModel):
    name: str
    description: Optional[str] = None


class DeleteFolderResponse(BaseModel):
    success: bool
    message: str

class CreateVerificationRequest(BaseModel):
    id: str
    internal_id: Optional[str] = None
    service_name: str
    chain: str
    expiration: Optional[str] = None
    webhook: Optional[str] = None
    secret: Optional[str] = None
    redirect_url: Optional[str] = None
    one_time: bool = False
    folder_id: Optional[str] = None
    custom_fields: Optional[List[CustomField]] = None
    force_email_verification: bool = False
    force_telegram_verification: bool = False
    force_twitter_verification: bool = False
    force_telephone_verification: bool = False
    token_gate: bool = False
    token_address: Optional[str] = None
    token_amount: Optional[Union[int, float]] = None
    is_nft: bool = False

class CreateVerificationResponse(BaseModel):
    verification_url: str
    
