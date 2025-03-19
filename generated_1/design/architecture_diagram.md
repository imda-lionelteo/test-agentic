```mermaid
flowchart LR
    WebUI[Web UI]
    AuthService[Authentication Service]
    RequestService[Tuition Request Service]
    TutorService[Tutor Management Service]
    NotificationService[Notification Service]
    MatchService[Match-making Service]
    Database[Database]
    OIDC[OIDC Providers]
    Email[Email Service]
    Geolocation[Geolocation API]
    FileStorage[Secure File Storage]
    Caching[Caching Service]

    WebUI --- AuthService : Uses
    WebUI --- RequestService : Uses
    WebUI --- TutorService : Uses
    AuthService --- Database : Reads/Writes
    RequestService --- Database : Reads/Writes
    TutorService --- Database : Reads/Writes
    NotificationService --- Email : Sends notifications
    NotificationService --- Database : Updates status
    MatchService --- Database : Reads data
    RequestService --- Geolocation : Uses
    TutorService --- FileStorage : Manages uploads
    AuthService --- OIDC : Integrates
    RequestService --- Caching : Caches queries
    MatchService --- Caching : Uses cache
```