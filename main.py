from time import sleep
from sys import exit
from typing import Optional
from models.linkedin_all_mail import Element, LinkedinMessageConversations
from models.linkedin_mail_chain import LinkedinMailChain
from src.environment import ALT_CSRF_TOKEN, ALT_LI_AT, CSRF_TOKEN, LI_AT
from restli.common.constants import WWWParams
from src.linkedin_api import LinkedinAPI
from models.mine import MailThread

# TODO
# - How to comment on a post
# - How to get new comments
# - How to know if theres new comments? 


api = LinkedinAPI()
main_account = WWWParams(CSRF_TOKEN, LI_AT)
alt_account = WWWParams(ALT_CSRF_TOKEN, ALT_LI_AT)

def tick() -> bool:
  maybe_mail = api.get_linkedin_messages_conversations(main_account)
  if not maybe_mail:
    return False
  for conversation in maybe_mail.data.messengerConversationsBySyncToken.elements:
    if conversation.unreadCount == 0:
      continue
    # Get unread messages and forward stuffs to them
    maybe_linkedin_mail_chain = api.get_single_messaging_thread(conversation, main_account)
    if not maybe_linkedin_mail_chain:
      continue
    mail_thread = MailThread.from__linkedin_mail_chain(conversation, maybe_linkedin_mail_chain)
    unread_messages = mail_thread.messages[0:conversation.unreadCount]
    for unread_message in unread_messages:
      if len(unread_message.host_urns) == 0:
        continue
      unread_forwarded_post = unread_message
      print(unread_forwarded_post)
      # Write message on each post
      # Mark messages as read


def get_all_message_threads(account_params: WWWParams) -> Optional[tuple[LinkedinMessageConversations, tuple[Element, LinkedinMailChain]]]:
  linkedin_api_constants = api.get_linkedin_api_constants()
  fsd_profile_urn = api.get_fsd_profile_urn(account_params)
  if fsd_profile_urn is None:
    return
  account_messages = api.get_linkedin_messages_conversations(account_params, linkedin_api_constants, fsd_profile_urn)
  if not account_messages:
    return
  account_threads: tuple[Element, LinkedinMailChain] = []
  for thread in account_messages.data.messengerConversationsBySyncToken.elements:
    thread_messages = api.get_single_messaging_thread(thread, alt_account)
    account_threads.append((thread, thread_messages))
  
  return account_messages, account_threads

account_messages, account_threads = get_all_message_threads(alt_account)
for account_thread in account_threads:
  print(MailThread.from__linkedin_mail_chain(account_thread[0], account_thread[1]))
# for _ in range(1):
#   print("sending")
#   api.share_post(alt_account)
# tick()