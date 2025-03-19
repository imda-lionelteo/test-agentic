```mermaid
sequenceDiagram
    participant NotificationService
    participant EmailService
    participant Database

    NotificationService->>NotificationService: triggerBackgroundNotification()
    NotificationService->>Database: fetchNewOffers()
    Database-->>NotificationService: listOfOffers
    NotificationService->>EmailService: sendEmailNotification(listOfOffers)
    EmailService-->>NotificationService: emailSentConfirmation
    NotificationService->>Database: updateOfferStatus('notified')
    NotificationService-->>NotificationService: logNotificationAttempt
```