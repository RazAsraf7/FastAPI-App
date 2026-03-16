# DoMyDuda – FastAPI Backend Service 🚀

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248.svg?logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?logo=docker&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939.svg?logo=jenkins&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5.svg?logo=kubernetes&logoColor=white)

## 📖 Overview
**DoMyDuda** is a robust backend service designed to manage application data through a modern REST API. 

This project goes beyond simple API development, demonstrating a complete, production-ready backend architecture. It integrates **FastAPI** for high-performance routing, **MongoDB** for data persistence, comprehensive unit testing with **Pytest**, and a full DevOps pipeline featuring **Docker** containerization, **Kubernetes** orchestration, and **Jenkins** CI/CD automation.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python)
* **Database:** MongoDB
* **Testing:** Pytest
* **Containerization:** Docker
* **Orchestration:** Kubernetes (Helm ready)
* **CI/CD:** Jenkins
* **Security:** Password Hashing integrated

## ✨ Features
* **RESTful API:** Efficient endpoints for managing and retrieving application data.
* **Database Integration:** Persistent data storage using MongoDB architecture.
* **Security:** Implemented user authentication with hashed passwords.
* **Automated Testing:** Dedicated Pytest suite (`test_DMD.py`) with user creation validation.
* **DevOps & CI/CD:** Ready-to-use `Jenkinsfile` for automated pipelines and Kubernetes manifests (`build-pod.yaml`, `mongodb-architecture.yaml`) for cluster deployment.
* **Containerized Environment:** Custom `Dockerfile` for seamless deployment across environments.

## 📂 Project Structure

```text
FastAPI-App
│
├── domyduda/                   # Core application logic and modules
├── MongoDB/                    # MongoDB related configurations
├── templates/                  # HTML templates for rendering
├── DMD.py                      # Main Application Entry Point (FastAPI app)
├── test_DMD.py                 # Pytest suite for automated testing
├── Dockerfile / Dockerfile1    # Docker images configuration (including Helm/Kubectl setup)
├── Jenkinsfile                 # CI/CD Pipeline definition
├── build-pod.yaml              # Kubernetes pod configuration
├── mongodb-architecture.yaml   # Kubernetes architecture for MongoDB
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables (e.g., ROOT_USERNAME)
