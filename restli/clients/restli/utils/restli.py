from restli.clients.restli.utils.encoder import param_encode
from restli.clients.restli.utils.decoder import reduced_decode
from restli.common.constants import HEADERS
from typing import Dict, Any, Optional
import copy
from requests import Response


def get_created_entity_id(response: Response, decode: bool = False) -> Any:
    """
    Return the created entity id. This is present in the response header for
    a CREATE request. Can optionally decode the entity id value; otherwise this will
    return the reduced-encoded string.

    Args:
        response (Response): the response object
        decode (bool, optional): Flag whether to decode the id. Defaults to False.

    Returns:
        Any: The created entity id
    """
    reduced_encoded_entity_id = response.headers.get(
        HEADERS.CREATED_ENTITY_ID.value, None
    )
    if decode and reduced_encoded_entity_id is not None:
        return reduced_decode(reduced_encoded_entity_id)
    else:
        return reduced_encoded_entity_id


def encode_query_params_for_get_requests(query_params: Optional[Dict[str, Any]]) -> str:
    """Encodes query params for HTTP GET requests

    This wrapper function on top of encoder.paramEncode is needed specifically to handle the
    "fields" query parameter for field projections. Although Rest.li protocol version 2.0.0 should
    have supported a query param string like "?fields=List(id,firstName,lastName)" it still requires
    the Rest.li protocol version 1.0.0 format of "?fields=id,firstName,lastName". Thus, if "fields"
    is provided as a query parameter for HTTP GET requests, it should not be encoded like all the other
    parameters.

    Args:
        query_params (Dict[str,Any]): a map of query param names and their corresponding values. The query
        param values should not be encoded.

    Returns:
        str: The encoded query param string
    """
    FIELDS_PARAM = "fields"

    if query_params is None:
        return ""

    query_params_copy = copy.deepcopy(query_params)
    fields = (
        query_params_copy.pop(FIELDS_PARAM)
        if FIELDS_PARAM in query_params_copy.keys()
        else None
    )

    encoded_query_param_string = param_encode(query_params_copy)
    if fields:
        encoded_query_param_string = "&".join(
            [encoded_query_param_string, f"{FIELDS_PARAM}={fields}"]
        )

    return encoded_query_param_string
