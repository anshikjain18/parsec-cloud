// Parsec Cloud (https://parsec.cloud) Copyright (c) BUSL-1.1 2016-present Scille SAS

/*
 * /!\ Auto-generated code (see `bindings/generator`), any modification will be lost ! /!\
 */

export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E }

type DateTime = string
type EntryName = string
type Password = string
type Path = string
type UserID = string
type OrganizationID = string
type DeviceID = string
type DeviceLabel = string
type HumanHandle = string
type BackendAddr = string
type BackendOrganizationAddr = string
type BackendOrganizationBootstrapAddr = string
type BackendInvitationAddr = string
type SASCode = string
type EntryID = Uint8Array
type SequesterVerifyKeyDer = Uint8Array
type InvitationToken = Uint8Array
type Handle = number
type CacheSize = number

export interface ClientConfig {
    configDir: Path
    dataBaseDir: Path
    mountpointBaseDir: Path
    workspaceStorageCacheSize: WorkspaceStorageCacheSize
}

export interface AvailableDevice {
    keyFilePath: Path
    organizationId: OrganizationID
    deviceId: DeviceID
    humanHandle: HumanHandle | null
    deviceLabel: DeviceLabel | null
    slug: string
    ty: DeviceFileType
}

export interface UserClaimInProgress1Info {
    handle: number
    greeterSas: SASCode
    greeterSasChoices: Array<SASCode>
}

export interface DeviceClaimInProgress1Info {
    handle: number
    greeterSas: SASCode
    greeterSasChoices: Array<SASCode>
}

export interface UserClaimInProgress2Info {
    handle: number
    claimerSas: SASCode
}

export interface DeviceClaimInProgress2Info {
    handle: number
    claimerSas: SASCode
}

export interface UserClaimInProgress3Info {
    handle: number
}

export interface DeviceClaimInProgress3Info {
    handle: number
}

export interface UserClaimFinalizeInfo {
    handle: number
}

export interface DeviceClaimFinalizeInfo {
    handle: number
}

export interface UserGreetInitialInfo {
    handle: number
}

export interface DeviceGreetInitialInfo {
    handle: number
}

export interface UserGreetInProgress1Info {
    handle: number
    greeterSas: SASCode
}

export interface DeviceGreetInProgress1Info {
    handle: number
    greeterSas: SASCode
}

export interface UserGreetInProgress2Info {
    handle: number
    claimerSas: SASCode
    claimerSasChoices: Array<SASCode>
}

export interface DeviceGreetInProgress2Info {
    handle: number
    claimerSas: SASCode
    claimerSasChoices: Array<SASCode>
}

export interface UserGreetInProgress3Info {
    handle: number
}

export interface DeviceGreetInProgress3Info {
    handle: number
}

export interface UserGreetInProgress4Info {
    handle: number
    requestedHumanHandle: HumanHandle | null
    requestedDeviceLabel: DeviceLabel | null
}

export interface DeviceGreetInProgress4Info {
    handle: number
    requestedDeviceLabel: DeviceLabel | null
}

// CancelError
export interface CancelErrorInternal {
    tag: 'Internal'
    error: string
}
export interface CancelErrorNotBinded {
    tag: 'NotBinded'
    error: string
}
export type CancelError =
  | CancelErrorInternal
  | CancelErrorNotBinded

// RealmRole
export interface RealmRoleContributor {
    tag: 'Contributor'
}
export interface RealmRoleManager {
    tag: 'Manager'
}
export interface RealmRoleOwner {
    tag: 'Owner'
}
export interface RealmRoleReader {
    tag: 'Reader'
}
export type RealmRole =
  | RealmRoleContributor
  | RealmRoleManager
  | RealmRoleOwner
  | RealmRoleReader

// DeviceAccessStrategy
export interface DeviceAccessStrategyPassword {
    tag: 'Password'
    password: Password
    keyFile: Path
}
export interface DeviceAccessStrategySmartcard {
    tag: 'Smartcard'
    keyFile: Path
}
export type DeviceAccessStrategy =
  | DeviceAccessStrategyPassword
  | DeviceAccessStrategySmartcard

