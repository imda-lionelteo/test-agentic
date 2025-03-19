```mermaid
sequenceDiagram
    participant Tutor
    participant WebUI
    participant OfferManagementService
    participant Database

    Tutor ->> WebUI: Request to view received offers
    WebUI ->> OfferManagementService: Fetch received offers
    OfferManagementService ->> Database: Retrieve offers data
    Database -->> OfferManagementService: Return offers list
    OfferManagementService ->> WebUI: Deliver offers data
    WebUI ->> Tutor: Display offers dashboard
```