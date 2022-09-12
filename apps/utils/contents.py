from apps.contents.models import DocumentContent


def save_document_content(documents, content):
    print(documents, "SAVE DOCUMENTS")
    """Save the files of the content in the database"""
    if documents:
        objs = []
        for document in documents:
            objs.append(DocumentContent(**document, content=content))
        DocumentContent.objects.bulk_create(objs)
    return content


def update_document_content(documents, content):
    """Save the files of the content in the database"""
    print(documents, 'documents ')
    if documents:
        objs = []
        for document in documents:
            dc = DocumentContent.objects.get(file_name=document['file_name'], content=content)
            dc.file = document['file']
            dc.file_type = document['file_type']
            objs.append(dc)
        DocumentContent.objects.bulk_update(objs, ['file', 'file_type'])
    return content