// ClientStartError
export interface ClientStartErrorInternal {
    tag: 'Internal'
    error: string
}
export interface ClientStartErrorLoadDeviceDecryptionFailed {
    tag: 'LoadDeviceDecryptionFailed'
    error: string
}
export interface ClientStartErrorLoadDeviceInvalidData {
    tag: 'LoadDeviceInvalidData'
    error: string
}
export interface ClientStartErrorLoadDeviceInvalidPath {
    tag: 'LoadDeviceInvalidPath'
    error: string
}
export type ClientStartError =
  | ClientStartErrorInternal
  | ClientStartErrorLoadDeviceDecryptionFailed
  | ClientStartErrorLoadDeviceInvalidData
  | ClientStartErrorLoadDeviceInvalidPath

// ClientStopError
export interface ClientStopErrorInternal {
    tag: 'Internal'
    error: string
}
export type ClientStopError =
  | ClientStopErrorInternal

// ClientListWorkspacesError
export interface ClientListWorkspacesErrorInternal {
    tag: 'Internal'
    error: string
}
export type ClientListWorkspacesError =
  | ClientListWorkspacesErrorInternal

// ClientWorkspaceCreateError
export interface ClientWorkspaceCreateErrorInternal {
    tag: 'Internal'
    error: string
}
export type ClientWorkspaceCreateError =
  | ClientWorkspaceCreateErrorInternal

// ClientWorkspaceRenameError
export interface ClientWorkspaceRenameErrorInternal {
    tag: 'Internal'
    error: string
}
export interface ClientWorkspaceRenameErrorUnknownWorkspace {
    tag: 'UnknownWorkspace'
    error: string
}
export type ClientWorkspaceRenameError =
  | ClientWorkspaceRenameErrorInternal
  | ClientWorkspaceRenameErrorUnknownWorkspace

// ClientWorkspaceShareError
export interface ClientWorkspaceShareErrorBadTimestamp {
    tag: 'BadTimestamp'
    error: string
    serverTimestamp: DateTime
    clientTimestamp: DateTime
    ballparkClientEarlyOffset: number
    ballparkClientLateOffset: number
}
export interface ClientWorkspaceShareErrorInternal {
    tag: 'Internal'
    error: string
}
export interface ClientWorkspaceShareErrorNotAllowed {
    tag: 'NotAllowed'
    error: string
}
export interface ClientWorkspaceShareErrorOffline {
    tag: 'Offline'
    error: string
}
export interface ClientWorkspaceShareErrorOutsiderCannotBeManagerOrOwner {
    tag: 'OutsiderCannotBeManagerOrOwner'
    error: string
}
export interface ClientWorkspaceShareErrorRevokedRecipient {
    tag: 'RevokedRecipient'
    error: string
}
export interface ClientWorkspaceShareErrorShareToSelf {
    tag: 'ShareToSelf'
    error: string
}
export interface ClientWorkspaceShareErrorUnknownRecipient {
    tag: 'UnknownRecipient'
    error: string
}
export interface ClientWorkspaceShareErrorUnknownRecipientOrWorkspace {
    tag: 'UnknownRecipientOrWorkspace'
    error: string
}
export interface ClientWorkspaceShareErrorUnknownWorkspace {
    tag: 'UnknownWorkspace'
    error: string
}
export interface ClientWorkspaceShareErrorWorkspaceInMaintenance {
    tag: 'WorkspaceInMaintenance'
    error: string
}
export type ClientWorkspaceShareError =
  | ClientWorkspaceShareErrorBadTimestamp
  | ClientWorkspaceShareErrorInternal
  | ClientWorkspaceShareErrorNotAllowed
  | ClientWorkspaceShareErrorOffline
  | ClientWorkspaceShareErrorOutsiderCannotBeManagerOrOwner
  | ClientWorkspaceShareErrorRevokedRecipient
  | ClientWorkspaceShareErrorShareToSelf
  | ClientWorkspaceShareErrorUnknownRecipient
  | ClientWorkspaceShareErrorUnknownRecipientOrWorkspace
  | ClientWorkspaceShareErrorUnknownWorkspace
  | ClientWorkspaceShareErrorWorkspaceInMaintenance

