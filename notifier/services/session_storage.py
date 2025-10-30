from django.http import JsonResponse

def remember_last_document(request, document_title:str ) -> JsonResponse:
    request.session["last_document_title"] = document_title
    request.session.modified = True
    return JsonResponse({"stored": document_title})
