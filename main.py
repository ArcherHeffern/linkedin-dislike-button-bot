import re
from typing import Optional

from pydantic import ValidationError
from common import ANSIColor 
from models.linkedin_all_mail import MessageConversations, Messages
from linkedin_api.clients.restli.client import RestliClient
from dotenv import dotenv_values

from linkedin_api.common.constants import WWWParams
from models.linkedin_mail_chain import MailChain
from models.mine import Mail, MailThread

DEBUG = True

ENV = dotenv_values()
ACCESS_TOKEN = ENV["ACCESS_TOKEN"]
CSRF_TOKEN = ENV["CSRF_TOKEN"]
LI_AT = ENV["LI_AT"]
MAILBOX_URN = ENV["MAILBOX_URN"]
QUERY_ID = ENV["QUERY_ID"]

def dprint(s: str):
  if DEBUG:
    print(f"Error: {s}")

class LinkedinAPI:
  def __init__(self):
    self.restli_client = RestliClient()


  def get_user_info(self):
    response = self.restli_client.get(
        resource_path="/userinfo",
        access_token=ACCESS_TOKEN,
    )
    # print(response.entity)


  def get_single_messaging_thread(self, msg_converation_urn: str) -> Optional[MailChain]:
    resource_path = "/voyager/api/voyagerMessagingGraphQL/graphql"
    path_keys = {}
    query_params = {
      "queryId": "messengerMessages.455dde239612d966346c1d1c4352f648",
      "variables": {
        "conversationUrn": str(msg_converation_urn)
      }
    }
    www_params: WWWParams = {
      "CSRFToken": CSRF_TOKEN,
      "li_at": LI_AT,
    }
    response = self.restli_client.get(
      resource_path=resource_path,
      access_token=ACCESS_TOKEN,
      path_keys=path_keys,
      query_params=query_params,
      use_www=www_params,
    )
    if not 200 <= response.status_code < 300:
      dprint(f"Not good: {response.status_code}")
      return

    entity = response.entity
    try:
      return MailChain.model_validate(entity, strict=True)
    except ValidationError as e:
      dprint(f"Validation Error: {str(e)}")
      return 

  def get_mail(self) -> Optional[Mail]:
    resource_path = "/voyager/api/voyagerMessagingGraphQL/graphql"
    path_keys = {}
    query_params = { 
      "queryId": QUERY_ID,
      "variables": {
      "mailboxUrn": MAILBOX_URN
    }
    }
    www_params: WWWParams = {
      "CSRFToken": CSRF_TOKEN,
      "li_at": LI_AT,
    }
    response = self.restli_client.get(
      resource_path=resource_path,
      access_token=ACCESS_TOKEN,
      path_keys=path_keys,
      query_params=query_params,
      use_www=www_params,
    )
    if not 200 <= response.status_code < 300:
      dprint(f"Not good: {response.status_code}")
      return

    entity = response.entity
    try:
      linkedin_mail = MessageConversations.model_validate(entity, strict=True)
      threads = []
      for linkedin_message_conversation in linkedin_mail.data.messengerConversationsBySyncToken.elements:
        linkedin_mail_chain = self.get_single_messaging_thread(linkedin_message_conversation.entityUrn) 
        threads.append(MailThread.from__linkedin_mail_chain(linkedin_message_conversation, linkedin_mail_chain))
      return Mail(threads)
    except ValidationError as e:
      dprint(e.title)
      return None


LinkedinAPI().get_user_info()
mail = LinkedinAPI().get_mail()
print(mail)