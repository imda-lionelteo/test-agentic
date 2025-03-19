```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant RegistrationService
    participant Database
    participant EmailService

    User ->> WebUI: Open registration form
    WebUI ->> RegistrationService: Submit registration details
    RegistrationService ->> Database: Check email uniqueness
    Database -->> RegistrationService: Return check result
    RegistrationService ->> EmailService: Send welcome email
    EmailService -->> RegistrationService: Confirmation
    RegistrationService ->> WebUI: Registration successful
    WebUI ->> User: Display dashboard
```