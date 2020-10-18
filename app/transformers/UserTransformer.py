def transform(items):
    array = []

    for item in items:
        array.append(singleTransform(item))
    return array


def singleTransform(values):
    return {
        "id": str(values.id),
        "name": values.name,
    }
