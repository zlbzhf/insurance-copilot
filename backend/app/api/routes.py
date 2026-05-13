from fastapi import APIRouter

from app.schemas.domain import (
    ChatRequest,
    ChatResponse,
    NeedAnalysisRequest,
    NeedAnalysisResponse,
    ObjectionRequest,
    ObjectionResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from app.services.knowledge import search_knowledge
from app.services.objection import respond_to_objection
from app.services.recommendation import analyze_needs, recommend_products

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/api/needs/analyze", response_model=NeedAnalysisResponse)
def analyze_needs_endpoint(request: NeedAnalysisRequest) -> NeedAnalysisResponse:
    return analyze_needs(request.customer)


@router.post("/api/products/recommend", response_model=RecommendationResponse)
def recommend_products_endpoint(request: RecommendationRequest) -> RecommendationResponse:
    return recommend_products(request.customer, request.top_k)


@router.post("/api/objections/respond", response_model=ObjectionResponse)
def objection_endpoint(request: ObjectionRequest) -> ObjectionResponse:
    return respond_to_objection(request.objection)


@router.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest) -> ChatResponse:
    compliance_notes = [
        "本助手仅提供销售辅助草稿，必须由持牌人员复核。",
        "涉及产品责任、费率和核保结论时，以正式条款和公司规则为准。",
    ]

    if request.customer:
        analysis = analyze_needs(request.customer)
        recs = recommend_products(request.customer, 2)
        product_lines = [
            f"- {item.product.name}：{'；'.join(item.reasons)}"
            for item in recs.recommendations
        ] or ["- 暂无完全匹配的样例产品，建议先补充预算、健康情况和已有保障。"]
        answer = "\n".join(
            [
                analysis.summary,
                "",
                "优先保障缺口：",
                *[f"- {gap.category}（{gap.priority}）：{gap.reason}" for gap in analysis.gaps],
                "",
                "可沟通的方案草案：",
                *product_lines,
                "",
                "知识库提示：",
                *(search_knowledge(request.message, 1) or ["未命中知识库，可补充公司 SOP 或条款资料。"]),
            ]
        )
        actions = ["补充客户健康告知和已有保单摘要", "将推荐草案交给合规/主管复核", "预约下一次需求确认沟通"]
    else:
        objection = respond_to_objection(request.message)
        answer = "\n".join(["建议话术：", *[f"- {line}" for line in objection.response_script]])
        actions = objection.follow_up_questions
        compliance_notes.extend(objection.compliance_notes)

    return ChatResponse(answer=answer, suggested_actions=actions, compliance_notes=compliance_notes)
