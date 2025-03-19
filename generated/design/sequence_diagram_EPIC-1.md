```mermaid
sequenceDiagram
participant User
participant UI
participant Authenticator
participant DB
participant EmailService
participant OAuthService

%% Registration Flow
User ->> UI: Open registration form
UI ->> Authenticator: Submit registration details
Authenticator ->> DB: Create new user record
Authenticator ->> EmailService: Send welcome email
EmailService -->> User: Confirm email sent

%% Login Flow
User ->> UI: Enter login credentials
UI ->> Authenticator: Validate credentials
Authenticator ->> DB: Fetch user record
DB -->> Authenticator: Return user record
Authenticator -->> UI: Return login success
```