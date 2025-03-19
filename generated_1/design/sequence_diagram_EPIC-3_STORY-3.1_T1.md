```mermaid
sequenceDiagram
    participant Tutor
    participant WebUI
    participant TutorProfileService
    participant FileStorage
    participant Database

    Tutor ->> WebUI: Open tutor profile creation form
    WebUI ->> TutorProfileService: Submit profile details
    TutorProfileService ->> FileStorage: Upload files if provided
    TutorProfileService ->> Database: Save tutor profile details
    Database -->> TutorProfileService: Confirm save
    TutorProfileService ->> WebUI: Return creation success
    WebUI ->> Tutor: Display profile confirmation
```