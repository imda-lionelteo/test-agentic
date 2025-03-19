```mermaid
sequenceDiagram
    participant Tutor
    participant WebUI
    participant OfferAcceptanceService
    participant Database

    Tutor ->> WebUI: Select offers to accept
    WebUI ->> OfferAcceptanceService: Confirm acceptance
    OfferAcceptanceService ->> Database: Update offer status to accepted
    Database -->> OfferAcceptanceService: Acknowledge update
    OfferAcceptanceService ->> WebUI: Return confirmation
    WebUI ->> Tutor: Display updated offer status
```