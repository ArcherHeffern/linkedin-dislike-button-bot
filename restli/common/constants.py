from enum import Enum
from dataclasses import dataclass

OAUTH_BASE_URL = "https://www.linkedin.com/oauth/v2"
NON_VERSIONED_BASE_URL = "https://api.linkedin.com/v2"
VERSIONED_BASE_URL = "https://api.linkedin.com/rest"
WWW_BASE_URL = "https://www.linkedin.com"

@dataclass
class LinkedinAPIConstant:
    kind: str
    id: str
    typeName: str
    name: str

@dataclass
class WWWParams:
    CSRFToken: str
    li_at: str
    

class HEADERS(Enum):
    CONTENT_TYPE = "Content-Type"
    CONNECTION = "Connection"
    RESTLI_PROTOCOL_VERSION = "X-RestLi-Protocol_Version"
    RESTLI_METHOD = "X-RestLi-Method"
    LINKEDIN_VERSION = "LinkedIn-Version"
    AUTHORIZATION = "Authorization"
    USER_AGENT = "user-agent"
    CREATED_ENTITY_ID = "x-restli-id"


class CONTENT_TYPE(Enum):
    URL_ENCODED = "application/x-www-form-urlencoded"
    JSON = "application/json"
    MULTIPART_MIXED_WITH_BOUNDARY = (
        lambda boundary: f"multipart/mixed; boundary={boundary}"
    )


class HTTP_METHODS(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class RESTLI_METHODS(Enum):
    GET = "GET"
    BATCH_GET = "BATCH_GET"
    GET_ALL = "GET_ALL"
    FINDER = "FINDER"
    BATCH_FINDER = "BATCH_FINDER"
    CREATE = "CREATE"
    BATCH_CREATE = "BATCH_CREATE"
    UPDATE = "UPDATE"
    BATCH_UPDATE = "BATCH_UPDATE"
    PARTIAL_UPDATE = "PARTIAL_UPDATE"
    BATCH_PARTIAL_UPDATE = "BATCH_PARTIAL_UPDATE"
    DELETE = "DELETE"
    BATCH_DELETE = "BATCH_DELETE"
    ACTION = "ACTION"


RESTLI_METHOD_TO_HTTP_METHOD_MAP = {
    "GET": "GET",
    "BATCH_GET": "GET",
    "GET_ALL": "GET",
    "FINDER": "GET",
    "BATCH_FINDER": "GET",
    "UPDATE": "PUT",
    "BATCH_UPDATE": "PUT",
    "CREATE": "POST",
    "BATCH_CREATE": "POST",
    "PARTIAL_UPDATE": "POST",
    "BATCH_PARTIAL_UPDATE": "POST",
    "ACTION": "POST",
    "DELETE": "DELETE",
    "BATCH_DELETE": "DELETE",
}

# Rest.li special characters
LIST_PREFIX = "List("
LIST_SUFFIX = ")"
LIST_ITEM_SEP = ","
OBJ_PREFIX = "("
OBJ_SUFFIX = ")"
OBJ_KEY_VAL_SEP = ":"
OBJ_KEY_VAL_PAIR_SEP = ","
LEFT_BRACKET = "("
RIGHT_BRACKET = ")"
