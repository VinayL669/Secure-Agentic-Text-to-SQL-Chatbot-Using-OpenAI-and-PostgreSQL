import decimal

NUMBER_TYPES = (int, float, decimal.Decimal)


def summarize(rows: list[dict]) -> dict:
    if not rows:
        return {"row_count": 0}

    summary = {"row_count": len(rows)}

    for column in rows[0].keys():
        values = [
            row[column]
            for row in rows
            if isinstance(row[column], NUMBER_TYPES) and not isinstance(row[column], bool)
        ]
        if not values:
            continue
        summary[f"{column}_sum"] = sum(values)
        summary[f"{column}_avg"] = sum(values) / len(values)
        summary[f"{column}_min"] = min(values)
        summary[f"{column}_max"] = max(values)

    return summary