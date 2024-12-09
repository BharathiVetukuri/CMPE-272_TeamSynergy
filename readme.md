# InsightBot: NLP Powered AI ChatBot

## Overview

**InsightBot** is an advanced AI-powered chatbot designed to enhance the student experience by providing real-time assistance with university-related inquiries. From academics to campus events and administrative services, InsightBot centralizes information and reduces response times, ensuring a seamless and personalized user experience.

---

## 🌟 Team : Synergy

- **Soumya Bharathi Vetukuri**
- **Rutuja Patil**
- **Shubham Kothiya**
- **Mann Nada**

### **Together, we aim to revolutionize the student experience through AI-driven solutions!**

---
## 🎯 Objectives  

### ✅ **Required Features Implemented**
InsightBot has successfully integrated all the mandatory features to ensure seamless functionality and enhanced student interaction:

1. **Real-Time Query Resolution**:  
   - AI-powered responses for queries regarding academics, campus events, administrative services, and more.  

2. **Centralized Information Retrieval**:  
   - One-stop solution to access university-related information from multiple resources without platform-hopping.  

3. **Personalized Recommendations**:  
   - Tailored suggestions based on user activity and preferences for academic resources, campus events, and opportunities.  

4. **Google Calendar Integration**:  
   - Direct scheduling of events or reminders through Google Calendar for streamlined organization.  

5. **Secure Authentication**:  
   - User login via credentials or **Google OAuth-based Single Sign-On (SSO)**.

6. **Robust Backend API**:  
   - Built on **FastAPI**, ensuring high performance, scalability, and efficient data handling.  

7. **Advanced Database Setup**:  
   - **MongoDB** and **Pinecone** enable rapid and accurate information retrieval.  

8. **CI/CD Pipeline**:  
   - Automated integration and deployment using **GitHub Actions**, **Jenkins**, and hosting on **AWS Ubuntu servers**.

---

### 🌟 **Additional Features Highlighted**
Beyond the core functionalities, InsightBot offers several advanced and innovative features:

1. **Retrieval-Augmented Generation (RAG)**:  
   - Combines natural language models with powerful retrieval systems to provide precise, context-aware responses.  
   - Includes advanced pre-processing of retrieved data for better accuracy.  

2. **Optimized Chatbot UI**:  
   - Intuitive and user-friendly interface built with **React**, featuring real-time AI responses and seamless event scheduling via an integrated **Google Calendar button**.

3. **Custom Test Suite for Reliability**:  
   - Comprehensive test cases developed for critical endpoints like root API, query handling, and vector store processing.  
   - All tests passed successfully, ensuring stability and reliability.  

4. **Interactive API Documentation**:  
   - FastAPI's built-in API docs provide an easy-to-use interface for testing and interacting with the backend.

5. **Efficient Information Storage**:  
   - Leveraging **Pinecone's vector database** for efficient and rapid query processing.  

6. **Scalable Deployment**:  
   - Designed for scalability and high availability using AWS infrastructure and CI/CD pipelines.

7. **Extensibility for Future Enhancements**:  
   - Modular architecture allows easy integration of additional data sources or AI capabilities.  


---

## 🏗️ High-Level Architecture  

### 1. **User Authentication**  
- Login options: **Credentials** or **Google OAuth-based SSO**.  

### 2. **User Interface**  
- **Chatbot Design**: Clean and user-friendly interface.  
  - 🛠️ **Features**:
    - HTTP POST requests via Axios to interact with FastAPI backend.
    - Real-time AI-generated responses.
    - A dedicated **Google Calendar button** for event scheduling.  

### 3. **FastAPI Backend**  
- **High-Performance API Framework**:  
  - Handles communication between the UI and server.  
  - Features automatic validation, type inference, and built-in API docs.  

### 4. **Server-Side RAG (Retrieval-Augmented Generation)**  
- Combines **language models** and **retrieval systems** to provide accurate responses.  
  - 🔎 **Steps**:  
    1. **Information Retrieval**: Searches databases and external resources.  
    2. **Pre-Processing**: Cleans and structures retrieved data.
     <br> 
    <img src="DemoPictures/rag_1" alt="Alt Text" width="600" height="500">
     <br>
     
    3. **Integration**: Delivers precise responses using advanced AI models.  
     <br>
    <img src="DemoPictures/rag_phase2" alt="Alt Text" width="600" height="500">

    
### 5. **Database**  
- Powered by **MongoDB Cluster** and **Pinecone** for fast, efficient information retrieval.  

### 6. **CI/CD Pipeline**  
- **Automation Tools**:  
  - **GitHub** for code repository.  
  - **Jenkins** for integration and deployment.  
  - Deployed on **AWS-hosted Ubuntu servers**.  

---

## Test Cases & Results

The InsightBot project includes comprehensive functional tests to ensure the reliability and correctness of its components. 

 <img src="DemoPictures/testcases.png" alt="Alt Text" width="600" height="800">

### Test Cases
1. **Root Endpoint Test**  
   - **Description**: Validates the root endpoint to ensure the API responds with the expected welcome message and HTTP 200 status.

2. **Query Documents Test**  
   - **Description**: Tests the `/query/` endpoint to validate response structure, HTTP status, and successful query processing.

3. **Vector Store Test**  
   - **Description**: Evaluates the `query_vector_store()` function by verifying query processing, result accuracy, and specific content, such as office hours information.

### Test Results
All test cases passed successfully, demonstrating the stability and reliability of the InsightBot API and its underlying services. 
- Below is a screenshot of the test results:
<br>
<br>
<img src="DemoPictures/testpassed.png" alt="Alt Text" width="900" height="700">


### Running Tests
To run the tests, use the following command:
```bash
pytest
```



---
## 💡 Technology Stack  

| **Component**       | **Technology**           |  
|----------------------|--------------------------|  
| **Frontend**         | React, Axios             |  
| **Backend**          | FastAPI (Python)         |  
| **Database**         | MongoDB, Pinecone        |  
| **CI/CD**            | GitHub, Jenkins, AWS     |  
| **AI Framework**     | Retrieval-Augmented Generation (RAG) |  

---

## 🎥 Demo  

👀 **Coming Soon!** Experience InsightBot in action and see how it transforms student life.  

---

## ⚙️ How to Run InsightBot  

Follow these steps to get started:  

1. **📥 Install Requirements** 
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