// UserProfile
export interface UserProfileAdmin {
    tag: 'Admin'
}
export interface UserProfileOutsider {
    tag: 'Outsider'
}
export interface UserProfileStandard {
    tag: 'Standard'
}
export type UserProfile =
  | UserProfileAdmin
  | UserProfileOutsider
  | UserProfileStandard

// WorkspaceStorageCacheSize
export interface WorkspaceStorageCacheSizeCustom {
    tag: 'Custom'
    size: number
}
export interface WorkspaceStorageCacheSizeDefault {
    tag: 'Default'
}
export type WorkspaceStorageCacheSize =
  | WorkspaceStorageCacheSizeCustom
  | WorkspaceStorageCacheSizeDefault

// ClientEvent
export interface ClientEventPing {
    tag: 'Ping'
    ping: string
}
export type ClientEvent =
  | ClientEventPing

// ClaimerGreeterAbortOperationError
export interface ClaimerGreeterAbortOperationErrorInternal {
    tag: 'Internal'
    error: string
}
export type ClaimerGreeterAbortOperationError =
  | ClaimerGreeterAbortOperationErrorInternal

// DeviceFileType
export interface DeviceFileTypePassword {
    tag: 'Password'
}
export interface DeviceFileTypeRecovery {
    tag: 'Recovery'
}
export interface DeviceFileTypeSmartcard {
    tag: 'Smartcard'
}
export type DeviceFileType =
  | DeviceFileTypePassword
  | DeviceFileTypeRecovery
  | DeviceFileTypeSmartcard

// DeviceSaveStrategy
export interface DeviceSaveStrategyPassword {
    tag: 'Password'
    password: Password
}
export interface DeviceSaveStrategySmartcard {
    tag: 'Smartcard'
}
export type DeviceSaveStrategy =
  | DeviceSaveStrategyPassword
  | DeviceSaveStrategySmartcard

// BootstrapOrganizationError
export interface BootstrapOrganizationErrorAlreadyUsedToken {
    tag: 'AlreadyUsedToken'
    error: string
}
export interface BootstrapOrganizationErrorBadTimestamp {
    tag: 'BadTimestamp'
    error: string
    serverTimestamp: DateTime
    clientTimestamp: DateTime
    ballparkClientEarlyOffset: number
    ballparkClientLateOffset: number
}
export interface BootstrapOrganizationErrorInternal {
    tag: 'Internal'
    error: string
}
export interface BootstrapOrganizationErrorInvalidToken {
    tag: 'InvalidToken'
    error: string
}
export interface BootstrapOrganizationErrorOffline {
    tag: 'Offline'
    error: string
}
export interface BootstrapOrganizationErrorSaveDeviceError {
    tag: 'SaveDeviceError'
    error: string
}
export type BootstrapOrganizationError =
  | BootstrapOrganizationErrorAlreadyUsedToken
  | BootstrapOrganizationErrorBadTimestamp
  | BootstrapOrganizationErrorInternal
  | BootstrapOrganizationErrorInvalidToken
  | BootstrapOrganizationErrorOffline
  | BootstrapOrganizationErrorSaveDeviceError

// ClaimerRetrieveInfoError
export interface ClaimerRetrieveInfoErrorAlreadyUsed {
    tag: 'AlreadyUsed'
    error: string
}
export interface ClaimerRetrieveInfoErrorInternal {
    tag: 'Internal'
    error: string
}
export interface ClaimerRetrieveInfoErrorNotFound {
    tag: 'NotFound'
    error: string
}
export interface ClaimerRetrieveInfoErrorOffline {
    tag: 'Offline'
    error: string
}
export type ClaimerRetrieveInfoError =
  | ClaimerRetrieveInfoErrorAlreadyUsed
  | ClaimerRetrieveInfoErrorInternal
  | ClaimerRetrieveInfoErrorNotFound
  | ClaimerRetrieveInfoErrorOffline

