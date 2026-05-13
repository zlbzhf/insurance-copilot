from app.schemas.domain import ObjectionResponse

COMPLIANCE = [
    "话术应基于客户真实需求，不夸大收益或保障。",
    "涉及产品责任时必须回到正式条款和公司合规口径。",
]


def respond_to_objection(objection: str) -> ObjectionResponse:
    text = objection.strip().lower()

    if any(keyword in text for keyword in ["贵", "太贵", "预算", "没钱"]):
        category = "price"
        script = [
            "您觉得预算有压力是很正常的，保险配置确实要和现金流匹配。",
            "我们不一定一步到位，可以先把最影响家庭财务安全的风险排出来。",
            "如果把预算控制在您能接受的范围内，优先补齐医疗或家庭责任缺口，您会更愿意先了解哪一块？",
        ]
        questions = ["您比较舒服的年预算区间是多少？", "当前最担心的是医疗费、收入中断，还是家人责任？"]
    elif any(keyword in text for keyword in ["没必要", "用不上", "不需要"]):
        category = "necessity"
        script = [
            "我理解，保险最好是一辈子都用不上。",
            "我们可以先不谈买不买，只做一次保障缺口盘点，看看已有保障能覆盖哪些风险。",
            "如果盘点后发现已经够了，那反而可以避免重复配置。",
        ]
        questions = ["您现在已有社保或商业保险吗？", "如果发生大额医疗支出，您希望用哪部分资金应对？"]
    elif any(keyword in text for keyword in ["考虑", "再说", "回头"]):
        category = "delay"
        script = [
            "当然可以，保险决策不应该被催促。",
            "为了方便您考虑，我可以把今天讨论的风险点、可选方案和注意事项整理成一页。",
            "下次我们只确认两个问题：保障缺口是否存在，以及预算是否舒适。",
        ]
        questions = ["您主要想再比较哪方面：价格、责任、公司，还是必要性？", "我整理资料时需要重点标出哪些顾虑？"]
    else:
        category = "general"
        script = [
            "这个顾虑很重要，我们先把问题拆清楚，不急着下结论。",
            "保险配置的核心不是买某个产品，而是确认风险、预算和保障责任是否匹配。",
            "我建议先做一次保障缺口梳理，再决定是否需要进一步看方案。",
        ]
        questions = ["您这个顾虑背后最担心的是什么？", "如果只解决一个问题，您希望保险先解决哪件事？"]

    return ObjectionResponse(category=category, response_script=script, follow_up_questions=questions, compliance_notes=COMPLIANCE)
