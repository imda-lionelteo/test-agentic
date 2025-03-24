```mermaid
sequenceDiagram
    participant Tutor
    participant TutorUI as Tutor UI
    participant TutorService
    participant DB as Database
    participant NotificationService
    participant MappingService

    Tutor->>TutorUI: Fill Out Profile Form
    TutorUI->>TutorUI: Preview Profile
    Tutor->>TutorUI: Submit Profile
    TutorUI->>TutorService: Send Profile Data
    TutorService->>DB: Store Profile Data
    TutorService->>TutorUI: Confirm Profile Submission
    TutorUI-->>Tutor: Display Confirmation Message
    Tutor->>TutorUI: Access Dashboard
    TutorUI->>TutorService: Retrieve Offers
    TutorService->>DB: Fetch Offers
    DB-->>TutorService: Return Offers
    TutorService->>TutorUI: Send Offers
    TutorUI-->>Tutor: Display Offers
    Tutor->>TutorUI: Respond to Offer
    TutorUI->>TutorService: Send Response
    TutorService->>NotificationService: Trigger Notification
    NotificationService->>Tutor: Send Notification
    TutorService->>MappingService: Update Mapping Data
    MappingService-->>TutorService: Confirm Update
```