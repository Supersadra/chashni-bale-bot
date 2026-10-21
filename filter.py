def filter_ingredients(foods:list, ingredients:list) -> list:
    return [
        food for food in foods
        if set(ingredients) <= set(food["ingredients"])
    ]

def filter_meal(foods:list, meal:str) -> list:
    if meal == "lunch":
        return [
            food for food in foods
            if food["meal"] != "شام"
        ]
    elif meal == "dinner":
        return [
            food for food in foods
            if food["meal"] != "ناهار"
        ]
    else:
        return [
            food for food in foods
            if food["meal"] == "شام و ناهار"
        ]  

def filter_time(foods:list, time:str) -> list:
    if time == "fast":
        return [
            food for food in foods
            if food["time"] == 1
        ]
    elif time == "normal":
        return [
            food for food in foods
            if food["time"] == 2
        ]
    else:
        return [
            food for food in foods
            if food["time"] == 3
        ]  

def filter_category(foods:list, category:str) -> list:
    if category == "fastfood":
        return [
            food for food in foods
            if food["category"] == "فست‌ فود"
        ]
    elif category == "pasta":
        return [
            food for food in foods
            if food["category"] == "ماکارونی و پاستا"
        ]
    elif category == "rice":
        return [
            food for food in foods
            if food["category"] == "برنجی"
        ]
    elif category == "stew":
        return [
            food for food in foods
            if food["category"] == "خورشت و خوراک"
        ]
    elif category == "soup":
        return [
            food for food in foods
            if food["category"] == "آش و سوپ"
        ]
    elif category == "bread":
        return [
            food for food in foods
            if food["category"] == "نانی ساده"
        ]
    elif category == "tilit":
        return [
            food for food in foods
            if food["category"] == "غذا های تیلیتی"
        ]
    else:
        return [
            food for food in foods
            if food["category"] == "غذا های سرد"
        ]  
