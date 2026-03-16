# FastAPI Application Example

## Overview

This project demonstrates how to build a lightweight REST API using FastAPI.

It serves as a learning project focused on building modern Python APIs with automatic documentation and fast performance.

---

## Tech Stack

* Python
* FastAPI
* Uvicorn

---

## Features

* REST API endpoints
* Automatic API documentation
* High-performance async framework

---

## Installation

Clone the repository:

```bash
git clone https://github.com/RazAsraf7/FastAPI-App
cd FastAPI-App
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn main:app --reload
```

---

## API Documentation

Once the server is running, open:

```
http://localhost:8000/docs
```

FastAPI automatically generates interactive API documentation using Swagger UI.

---

## Example Endpoint

```
GET /
```

Response:

```
{"message": "Hello World"}
```

---

## Purpose

The purpose of this project is to explore FastAPI and understand the fundamentals of building Python-based web APIs.
