import json
from pathlib import Path

from app.schemas.domain import (
    CoverageGap,
    CustomerProfile,
    NeedAnalysisResponse,
    Product,
    ProductRecommendation,
    RecommendationResponse,
)

ROOT = Path(__file__).resolve().parents[3]
PRODUCTS_PATH = ROOT / "data" / "products.json"

DISCLAIMER = (
    "本推荐仅为销售辅助草案，不构成保险、投资、法律或税务建议；"
    "具体保障责任、费率、核保结论和除外责任以正式条款、投保规则和公司合规复核为准。"
)

CATEGORY_LABELS = {
    "medical": "医疗保障",
    "critical_illness": "重疾保障",
    "life": "寿险责任",
    "accident": "意外保障",
    "retirement": "养老规划",
    "education": "教育金规划",
    "wealth": "财富规划",
}


def load_products() -> list[Product]:
    data = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    return [Product.model_validate(item) for item in data]


def analyze_needs(customer: CustomerProfile) -> NeedAnalysisResponse:
    gaps: list[CoverageGap] = []
    existing = customer.existing_coverage.lower()

    if "medical" in customer.concerns or "医疗" not in existing:
        gaps.append(
            CoverageGap(
                category="医疗保障",
                priority="high",
                reason="医疗险通常是基础保障的第一层，用来应对大额住院医疗支出。",
                next_question="客户目前是否有社保？是否已有商业医疗险，免赔额和续保条件是什么？",
            )
        )

    if "家庭" in customer.family_role or "支柱" in customer.family_role or "life" in customer.concerns:
        gaps.append(
            CoverageGap(
                category="家庭责任保障",
                priority="high",
                reason="如果客户承担房贷、子女教育或赡养责任，寿险和重疾保障可降低家庭现金流中断风险。",
                next_question="客户每年家庭固定支出、负债余额和需要照顾的人分别是多少？",
            )
        )

    if "critical_illness" in customer.concerns and customer.annual_budget >= 3000:
        gaps.append(
            CoverageGap(
                category="重疾保障",
                priority="medium",
                reason="重疾险与医疗险不同，给付型责任可用于康复、收入损失和家庭开支。",
                next_question="客户更关注保额充足、缴费压力，还是保障病种和赔付次数？",
            )
        )

    if "accident" in customer.concerns or customer.annual_budget < 1000:
        gaps.append(
            CoverageGap(
                category="意外保障",
                priority="medium",
                reason="意外险保费较低，适合做基础补充，但不能替代疾病保障。",
                next_question="客户职业类别、通勤方式、是否经常差旅或运动？",
            )
        )

    if not gaps:
        gaps.append(
            CoverageGap(
                category="保障结构复核",
                priority="low",
                reason="客户已有一定保障，建议先复核保额、责任范围、等待期、免赔额和续保条件。",
                next_question="能否提供现有保单的险种、保额、保费和保障期限摘要？",
            )
        )

    return NeedAnalysisResponse(
        summary=f"{customer.age}岁客户，家庭角色为{customer.family_role}，年预算约{customer.annual_budget}元。建议先补齐高优先级保障缺口，再考虑长期储蓄型目标。",
        gaps=gaps,
        compliance_notes=[DISCLAIMER, "不得诱导客户隐瞒健康告知或退保换保。"],
    )


def recommend_products(customer: CustomerProfile, top_k: int = 3) -> RecommendationResponse:
    products = load_products()
    recommendations: list[ProductRecommendation] = []
    concerns = set(customer.concerns)

    for product in products:
        if not (product.min_age <= customer.age <= product.max_age):
            continue
        if customer.annual_budget < product.min_annual_premium:
            continue

        score = 0
        reasons: list[str] = []
        if product.category in concerns:
            score += 50
            reasons.append(f"客户明确关注{CATEGORY_LABELS.get(product.category, product.category)}。")
        if "家庭" in customer.family_role or "支柱" in customer.family_role:
            if "family" in product.suitable_for or "income_protection" in product.suitable_for:
                score += 25
                reasons.append("客户承担家庭责任，产品适合用于家庭现金流风险管理。")
        if customer.annual_budget <= 1000 and "budget_sensitive" in product.suitable_for:
            score += 20
            reasons.append("客户预算较敏感，适合先配置低门槛基础保障。")
        if product.min_annual_premium <= max(customer.annual_budget * 0.6, 1):
            score += 10
            reasons.append("预计保费在客户预算范围内，沟通压力较低。")

        if score > 0:
            recommendations.append(
                ProductRecommendation(
                    product=product,
                    score=score,
                    reasons=reasons or ["与客户基础情况存在一定匹配。"],
                    cautions=product.cautions,
                )
            )

    recommendations.sort(key=lambda item: item.score, reverse=True)
    return RecommendationResponse(recommendations=recommendations[:top_k], disclaimer=DISCLAIMER)
