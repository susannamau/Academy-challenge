# Academy-challenge


# Structure of the App

```mermaid
graph TB
    A[Home: quale task vuoi performare?] --> B[Question Answering]
    A --> B2[Comparison of files]
    A --> B3[Admin]

    B --> C[Upload a file]
    C --> D[Ask a question]
    D --> E[Recent files]
    E --> F[Provide feedback]

    B2 --> G[Upload file 1]
    G --> H[Upload file 2]
    H --> I[Find differences]
    I --> J[Provide feedback]

    B3 --> K{Login}
    K -- Successful --> L[Admin dashboard]
    K -- Unsuccessful --> M[Invalid credentials]
    L --> N[Average user feedback]
    N --> O[Average response time]
    O --> P[Scatterplot Response Word Count x Response Time]
    P --> Q[Barplot User feedback]
    Q --> R[Table of files with feedback 1 or 2]
