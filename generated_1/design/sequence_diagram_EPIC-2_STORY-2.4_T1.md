```mermaid
sequenceDiagram
    participant Requester
    participant WebUI
    participant OfferService
    participant Database
    participant NotificationQueue

    Requester ->> WebUI: Select tutors and send offer
    WebUI ->> OfferService: Process send offer action
    OfferService ->> Database: Create offer entries with status 'new'
    Database -->> OfferService: Confirm offer creation
    OfferService ->> NotificationQueue: Enqueue notifications
    NotificationQueue -->> OfferService: Notification queued
    OfferService ->> WebUI: Return success message
    WebUI ->> Requester: Display offer sent confirmation
```