// ClaimInProgressError
export interface ClaimInProgressErrorActiveUsersLimitReached {
    tag: 'ActiveUsersLimitReached'
    error: string
}
export interface ClaimInProgressErrorAlreadyUsed {
    tag: 'AlreadyUsed'
    error: string
}
export interface ClaimInProgressErrorCancelled {
    tag: 'Cancelled'
    error: string
}
export interface ClaimInProgressErrorCorruptedConfirmation {
    tag: 'CorruptedConfirmation'
    error: string
}
export interface ClaimInProgressErrorInternal {
    tag: 'Internal'
    error: string
}
export interface ClaimInProgressErrorNotFound {
    tag: 'NotFound'
    error: string
}
export interface ClaimInProgressErrorOffline {
    tag: 'Offline'
    error: string
}
export interface ClaimInProgressErrorPeerReset {
    tag: 'PeerReset'
    error: string
}
export type ClaimInProgressError =
  | ClaimInProgressErrorActiveUsersLimitReached
  | ClaimInProgressErrorAlreadyUsed
  | ClaimInProgressErrorCancelled
  | ClaimInProgressErrorCorruptedConfirmation
  | ClaimInProgressErrorInternal
  | ClaimInProgressErrorNotFound
  | ClaimInProgressErrorOffline
  | ClaimInProgressErrorPeerReset

// UserOrDeviceClaimInitialInfo
export interface UserOrDeviceClaimInitialInfoDevice {
    tag: 'Device'
    handle: number
    greeterUserId: UserID
    greeterHumanHandle: HumanHandle | null
}
export interface UserOrDeviceClaimInitialInfoUser {
    tag: 'User'
    handle: number
    claimerEmail: string
    greeterUserId: UserID
    greeterHumanHandle: HumanHandle | null
}
export type UserOrDeviceClaimInitialInfo =
  | UserOrDeviceClaimInitialInfoDevice
  | UserOrDeviceClaimInitialInfoUser

// InvitationStatus
export interface InvitationStatusDeleted {
    tag: 'Deleted'
}
export interface InvitationStatusIdle {
    tag: 'Idle'
}
export interface InvitationStatusReady {
    tag: 'Ready'
}
export type InvitationStatus =
  | InvitationStatusDeleted
  | InvitationStatusIdle
  | InvitationStatusReady

// InvitationEmailSentStatus
export interface InvitationEmailSentStatusBadRecipient {
    tag: 'BadRecipient'
}
export interface InvitationEmailSentStatusNotAvailable {
    tag: 'NotAvailable'
}
export interface InvitationEmailSentStatusSuccess {
    tag: 'Success'
}
export type InvitationEmailSentStatus =
  | InvitationEmailSentStatusBadRecipient
  | InvitationEmailSentStatusNotAvailable
  | InvitationEmailSentStatusSuccess

// NewUserInvitationError
export interface NewUserInvitationErrorAlreadyMember {
    tag: 'AlreadyMember'
    error: string
}
export interface NewUserInvitationErrorInternal {
    tag: 'Internal'
    error: string
}
export interface NewUserInvitationErrorNotAllowed {
    tag: 'NotAllowed'
    error: string
}
export interface NewUserInvitationErrorOffline {
    tag: 'Offline'
    error: string
}
export type NewUserInvitationError =
  | NewUserInvitationErrorAlreadyMember
  | NewUserInvitationErrorInternal
  | NewUserInvitationErrorNotAllowed
  | NewUserInvitationErrorOffline

