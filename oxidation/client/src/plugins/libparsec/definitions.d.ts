// Parsec Cloud (https://parsec.cloud) Copyright (c) BUSL-1.1 (eventually AGPL-3.0) 2016-present Scille SAS

/*
 * /!\ Auto-generated code (see `bindings/generator`), any modification will be lost ! /!\
 */

export type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

type OrganizationID = string;
type DeviceLabel = string;
type HumanHandle = string;
type Path = string;
type StrPath = string;
type BackendAddr = string;
type DeviceID = string;
type LoggedCoreHandle = number;
type ClientHandle = number;

export interface ClientConfig {
    configDir: Path;
    dataBaseDir: Path;
    mountpointBaseDir: Path;
    preferredOrgCreationBackendAddr: BackendAddr;
    workspaceStorageCacheSize: WorkspaceStorageCacheSize;
}

// ClientEvent
export interface ClientEventClientConnectionChanged {
    tag: 'ClientConnectionChanged'
    client: number;
}
export interface ClientEventWorkspaceReencryptionEnded {
    tag: 'WorkspaceReencryptionEnded'
}
export interface ClientEventWorkspaceReencryptionNeeded {
    tag: 'WorkspaceReencryptionNeeded'
}
export interface ClientEventWorkspaceReencryptionStarted {
    tag: 'WorkspaceReencryptionStarted'
}
export type ClientEvent =
  | ClientEventClientConnectionChanged
  | ClientEventWorkspaceReencryptionEnded
  | ClientEventWorkspaceReencryptionNeeded
  | ClientEventWorkspaceReencryptionStarted

// WorkspaceStorageCacheSize
export interface WorkspaceStorageCacheSizeCustom {
    tag: 'Custom'
    size: number;
}
export interface WorkspaceStorageCacheSizeDefault {
    tag: 'Default'
}
export type WorkspaceStorageCacheSize =
  | WorkspaceStorageCacheSizeCustom
  | WorkspaceStorageCacheSizeDefault

// DeviceAccessParams
export interface DeviceAccessParamsPassword {
    tag: 'Password'
    path: Path;
    password: string;
}
export interface DeviceAccessParamsSmartcard {
    tag: 'Smartcard'
    path: Path;
}
export type DeviceAccessParams =
  | DeviceAccessParamsPassword
  | DeviceAccessParamsSmartcard

// ClientLoginError
export interface ClientLoginErrorAccessMethodNotAvailable {
    tag: 'AccessMethodNotAvailable'
}
export interface ClientLoginErrorDecryptionFailed {
    tag: 'DecryptionFailed'
}
export interface ClientLoginErrorDeviceAlreadyLoggedIn {
    tag: 'DeviceAlreadyLoggedIn'
}
export interface ClientLoginErrorDeviceInvalidFormat {
    tag: 'DeviceInvalidFormat'
}
export type ClientLoginError =
  | ClientLoginErrorAccessMethodNotAvailable
  | ClientLoginErrorDecryptionFailed
  | ClientLoginErrorDeviceAlreadyLoggedIn
  | ClientLoginErrorDeviceInvalidFormat

export interface LibParsecPlugin {
    clientLogin(
        load_device_params: DeviceAccessParams,
        config: ClientConfig,
        on_event_callback: (ClientEvent) => void
    ): Promise<Result<number, ClientLoginError>>;
}
