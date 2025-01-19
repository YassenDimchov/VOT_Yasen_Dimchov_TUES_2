# File Management System - Setup Instructions

This repository provides a **File Management System** with **Keycloak** authentication and file upload functionality. The system uses **Keycloak** for identity and access management, **Docker** for containerization, and **Postman** for API testing.

---

## Prerequisites

To set up and test the system, you'll need the following:

### Tools

- **Docker** (for containerization)
- **Docker Compose** (for orchestration of multi-container environments)
- **Postman** (for API testing)
- **PowerShell** or **Terminal** (for command-line access)
- **Keycloak** (to manage authentication and authorization)

### Software

Ensure you have the following installed on your machine:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/) based on your operating system.
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/).
- **Postman**: [Download Postman](https://www.postman.com/downloads/).
- **PowerShell / Terminal**: Use the default terminal/command prompt on Windows, or **PowerShell** (Windows) or **Terminal** (macOS/Linux).

### Keycloak

The **File Management System** uses **Keycloak** for authentication. It must be running in a Docker container.

---

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/your-username/file-management-system.git
cd file-management-system
```
### 2. Set Up Docker Containers
In the root of this project, there should be a docker-compose.yml file. It defines the necessary containers, such as Keycloak and the File Management System.

Run Docker Compose to start Keycloak and the application services:
```bash
docker-compose up
```
This will:

- Start a Keycloak server.
- Start the File Management System backend.
- Expose Keycloak at http://localhost:8080/ and the File Management API at http://localhost:5000/.
### 3. Access Keycloak
#### 1. Open your browser and go to http://localhost:8080/.

#### 2. Log in with the default admin credentials:

- **Username**: admin
- **Password**: admin

#### 3. You can now configure the File Management System client and roles:

- Go to the Realm Settings and ensure that the roles for file management are set up correctly.
- Add a Client (file-management-client) if it doesn't already exist.
### 4. Generate Bearer Token (For API Authorization)
To interact with the File Management API, you need an access token from Keycloak. You can use Postman or a script to generate the token:

**Using Postman**

#### 1.Create a new POST request to the token endpoint:

- URL: http://localhost:8080/realms/<realm-name>/protocol/openid-connect/token
- Set Body type to x-www-form-urlencoded.
- Add the following parameters:
  - grant_type: client_credentials
  - client_id: file-management-client
  - client_secret: <your-client-secret>
#### 2.After sending the request, you should get a response with an access_token.
**Using PowerShell**

Run the following PowerShell command to get a bearer token:

```bash
$uri = "http://localhost:8080/realms/<realm-name>/protocol/openid-connect/token"
$body = @{
    grant_type    = "client_credentials"
    client_id     = "file-management-client"
    client_secret = "<your-client-secret>"
}

$response = Invoke-RestMethod -Uri $uri -Method Post -ContentType "application/x-www-form-urlencoded" -Body $body
$access_token = $response.access_token
$access_token
```

### 5. Use Postman to Test APIs
#### 1.Open Postman and create a new POST request for file upload:

- URL: http://localhost:5000/upload
- Set Headers to:
  - Authorization: Bearer <your-access-token>
- Set Body to form-data and upload a file:
  - Key: file
  - Value: Choose a file to upload (e.g., example.txt).
#### 2.Send the request. If the file is uploaded successfully, you'll receive a confirmation response.

## Docker Commands
- To start the services:
```bash
docker-compose up
```
- To stop the services:
```bash
docker-compose down
```