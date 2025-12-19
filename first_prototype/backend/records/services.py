def scale_nutrients(base, serving_g: float, amount_g: float):
    """
    base: dict with keys kcal/carb_g/protein_g/fat_g/sugar_g/sodium_mg
    serving_g: 기준 제공량(g)
    amount_g: 섭취량(g)
    """
    if serving_g <= 0:
        serving_g = 100.0
    ratio = amount_g / serving_g

    def r(x):
        return round(float(x) * ratio, 2)

    return {
        "kcal": r(base.get("kcal", 0)),
        "carb_g": r(base.get("carb_g", 0)),
        "protein_g": r(base.get("protein_g", 0)),
        "fat_g": r(base.get("fat_g", 0)),
        "sugar_g": r(base.get("sugar_g", 0)),
        "sodium_mg": r(base.get("sodium_mg", 0)),
    }


def estimate_exercise_kcal(minutes: int, intensity: str, weight_kg: float = 60.0):
    """
    매우 단순 추정치(프로토타입). 이후 MET 기반으로 교체 가능.
    """
    if minutes <= 0:
        return 0.0

    # 강도 계수(프로토타입)
    factor = {"low": 4.0, "mid": 6.0, "high": 8.5}.get(intensity, 6.0)
    # 분당 소모량 추정: (계수 * 체중) / 60 형태의 단순식
    kcal = (factor * weight_kg) * (minutes / 60.0)
    return round(kcal, 1)
