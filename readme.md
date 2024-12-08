# InsightBot: NLP Powered AI ChatBot
Dive deep into various machine learning tasks using the Pycaret library. Each notebook in this repository showcases a different machine learning problem and how it can be solved using Pycaret. 

## Team

- **Soumya Bharathi Vetukuri**
- **Rutuja Patil**
- **Shubham Kothiya**
- **Mann Nada**

### **Together, we aim to revolutionize the student experience through AI-driven solutions!**

---

## Objectives
- Providing Instant Assistance: Offering real-time responses to student queries related to academics, campus resources, events, and administrative services.
- Centralizing Information: Acting as a single point of contact for all university-related inquiries, eliminating the need to navigate multiple platforms or resources.
- Improving Efficiency: Reducing response times for common student concerns, such as course schedules, fee payment processes, and exam details, thereby enhancing productivity.
- Personalized Support: Utilizing AI to provide customized recommendations, such as suggesting campus events, academic resources, or career opportunities based on user input.
- Enhancing Student Experience: Simplifying the resolution of common challenges faced by students and improving their overall satisfaction with university services.



## Key Features

- **Real-Time Assistance**: Offers instant responses to student queries related to courses, fees, schedules, and more.
- **Centralized Information**: Serves as a single point of contact for all university-related information, eliminating platform navigation hassle.
- **Personalized Recommendations**: Suggests resources, events, and opportunities tailored to individual users.
- **Efficiency Boost**: Streamlines common student processes, improving productivity and satisfaction.
- **Google Calendar Integration**: Simplifies event scheduling through direct Google Calendar access.

---


## High level architecture


### 1. **User Authentication**
   - **Login Options**: User credentials or Google OAuth-based Single Sign-On (SSO).

### 2. **User Interface**
   - **Chatbot Interface**: Intuitive query-response design for seamless interaction.
   - **Features**:
     - Uses Axios for HTTP POST requests to interact with FastAPI backend.
     - Displays AI-generated replies in real time.
     - Includes a dedicated button for event scheduling via Google Calendar.

### 3. **FastAPI Backend**
   - **High-Performance API Framework**:
     - Facilitates communication between UI and server.
     - Automatic validation, type inference, and API documentation.

### 4. **Server-Side RAG (Retrieval-Augmented Generation)**
   - **AI Framework**:
     - Combines large language models with retrieval systems for precise and relevant responses.
     - Steps:
       1. **Information Retrieval**: Queries external data (databases, knowledge bases, web).
       2. **Pre-Processing**: Cleans and structures retrieved data.
       3. **Integration**: Integrates processed data with language models.

### 5. **Database**
   - **MongoDB Cluster**:
     - Stores cleaned and structured university-related information.
     - Organized into collections for efficient querying and retrieval.

### 6. **CI/CD Pipeline**
   - **Automation**:
     - GitHub as the code repository.
     - Jenkins integration for continuous integration and deployment.
     - Deployment to AWS-hosted Ubuntu servers.


## Technology Stack

| **Component**           | **Technology**           |
|--------------------------|--------------------------|
| **Frontend**            | React, Axios            |
| **Backend**             | FastAPI (Python)        |
| **Database**            | MongoDB , Pinecone                |
| **CI/CD**               | GitHub, Jenkins, AWS    |
| **AI Framework**        | Retrieval-Augmented Generation (RAG) |

---




## Demo

Experience InsightBot in action and discover how it simplifies student life.

---

Thank you for exploring **InsightBot**!


## How to Run the Project

Follow these steps to set up and run the InsightBot project:

1. **Install Requirements**  
   Install the necessary Python packages by running:  
   ```
   pip install -r requirements.txt 
   ```

2. **Configure MongoDB**
Add your MongoDB connection key to the .env file.

3. **Run the Webserver**
Start the webserver using the following command:
```
uvicorn main:app --reload
```

4. **Test API Endpoints**
Use the FastAPI interface to test the chatbot functionality.

Endpoint:
```
POST http://127.0.0.1:8000/query
```
Request Body (JSON):
```
{
  "queries": ["what is office hours of hammer theatre?"]
}
```





