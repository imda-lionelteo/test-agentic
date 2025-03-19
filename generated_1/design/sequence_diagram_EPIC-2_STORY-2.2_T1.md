```mermaid
sequenceDiagram
    participant Requester
    participant WebUI
    participant RequestService
    participant Database

    Requester ->> WebUI: Request dashboard view
    WebUI ->> RequestService: Retrieve tuition requests
    RequestService ->> Database: Fetch requests
    Database -->> RequestService: Return requests list
    RequestService ->> WebUI: Return paginated list
    WebUI ->> Requester: Display dashboard
```