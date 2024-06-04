# Academy-challenge
## Final challenge of the BPER Academy
Authors: Susanna Maugeri & Riccardo Sparacino.

This is a web application built with Flask. The application allows users to upload files and ask questions and to compare two files to find differences between them.


## The features
The features implemented so far are:

* Question Answering
    * Upload a file
    * Ask a question using LLaMA3
    * See, download or delete recent uploaded files
    * Provide a feedback
* Comparison of two files
    * Upload file 1
    * Upload file 2
    * Find differences using LLaMA3 
    * Provide a feedback
* Admin dashboard
    * Login with admin credentials
    * See KPIs and statistics:
        * Average User Feedback
        * Average Response Time
        * Scatterplot Response Word Count x Response Time
        * Barplot of User Feedbacks
        * Table of the files to be checked because they got feedback 1 or 2

## The model
The underling model is [LLaMA3](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) by Meta and the API is implemented by [HuggingFace](https://huggingface.co/). 

## Requirements

To run this application, you will need Python and Flask. Also, an HuggingFace key is needed to query the LLM.

## Installation

Clone the repository to your local machine and navigate to the app directory.

Install the libraries in `requirements.txt`. 

When running `run.py`, by default the application will we available at `http://127.0.0.1:5000/`.


## Structure of the App

```mermaid
graph TB
    A[Home: what task do you want to perform?] --> B[Question Answering]
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
