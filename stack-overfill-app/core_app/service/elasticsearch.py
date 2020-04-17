import logging

from django.conf import settings
from elasticsearch import Elasticsearch, TransportError
from elasticsearch.helpers import streaming_bulk

FAILED_TO_LOAD_ERROR = 'Failed to load {}: {!r}'

logger = logging.getLogger(__name__)


# configure the client for elastic search
def get_client():
    return Elasticsearch(hosts=[{'host': settings.ES_HOST, 'port': settings.ES_PORT}])


# a function to bulk load existing question models into the ES.
def bulk_load(questions):
    all_ok = True
    es_questions = (q.as_elasticsearch_dict() for q in questions)

    for ok, result in streaming_bulk(
        get_client(),
        es_questions,
        index=settings.ES_INDEX,
        raise_on_error=False,
    ):
        if not ok:
            all_ok = False
            action, result = result.popitem()
            logger.error(FAILED_TO_LOAD_ERROR.format(result['_id'], result))

    return all_ok


# a function for querying the elasticsearch with a given query parameter
def search_for_questions(query):
    client = get_client()
    result = client.search(index=settings.ES_INDEX, body={
        'query': {
            'match': {
                'text': query
            }
        }
    })
    return (obj['_source'] for obj in result['hits']['hits'])


# a function to update the ES with a particular question model.
def upsert(question_model):
    client = get_client()
    question_dict = question_model.as_elasticsearch_dict()
    doc_type = question_dict['_type']
    del question_dict['_id']
    del question_dict['_type']
    response = client.update(
        settings.ES_INDEX,
        doc_type=doc_type,
        id=question_model.id,
        body={
            'doc': question_dict,
            'doc_as_upsert': True,
        }
    )
    return response