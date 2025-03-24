```mermaid
sequenceDiagram
    participant System
    participant NotificationService
    participant EmailService
    participant InAppService
    participant DB as Database

    System->>NotificationService: Trigger Notification Event
    NotificationService->>DB: Log Notification Event
    NotificationService->>NotificationService: Scan for New Events
    NotificationService->>DB: Retrieve Email Template
    DB-->>NotificationService: Return Email Template
    NotificationService->>EmailService: Send Email Notification
    EmailService-->>NotificationService: Confirm Email Sent
    NotificationService->>InAppService: Send In-App Notification
    InAppService-->>NotificationService: Confirm In-App Notification Sent
    NotificationService->>DB: Update Notification Status
    NotificationService->>NotificationService: Check for Retry Events
    NotificationService->>NotificationService: Apply Rate Limiting
```