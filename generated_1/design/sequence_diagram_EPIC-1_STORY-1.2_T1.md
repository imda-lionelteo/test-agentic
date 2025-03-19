```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant LoginService
    participant Database

    User ->> WebUI: Open login page
    WebUI ->> LoginService: Submit credentials
    LoginService ->> Database: Validate credentials
    Database -->> LoginService: Return user record
    LoginService ->> WebUI: Return login success
    WebUI ->> User: Show user dashboard
```