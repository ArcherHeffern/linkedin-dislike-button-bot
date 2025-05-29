from dataclasses import dataclass
from typing import Self
from models.linkedin_all_mail import Element
from models.linkedin_mail_chain import MailChain

@dataclass
class Mail:
    threads: list['MailThread']

@dataclass
class MailThread:
    from_: str
    messages: list[str]

    @staticmethod
    def from__linkedin_mail_chain(linkedin_message_conversation: Element, linkedin_mail_chain: MailChain) -> Self:
        pt = linkedin_message_conversation.creator.participantType
        name = None
        if pt.member:
            name = pt.member.firstName.text + " " + pt.member.lastName.text
        elif pt.organization:
            name = pt.organization.name.text
        else:
            name = "(CUSTOM)"
        return MailThread(name, [m.body.text for m in linkedin_mail_chain.data.messengerMessagesBySyncToken.elements])