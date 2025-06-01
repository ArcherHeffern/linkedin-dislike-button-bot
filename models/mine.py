from dataclasses import dataclass
from models.linkedin_all_mail import Element
from models.linkedin_mail_chain import LinkedinMailChain
from typing import NewType

@dataclass
class Mail:
    threads: list['MailThread']

HostUrn = NewType('HostUrn', str) 
FsdProfileUrn = NewType('FsdProfileUrn', str) 

@dataclass
class Message:
    msg: str
    host_urns: list[HostUrn]

@dataclass
class MailThread:
    from_: str
    messages: list[Message]

    @staticmethod
    def from__linkedin_mail_chain(linkedin_message_conversation: Element, linkedin_mail_chain: LinkedinMailChain) -> 'MailThread':
        pt = linkedin_message_conversation.creator.participantType
        name = None
        if pt.member:
            name = pt.member.firstName.text + " " + pt.member.lastName.text
        elif pt.organization:
            name = pt.organization.name.text
        else:
            name = "(CUSTOM)"

        messages: list[Message] = []
        for linkedin_message in linkedin_mail_chain.data.messengerMessagesBySyncToken.elements:
            host_urns: list[HostUrn] = [HostUrn(render_content.hostUrnData.hostUrn) for render_content in linkedin_message.renderContent if render_content.hostUrnData is not None]
            messages.append(Message(linkedin_message.body.text, host_urns))
        return MailThread(name, messages)