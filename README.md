# Academy-challenge


# Structure of the App

```mermaid
graph TB
    A[Home: quale task vuoi performare?] --> B[Question Answering]
    A --> B2[Comparison of files]
    A --> B3[Admin]

    B --> C[Upload a file]
    B --> D[Ask a question]
    B --> E[Recent files]
    B --> F[Provide feedback]

    B2 --> G[Upload file 1]
    B2 --> H[Upload file 2]
    B2 --> I[Find differences]
    B2 --> J[Provide feedback]

    B3 --> K{Login}
    K -- Successful --> L[Admin dashboard]
    K -- Unsuccessful --> M[Invalid credentials]
    L --> N[Average user feedback]
    L --> O[Average response time]
    L --> P[Scatterplot Response Word Count x Response Time]
    L --> Q[Barplot User feedback]
    L --> R[Table of files with feedback 1 or 2]
