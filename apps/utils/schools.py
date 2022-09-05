from apps.schools.models import DocumentContent


def save_document_content(documents, content):
    """Save the files of the content in the database"""
    if documents:
        objs = []
        for document in documents:
            objs.append(DocumentContent(**document, content=content))
        DocumentContent.objects.bulk_create(objs)
    return content
