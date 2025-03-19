```mermaid
flowchart LR
  UI[User Interface]
  API[API Gateway]
  AuthService[Authentication Service]
  TRService[Tuition Request Service]
  TutorService[Tutor Service]
  MatchService[Matching Service]
  NotifService[Notification Service]
  DB[Database]
  OAuth[OAuth Providers]
  Email[Email Service]
  Geo[Geolocation API]
  FileStorage[File Storage]
  Caching[Caching Service]
  Queue[Message Queue]

  UI -- API
  API -- AuthService
  API -- TRService
  API -- TutorService
  API -- MatchService
  API -- NotifService

  AuthService -- DB
  AuthService -- OAuth
  AuthService -- Email

  TRService -- DB
  TRService -- Geo

  TutorService -- DB
  TutorService -- FileStorage

  MatchService -- DB
  MatchService -- Caching

  NotifService -- Queue
  NotifService -- Email
```