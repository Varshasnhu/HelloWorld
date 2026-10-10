def calculate_statistics(numbers):
    if numbers is None:
        raise ValueError("numbers cannot be None")

    if len(numbers) == 0:
        return {
            "total": 0,
            "count": 0,
            "average": 0,
            "maximum": None,
            "minimum": None,
            "positive": False,
        }

    total = 0
    count = 0
    maximum = numbers[0]
    minimum = numbers[0]

    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError("All values in the list must be numeric.")

        total += num
        count += 1

        if num > maximum:
            maximum = num
        if num < minimum:
            minimum = num

    average = total / count if count > 0 else 0
    positive = total > 0

    return {
        "total": total,
        "count": count,
        "average": average,
        "maximum": maximum,
        "minimum": minimum,
        "positive": positive,
    }


result = calculate_statistics([1, 2, 3, 4, 5])
print(result)