// NewDeviceInvitationError
export interface NewDeviceInvitationErrorInternal {
    tag: 'Internal'
    error: string
}
export interface NewDeviceInvitationErrorOffline {
    tag: 'Offline'
    error: string
}
export interface NewDeviceInvitationErrorSendEmailToUserWithoutEmail {
    tag: 'SendEmailToUserWithoutEmail'
    error: string
}
export type NewDeviceInvitationError =
  | NewDeviceInvitationErrorInternal
  | NewDeviceInvitationErrorOffline
  | NewDeviceInvitationErrorSendEmailToUserWithoutEmail

// DeleteInvitationError
export interface DeleteInvitationErrorAlreadyDeleted {
    tag: 'AlreadyDeleted'
    error: string
}
export interface DeleteInvitationErrorInternal {
    tag: 'Internal'
    error: string
}
export interface DeleteInvitationErrorNotFound {
    tag: 'NotFound'
    error: string
}
export interface DeleteInvitationErrorOffline {
    tag: 'Offline'
    error: string
}
export type DeleteInvitationError =
  | DeleteInvitationErrorAlreadyDeleted
  | DeleteInvitationErrorInternal
  | DeleteInvitationErrorNotFound
  | DeleteInvitationErrorOffline

// InviteListItem
export interface InviteListItemDevice {
    tag: 'Device'
    token: InvitationToken
    createdOn: DateTime
    status: InvitationStatus
}
export interface InviteListItemUser {
    tag: 'User'
    token: InvitationToken
    createdOn: DateTime
    claimerEmail: string
    status: InvitationStatus
}
export type InviteListItem =
  | InviteListItemDevice
  | InviteListItemUser

// ListInvitationsError
export interface ListInvitationsErrorInternal {
    tag: 'Internal'
    error: string
}
export interface ListInvitationsErrorOffline {
    tag: 'Offline'
    error: string
}
export type ListInvitationsError =
  | ListInvitationsErrorInternal
  | ListInvitationsErrorOffline

// ClientStartInvitationGreetError
export interface ClientStartInvitationGreetErrorInternal {
    tag: 'Internal'
    error: string
}
export type ClientStartInvitationGreetError =
  | ClientStartInvitationGreetErrorInternal

// GreetInProgressError
export interface GreetInProgressErrorActiveUsersLimitReached {
    tag: 'ActiveUsersLimitReached'
    error: string
}
export interface GreetInProgressErrorAlreadyUsed {
    tag: 'AlreadyUsed'
    error: string
}
export interface GreetInProgressErrorBadTimestamp {
    tag: 'BadTimestamp'
    error: string
    serverTimestamp: DateTime
    clientTimestamp: DateTime
    ballparkClientEarlyOffset: number
    ballparkClientLateOffset: number
}
export interface GreetInProgressErrorCancelled {
    tag: 'Cancelled'
    error: string
}
export interface GreetInProgressErrorCorruptedInviteUserData {
    tag: 'CorruptedInviteUserData'
    error: string
}
export interface GreetInProgressErrorDeviceAlreadyExists {
    tag: 'DeviceAlreadyExists'
    error: string
}
export interface GreetInProgressErrorInternal {
    tag: 'Internal'
    error: string
}
export interface GreetInProgressErrorNonceMismatch {
    tag: 'NonceMismatch'
    error: string
}
export interface GreetInProgressErrorNotFound {
    tag: 'NotFound'
    error: string
}
export interface GreetInProgressErrorOffline {
    tag: 'Offline'
    error: string
}
export interface GreetInProgressErrorPeerReset {
    tag: 'PeerReset'
    error: string
}
export interface GreetInProgressErrorUserAlreadyExists {
    tag: 'UserAlreadyExists'
    error: string
}
export interface GreetInProgressErrorUserCreateNotAllowed {
    tag: 'UserCreateNotAllowed'
    error: string
}
export type GreetInProgressError =
  | GreetInProgressErrorActiveUsersLimitReached
  | GreetInProgressErrorAlreadyUsed
  | GreetInProgressErrorBadTimestamp
  | GreetInProgressErrorCancelled
  | GreetInProgressErrorCorruptedInviteUserData
  | GreetInProgressErrorDeviceAlreadyExists
  | GreetInProgressErrorInternal
  | GreetInProgressErrorNonceMismatch
  | GreetInProgressErrorNotFound
  | GreetInProgressErrorOffline
  | GreetInProgressErrorPeerReset
  | GreetInProgressErrorUserAlreadyExists
  | GreetInProgressErrorUserCreateNotAllowed

