from typing import List
from django.core.cache import cache
from notifier.models import Document

CACHE_KEY = "activity.session14.documents:list"


def get_cached_document_payload() -> List[dict]:
    def _query():
        documents = Document.objects.order_by("-uploaded_at")
        return [
            {
                "title": doc.title,
                "description": doc.description,
            }
            for doc in documents
        ]

    return cache.get_or_set(CACHE_KEY, _query, timeout=60)
