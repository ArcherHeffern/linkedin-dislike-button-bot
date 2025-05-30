from pydantic import BaseModel
from typing import List, Optional


class AttributedText(BaseModel):
    _type: str
    attributes: List
    text: str
    _recipeType: str


class Pronoun(BaseModel):
    customPronoun: Optional[str]
    standardizedPronoun: Optional[str]


class VectorArtifact(BaseModel):
    width: int
    height: int
    _type: str
    _recipeType: str
    fileIdentifyingUrlPathSegment: str


class ProfilePicture(BaseModel):
    digitalmediaAsset: Optional[str]
    _type: str
    attribution: Optional[str]
    _recipeType: str
    focalPoint: Optional[str]
    artifacts: List[VectorArtifact]
    rootUrl: str


class MemberParticipantInfo(BaseModel):
    profileUrl: str
    firstName: AttributedText
    lastName: AttributedText
    profilePicture: Optional[ProfilePicture]
    distance: str
    profileFrameA11yContent: Optional[AttributedText]
    pronoun: Optional[Pronoun]
    _type: str
    _recipeType: str
    headline: AttributedText


class ParticipantType(BaseModel):
    member: Optional[MemberParticipantInfo]
    custom: Optional[str]
    organization: Optional[dict]


class MessagingParticipant(BaseModel):
    hostIdentityUrn: str
    preview: Optional[str]
    entityUrn: str
    showPremiumInBug: bool
    memberBadgeType: Optional[str]
    showVerificationBadge: bool
    _type: str
    _recipeType: str
    backendUrn: str
    participantType: ParticipantType


class HostUrnData(BaseModel):
    _type: str
    type: str
    _recipeType: str
    hostUrn: str


class MessageBody(BaseModel):
    _type: str
    attributes: List
    text: str
    _recipeType: str


class Conversation(BaseModel):
    _recipeType: str
    _type: str
    entityUrn: str

class ConversationAdsMessageContent(BaseModel):
    ...

class RenderContentItem(BaseModel):
    videoMeeting: Optional[str]
    conversationAdsMessageContent: Optional[ConversationAdsMessageContent]
    repliedMessageContent: Optional[str]
    video: Optional[str]
    vectorImage: Optional[str]
    awayMessage: Optional[str]
    file: Optional[str]
    externalMedia: Optional[str]
    messageAdRenderContent: Optional[dict]
    audio: Optional[str]
    forwardedMessageContent: Optional[str]
    hostUrnData: Optional[HostUrnData]
    unavailableContent: Optional[str]


class Message(BaseModel):
    reactionSummaries: List
    footer: Optional[str]
    subject: Optional[str]
    _type: str
    inlineWarning: Optional[str]
    body: MessageBody
    originToken: Optional[str]
    _recipeType: str
    backendUrn: str
    deliveredAt: int
    renderContentFallbackText: Optional[str]
    actor: MessagingParticipant
    entityUrn: str
    sender: MessagingParticipant
    backendConversationUrn: str
    incompleteRetriableData: bool
    messageBodyRenderFormat: str
    renderContent: List[RenderContentItem]
    conversation: Conversation


class SyncMetadata(BaseModel):
    _type: str
    deletedUrns: List[str]
    newSyncToken: str
    _recipeType: str
    shouldClearCache: bool


class MessengerMessagesBySyncToken(BaseModel):
    _type: str
    metadata: SyncMetadata
    _recipeType: str
    elements: List[Message]


class Data(BaseModel):
    _recipeType: str
    _type: str
    messengerMessagesBySyncToken: MessengerMessagesBySyncToken


class LinkedinMailChain(BaseModel):
    data: Data