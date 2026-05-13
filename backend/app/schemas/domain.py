from typing import Literal

from pydantic import BaseModel, Field


RiskConcern = Literal["medical", "critical_illness", "life", "accident", "retirement", "education", "wealth"]


class CustomerProfile(BaseModel):
    name: str | None = None
    age: int = Field(ge=0, le=100)
    family_role: str = Field(description="家庭角色，例如：单身、夫妻、有娃、家庭经济支柱")
    annual_budget: int = Field(ge=0, description="年保费预算，单位：人民币元")
    existing_coverage: str = Field(default="", description="已有保障摘要")
    concerns: list[RiskConcern] = Field(default_factory=list)
    risk_preference: Literal["conservative", "balanced", "aggressive"] = "balanced"


class NeedAnalysisRequest(BaseModel):
    customer: CustomerProfile


class CoverageGap(BaseModel):
    category: str
    priority: Literal["high", "medium", "low"]
    reason: str
    next_question: str


class NeedAnalysisResponse(BaseModel):
    summary: str
    gaps: list[CoverageGap]
    compliance_notes: list[str]


class Product(BaseModel):
    id: str
    name: str
    category: str
    suitable_for: list[str]
    min_age: int
    max_age: int
    min_annual_premium: int
    highlights: list[str]
    cautions: list[str]


class ProductRecommendation(BaseModel):
    product: Product
    score: int
    reasons: list[str]
    cautions: list[str]


class RecommendationRequest(BaseModel):
    customer: CustomerProfile
    top_k: int = Field(default=3, ge=1, le=10)


class RecommendationResponse(BaseModel):
    recommendations: list[ProductRecommendation]
    disclaimer: str


class ObjectionRequest(BaseModel):
    objection: str
    customer: CustomerProfile | None = None


class ObjectionResponse(BaseModel):
    category: str
    response_script: list[str]
    follow_up_questions: list[str]
    compliance_notes: list[str]


class ChatRequest(BaseModel):
    message: str
    customer: CustomerProfile | None = None


class ChatResponse(BaseModel):
    answer: str
    suggested_actions: list[str]
    compliance_notes: list[str]
