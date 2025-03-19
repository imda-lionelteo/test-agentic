```mermaid
sequenceDiagram
    participant Requester
    participant WebUI
    participant SearchService
    participant Database

    Requester ->> WebUI: Select tuition request for tutor match
    WebUI ->> SearchService: Trigger tutor search with filters
    SearchService ->> Database: Query tutor profiles based on criteria
    Database -->> SearchService: Return list of matching tutors
    SearchService ->> WebUI: Deliver tutor profiles
    WebUI ->> Requester: Display matching tutors
```