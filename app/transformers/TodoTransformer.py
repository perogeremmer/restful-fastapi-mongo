from app.transformers import UserTransformer


def transform(items):
    array = []

    for item in items:
        array.append(singleTransform(item))
    return array


def singleTransform(values):

    return {
        "id": str(values.id),
        "title": str(values.title),
        "description": str(values.description) if values.description else "",
        "owner_id": str(values.owner.id) if values.owner else "",
        "owner": UserTransformer.singleTransform(values.owner.fetch()) if values.owner else {}
    }
