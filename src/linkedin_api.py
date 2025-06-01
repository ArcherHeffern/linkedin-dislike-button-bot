import re
import string
from typing import Any, Optional
import requests
from pydantic import ValidationError
from models.linkedin_all_mail import Element, LinkedinMessageConversations, Message
from models.linkedin_mail_chain import LinkedinMailChain
from models.linkedin_user_info import LinkedinUserInfo
from models.mine import FsdProfileUrn
from restli.clients.restli.client import RestliClient
from restli.common.constants import LinkedinAPIConstant, WWWParams
from src.environment import ACCESS_TOKEN
from src.util import dprint


class LinkedinAPI:
  def __init__(self):
    self.restli_client = RestliClient()

  def get_user_info(self) -> Optional[Any]:
    if not ACCESS_TOKEN:
      dprint("ACCESS_TOKEN must exist for this API call. See README.md for instructions")
    response = self.restli_client.get(
        resource_path="/userinfo",
        access_token=ACCESS_TOKEN,
    )
    if not 200 <= response.status_code < 300:
      dprint(f"Not good: {response.status_code} while getting user info")
      return
    entity = response.entity
    try:
      return LinkedinUserInfo.model_validate(entity, strict=True)
    except ValidationError as e:
      dprint(f"Validation Error: {str(e)}")
      return 

  def get_linkedin_api_constants(self) -> Optional[list[LinkedinAPIConstant]]:
    """
    Makes call to 
    https://static.licdn.com/aero-v1/sc/h/1bgzy5d1ndwxe5u1rxfwa5uqq

    This returns javascript containing ids used for querying, for example, getting user mailbox. 

    This function fetches the javascript code, and parses out the variables
    """
    url = "https://static.licdn.com/aero-v1/sc/h/1bgzy5d1ndwxe5u1rxfwa5uqq"
    api_constants_response = requests.get(url)
    if api_constants_response.status_code != 200:
      return None
    matches = re.findall("Fa\\(!0,\\{ *kind: *\"([^\"]*)\", *id: *\"([^\"]*)\", *typeName: *\"([^\"]*)\", *name: *\"([^\"]*)\",?", api_constants_response.text, re.M)

    linkedin_api_constants: list[LinkedinAPIConstant] = []
    for match in matches:
      linkedin_api_constants.append(LinkedinAPIConstant(match[0], match[1], match[2], match[3]))
    return linkedin_api_constants

  def share_post(self, message: Message, www_params: WWWParams) -> bool:
    """
    Must call self.get_linkedin_messages_conversations() and provide messaging thread you would like to share post with
    """
    path_keys = {}
    query_params = {
      "action": "createMessage"
    }
    entity = {
      "message": {
        "body": {
          "attributes":[],
          "text":""
        },
        "renderContentUnions":[
          {
            "hostUrnData": {
              "hostUrn":"urn:li:fsd_update:(urn:li:activity:7334407318954000384,FEED_DETAIL,EMPTY,DEFAULT,false)","type":"FEED_UPDATE"
            }
          }
        ],
        "conversationUrn":"urn:li:msg_conversation:(urn:li:fsd_profile:ACoAAD1jIgEBHVxaTagUhtTrMNxn7U-nsVAsg1o,2-MTZmYzRjZjItNjA0My00YWZkLWI4ZmQtMGU1Y2M1Y2VlNDUzXzEwMA==)",
        "originToken":message.originToken,
      },
      "mailboxUrn":"urn:li:fsd_profile:ACoAAD1jIgEBHVxaTagUhtTrMNxn7U-nsVAsg1o",
      "trackingId":"ìû=\n´\u0006H^·¤ll",
      # "trackingId":f"ìû=\n{tracking_id}",
      "dedupeByClientGeneratedToken":False,
      "messageRequestContextByRecipient":[]
    }

    response = self.restli_client.create(
      resource_path="/voyager/api/voyagerMessagingDashMessengerMessages",
      entity=entity,
      access_token="",
      path_keys=path_keys,
      query_params=query_params,
      use_www=www_params,
    )

    if response.status_code < 200 or response.status_code > 299:
      dprint(f"Not good: {response.status_code} while forwarding post")
      return False
    return True
    # fetch("https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages?action=createMessage", {
    #   "headers": {
    #     "accept": "application/json",
    #     "csrf-token": "ajax:4348196725114241813",
    #     "x-restli-protocol-version": "2.0.0"
    #   },
    #   "body": "{\"message\":{\"body\":{\"attributes\":[],\"text\":\"\"},\"renderContentUnions\":[{\"hostUrnData\":{\"hostUrn\":\"urn:li:fsd_update:(urn:li:activity:7334407318954000384,FEED_DETAIL,EMPTY,DEFAULT,false)\",\"type\":\"FEED_UPDATE\"}}],\"conversationUrn\":\"urn:li:msg_conversation:(urn:li:fsd_profile:ACoAAD1jIgEBHVxaTagUhtTrMNxn7U-nsVAsg1o,2-MTZmYzRjZjItNjA0My00YWZkLWI4ZmQtMGU1Y2M1Y2VlNDUzXzEwMA==)\",\"originToken\":\"ecfb3d0a-b406-485e-93b7-8593a4906c6c\"},\"mailboxUrn\":\"urn:li:fsd_profile:ACoAAD1jIgEBHVxaTagUhtTrMNxn7U-nsVAsg1o\",\"trackingId\":\"ìû=\\n´\\u0006H^·¤ll\",\"dedupeByClientGeneratedToken\":false,\"messageRequestContextByRecipient\":[]}",
    #   "method": "POST",
    #   "mode": "cors",
    #   "credentials": "omit"
    # });
  
  def get_fsd_profile_urn(self, www_params: WWWParams):
    """
    Grep out first occurance of urn:li:fsd_profile:\\w* from https://www.linkedin.com/feed/

    Used in probably many places...like as MailUrn 
    """
    cookies = {
      "li_at": www_params.li_at, 
      "JSESSIONID": www_params.CSRFToken
    }
    headers = {
      "Csrf-Token": www_params.CSRFToken
    }
    feed_response = requests.get(
      "https://www.linkedin.com/feed/", 
      cookies=cookies, 
      headers=headers,
    )
    if not feed_response.ok:
      return None
    
    maybe_fsd_profile_urn_pattern = re.search("urn:li:fsd_profile:[^ &]*", feed_response.text) # Incomplete regex. Replace [^ &] with positive character group stating which characters CAN be used in an URN
    return maybe_fsd_profile_urn_pattern.group()
    
  def mark_message_as_read(self, messaging_thread_urn: str) -> bool:
    ...

  def get_single_messaging_thread(self, element: Element, www_params: WWWParams) -> Optional[LinkedinMailChain]:
    return self.__get_single_messaging_thread(element.entityUrn, www_params)

  def __get_single_messaging_thread(self, msg_converation_urn: str, www_params: WWWParams) -> Optional[LinkedinMailChain]:
    resource_path = "/voyager/api/voyagerMessagingGraphQL/graphql"
    path_keys = {}
    query_params = {
      "queryId": "messengerMessages.455dde239612d966346c1d1c4352f648", # TODO: What is this? 
      "variables": {
        "conversationUrn": str(msg_converation_urn)
      }
    }
    response = self.restli_client.get(
      resource_path=resource_path,
      access_token="",
      path_keys=path_keys,
      query_params=query_params,
      use_www=www_params,
    )
    if not 200 <= response.status_code < 300:
      dprint(f"Not good: {response.status_code} while getting single messaging thread")
      return

    entity = response.entity
    try:
      return LinkedinMailChain.model_validate(entity, strict=True)
    except ValidationError as e:
      dprint(f"Validation Error: {str(e)}")
      return 

  def get_linkedin_messages_conversations(self, www_params: WWWParams, linkedin_api_constants: list[LinkedinAPIConstant], fsd_profile_urn: FsdProfileUrn) -> Optional[LinkedinMessageConversations]:
    """Mail messages may be incomplete"""
    query_id = None
    for linkedin_api_constant in linkedin_api_constants:
      if linkedin_api_constant.name == "initial-sync-conversations" and linkedin_api_constant.kind == "query":
        query_id = linkedin_api_constant.id
        break
    if query_id is None:
      dprint("Could not find linkedin api constant needed for getting conversations")
      return
    return self.__get_linkedin_messages_conversations(www_params, query_id, fsd_profile_urn)

  def __get_linkedin_messages_conversations(self, www_params: WWWParams, query_id: str, fsd_profile_urn: FsdProfileUrn) -> Optional[LinkedinMessageConversations]:
    resource_path = "/voyager/api/voyagerMessagingGraphQL/graphql"
    path_keys = {}
    query_params = { 
      "queryId": query_id,
      "variables": {
      "mailboxUrn": str(fsd_profile_urn)
      }
    }
    response = self.restli_client.get(
      resource_path=resource_path,
      access_token="",
      path_keys=path_keys,
      query_params=query_params,
      use_www=www_params,
    )
    if not 200 <= response.status_code < 300:
      dprint(f"Not good: {response.status_code} while getting linkedin messages conversation")
      return

    entity = response.entity
    try:
      return LinkedinMessageConversations.model_validate(entity, strict=True)
    except ValidationError as e:
      dprint(f"Error validating {e} model")
      return None