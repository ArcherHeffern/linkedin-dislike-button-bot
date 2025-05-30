
from pydantic import BaseModel
from typing import Optional


class DisabledFeature(BaseModel):
  ...

class MessageBody(BaseModel):
  _type: dict
  attributes: list
  text: str # What we want!
  _recipeType: dict
  
class Message(BaseModel):
  reactionSummaries: list[dict]
  footer: Optional[str]
  subject: Optional[str]
  _type: dict
  inlineWarning: Optional[str]
  body: MessageBody
  _recipeType: dict
  originToken: Optional[str]
  backendUrn: str
  deliveredAt: int
  renderContentFallbackText: Optional[str]
  actor: dict
  entityUrn: str
  sender: dict
  backendConversationUrn: str
  incompleteRetriableData: bool
  messageBodyRenderFormat: str
  renderContent: list[dict]
  conversation: dict

class Messages(BaseModel):
  elements: list[Message]

class MemberName(BaseModel):
  _type: dict
  attributes: list[dict]
  text: str
  _recipeType: str

class MemberParticipantType(BaseModel):
  profileUrl: str
  firstName: MemberName
  lastName: MemberName

class OrgParticipationName(BaseModel):
  _type: str
  attributes: list[str]
  text: str
  _recipeType: str

class OrgParticipantType(BaseModel):
  industryName: Optional[str]
  name: OrgParticipationName
  pageUrl: str

class ParticipantType(BaseModel):
  member: Optional[MemberParticipantType]
  organization: Optional[OrgParticipantType]
  custom: Optional[dict]

class Creator(BaseModel):
  hostIdentityUrn: str
  preview: Optional[dict]
  entityUrn: str
  memberBadgeType: Optional[str]
  showPremiumInBug: bool
  showVerificationBadge: bool
  _type: dict
  participantType: ParticipantType
  _recipeType: dict
  backendUrn: str

class Element(BaseModel):
  notificationStatus: str
  conversationParticipants: list[dict]
  unreadCount: int
  conversationVerificationLabel: Optional[int]
  lastActivityAt: int
  descriptionText: Optional[str]
  conversationVerificationExplanation: Optional[str]
  title: Optional[str]
  backendUrn: str
  shortHeadlineText: Optional[str]
  createdAt: int
  lastReadAt: Optional[int]
  hostConversationActions: list[dict]
  entityUrn: str
  categories: list[str]
  state: Optional[str]
  disabledFeatures: list[DisabledFeature]
  creator: Creator
  read: bool
  groupChat: bool
  _type: dict
  contentMetadata: Optional[dict]
  _recipeType: dict
  conversationUrl: str
  headlineText: Optional[str]
  incompleteRetriableData: bool
  messages: Messages
  conversationTypeText: Optional[dict]

class MessengerConversationsBySyncToken(BaseModel):
  # _type: str
  # metadata: dict
  # _recipeType: str
  elements: list[Element]

class Data(BaseModel):
  _recipeType: str 
  _type: str
  messengerConversationsBySyncToken: MessengerConversationsBySyncToken
  
class LinkedinMessageConversations(BaseModel):
  data: Data