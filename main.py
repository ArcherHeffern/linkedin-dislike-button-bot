from typing import Optional

from pydantic import ValidationError
from common import ANSIColor, MessageConversations
from linkedin_api.clients.restli.client import RestliClient
from dotenv import dotenv_values

from linkedin_api.common.constants import WWWParams

DEBUG = True

ENV = dotenv_values()
ACCESS_TOKEN = ENV["ACCESS_TOKEN"]
CSRF_TOKEN = ENV["CSRF_TOKEN"]
LI_AT = ENV["LI_AT"]
MAILBOX_URN = ENV["MAILBOX_URN"]
QUERY_ID = ENV["QUERY_ID"]

def dprint(s: str):
  if DEBUG:
    print(s)

class LinkedinAPI:
  def __init__(self):
    self.restli_client = RestliClient()


  def get_user_info(self):
    response = self.restli_client.get(
        resource_path="/userinfo",
        access_token=ACCESS_TOKEN,
    )
    # print(response.entity)


  def get_mail(self) -> Optional[MessageConversations]:
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
      return MessageConversations.model_validate(entity, strict=True)
    except ValidationError as e:
      dprint(e.title)
      return None


LinkedinAPI().get_user_info()
mail = LinkedinAPI().get_mail()
if mail is None:
  exit(1)
# print(parsed_entity.data.messengerConversationsBySyncToken.elements[0].messages.elements[0].body.keys())
for messages in mail.data.messengerConversationsBySyncToken.elements:
  pt = messages.creator.participantType
  name = None
  if pt.member:
    name = pt.member.firstName.text + " " + pt.member.lastName.text
    if name == "Ethan Reynolds":
      print(messages)
      from sys import exit
      exit(1)
  elif pt.organization:
    name = pt.organization.name.text
  else:
    name = "(CUSTOM)"

  print(fr"{ANSIColor.RED.value}{name}{ANSIColor.RESET.value}")
  for message in messages.messages.elements:
    print(f">\t{message.body.text}")
    # print(parsed_entity.model_dump()
# LinkedinAPI().get_mail()
