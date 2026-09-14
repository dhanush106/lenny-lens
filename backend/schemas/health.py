from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    status: str
    environment: str


class ReadinessResponse(BaseModel):
    status: str
    database: str
    llm_provider: str
    llm_model: str
    retrieval_mode: str
    detail: Optional[str] = None


class ProviderStatus(BaseModel):
    id: str
    label: str
    model: str
    selected: bool
    configured: bool


class RuntimeResponse(BaseModel):
    provider: str
    model: str
    retrieval_mode: str
    embedding_model: str
    environment: str
    providers: list[ProviderStatus]


class LLMConfigurationRequest(BaseModel):
    provider: str
    model: str
    api_key: str = ""


class ModelListRequest(BaseModel):
    provider: str
    api_key: str = ""