export interface LibParsecPlugin {
    cancel(
        canceller: number
    ): Promise<Result<null, CancelError>>
    newCanceller(
    ): Promise<number>
    clientStart(
        config: ClientConfig,
        on_event_callback: (event: ClientEvent) => void,
        access: DeviceAccessStrategy
    ): Promise<Result<number, ClientStartError>>
    clientStop(
        client: number
    ): Promise<Result<null, ClientStopError>>
    clientListWorkspaces(
        client: number
    ): Promise<Result<Array<[EntryID, EntryName]>, ClientListWorkspacesError>>
    clientWorkspaceCreate(
        client: number,
        name: EntryName
    ): Promise<Result<EntryID, ClientWorkspaceCreateError>>
    clientWorkspaceRename(
        client: number,
        workspace_id: EntryID,
        new_name: EntryName
    ): Promise<Result<null, ClientWorkspaceRenameError>>
    clientWorkspaceShare(
        client: number,
        workspace_id: EntryID,
        recipient: UserID,
        role: RealmRole | null
    ): Promise<Result<null, ClientWorkspaceShareError>>
    claimerGreeterAbortOperation(
        handle: number
    ): Promise<Result<null, ClaimerGreeterAbortOperationError>>
    listAvailableDevices(
        path: Path
    ): Promise<Array<AvailableDevice>>
    bootstrapOrganization(
        config: ClientConfig,
        on_event_callback: (event: ClientEvent) => void,
        bootstrap_organization_addr: BackendOrganizationBootstrapAddr,
        save_strategy: DeviceSaveStrategy,
        human_handle: HumanHandle | null,
        device_label: DeviceLabel | null,
        sequester_authority_verify_key: SequesterVerifyKeyDer | null
    ): Promise<Result<AvailableDevice, BootstrapOrganizationError>>
    claimerRetrieveInfo(
        config: ClientConfig,
        on_event_callback: (event: ClientEvent) => void,
        addr: BackendInvitationAddr
    ): Promise<Result<UserOrDeviceClaimInitialInfo, ClaimerRetrieveInfoError>>
    claimerUserInitialDoWaitPeer(
        canceller: number,
        handle: number
    ): Promise<Result<UserClaimInProgress1Info, ClaimInProgressError>>
    claimerDeviceInitialDoWaitPeer(
        canceller: number,
        handle: number
    ): Promise<Result<DeviceClaimInProgress1Info, ClaimInProgressError>>
    claimerUserInProgress1DoSignifyTrust(
        canceller: number,
        handle: number
    ): Promise<Result<UserClaimInProgress2Info, ClaimInProgressError>>
    claimerDeviceInProgress1DoSignifyTrust(
        canceller: number,
        handle: number
    ): Promise<Result<DeviceClaimInProgress2Info, ClaimInProgressError>>
    claimerUserInProgress2DoWaitPeerTrust(
        canceller: number,
        handle: number
    ): Promise<Result<UserClaimInProgress3Info, ClaimInProgressError>>
    claimerDeviceInProgress2DoWaitPeerTrust(
        canceller: number,
        handle: number
    ): Promise<Result<DeviceClaimInProgress3Info, ClaimInProgressError>>
    claimerUserInProgress3DoClaim(
        canceller: number,
        handle: number,
        requested_device_label: DeviceLabel | null,
        requested_human_handle: HumanHandle | null
    ): Promise<Result<UserClaimFinalizeInfo, ClaimInProgressError>>
    claimerDeviceInProgress3DoClaim(
        canceller: number,
        handle: number,
        requested_device_label: DeviceLabel | null
    ): Promise<Result<DeviceClaimFinalizeInfo, ClaimInProgressError>>
    claimerUserFinalizeSaveLocalDevice(
        handle: number,
        save_strategy: DeviceSaveStrategy
    ): Promise<Result<AvailableDevice, ClaimInProgressError>>
    claimerDeviceFinalizeSaveLocalDevice(
        handle: number,
        save_strategy: DeviceSaveStrategy
    ): Promise<Result<AvailableDevice, ClaimInProgressError>>
    clientNewUserInvitation(
        client: number,
        claimer_email: string,
        send_email: boolean
    ): Promise<Result<[InvitationToken, InvitationEmailSentStatus], NewUserInvitationError>>
    clientNewDeviceInvitation(
        client: number,
        send_email: boolean
    ): Promise<Result<[InvitationToken, InvitationEmailSentStatus], NewDeviceInvitationError>>
    clientDeleteInvitation(
        client: number,
        token: InvitationToken
    ): Promise<Result<null, DeleteInvitationError>>
    clientListInvitations(
        client: number
    ): Promise<Result<Array<InviteListItem>, ListInvitationsError>>
    clientStartUserInvitationGreet(
        client: number,
        token: InvitationToken
    ): Promise<Result<UserGreetInitialInfo, ClientStartInvitationGreetError>>
    clientStartDeviceInvitationGreet(
        client: number,
        token: InvitationToken
    ): Promise<Result<DeviceGreetInitialInfo, ClientStartInvitationGreetError>>
    greeterUserInitialDoWaitPeer(
        canceller: number,
        handle: number
    ): Promise<Result<UserGreetInProgress1Info, GreetInProgressError>>
    greeterDeviceInitialDoWaitPeer(
        canceller: number,
        handle: number
    ): Promise<Result<DeviceGreetInProgress1Info, GreetInProgressError>>
    greeterUserInProgress1DoWaitPeerTrust(
        canceller: number,
        handle: number
    ): Promise<Result<UserGreetInProgress2Info, GreetInProgressError>>
    greeterDeviceInProgress1DoWaitPeerTrust(
        canceller: number,
        handle: number
    ): Promise<Result<DeviceGreetInProgress2Info, GreetInProgressError>>
    greeterUserInProgress2DoSignifyTrust(
        canceller: number,
        handle: number
    ): Promise<Result<UserGreetInProgress3Info, GreetInProgressError>>
    greeterDeviceInProgress2DoSignifyTrust(
        canceller: number,
        handle: number
    ): Promise<Result<DeviceGreetInProgress3Info, GreetInProgressError>>
    greeterUserInProgress3DoGetClaimRequests(
        canceller: number,
        handle: number
    ): Promise<Result<UserGreetInProgress4Info, GreetInProgressError>>
    greeterDeviceInProgress3DoGetClaimRequests(
        canceller: number,
        handle: number
    ): Promise<Result<DeviceGreetInProgress4Info, GreetInProgressError>>
    greeterUserInProgress4DoCreate(
        canceller: number,
        handle: number,
        human_handle: HumanHandle | null,
        device_label: DeviceLabel | null,
        profile: UserProfile
    ): Promise<Result<null, GreetInProgressError>>
    greeterDeviceInProgress4DoCreate(
        canceller: number,
        handle: number,
        device_label: DeviceLabel | null
    ): Promise<Result<null, GreetInProgressError>>
    testNewTestbed(
        template: string,
        test_server: BackendAddr | null
    ): Promise<Path>
    testGetTestbedOrganizationId(
        discriminant_dir: Path
    ): Promise<OrganizationID | null>
    testGetTestbedBootstrapOrganizationAddr(
        discriminant_dir: Path
    ): Promise<BackendOrganizationBootstrapAddr | null>
    testDropTestbed(
        path: Path
    ): Promise<null>
}
