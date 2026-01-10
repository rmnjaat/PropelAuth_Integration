# FastAPI PropelAuth Integration

A clean and robust integration of **PropelAuth** with **FastAPI**. This project demonstrates how to manage users and secure endpoints using PropelAuth's powerful authentication and authorization services.

## 🚀 Features

- **PropelAuth Integration**: Full integration with PropelAuth for handling authentication and user management.
- **Secure Endpoints**: Implementation of security dependencies to protect routes.
- **User Management**: APIs to create, update, and delete users via PropelAuth's backend API.
- **Service-Repository Pattern**: Clean code structure following the service and repository design patterns.
- **Request Context**: Custom middleware/context management to pass user information across the request lifecycle.

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Authentication**: [PropelAuth](https://www.propelauth.com/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/latest/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)

## 📋 Prerequisites

- Python 3.9+
- A PropelAuth account and project set up.
- PropelAuth **Auth URL** and **API Key**.

## ⚙️ Configuration

Create a `.env` file in the root directory and add your PropelAuth credentials:

```env
AUTH_URL=your_propelauth_auth_url
AUTH_KEY=your_propelauth_api_key
```

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd PropelAuth_Integration
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install propelauth-py  # Ensure propelauth-py is installed
   ```

3. **Run the application**:
   ```bash
   python main.py
   # OR
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## 📡 API Endpoints

### Authentication
- `POST /auth/logout`: Invalidate the current session (Requires `X-AUTH-TOKEN` header).

### User Management
- `GET /user/health`: Check the status of the user management service.
- `POST /user/create`: Create a new user in PropelAuth.
- `PUT /user/{user_id}`: Update existing user details (e.g., role, properties).
- `DELETE /user/{user_id}`: Remove a user from the system.

## 🔒 Security

This project uses a custom header `X-AUTH-TOKEN` for authentication. The `AuthenticateUser` class validates the token against PropelAuth and populates the request context with the user's information.

## 🧠 How the PropelAuth Integration Works

### 1. Unified Authentication Provider
We use a singleton `Auth_provider` class (in `packages/auth_provider.py`) to initialize the PropelAuth Python SDK. This ensures the connection is established once and reused throughout the application.

```python
# packages/auth_provider.py
self.auth_v2 = init_base_auth(self.auth_url, self.auth_key)
```

### 2. FastAPI Security Dependencies
Authentication is handled via a dedicated security class `AuthenticateUser`. It:
- Extracts the token from the `X-AUTH-TOKEN` header.
- Uses `auth_v2.validate_access_token_and_get_user(token)` to verify the user.
- Injects the authenticated `User` object into the request.

### 3. User Management (B2B/SaaS focus)
The system is built to handle complex user operations beyond simple login:
- **Creation**: Users are created in PropelAuth and simultaneously added to a specific **Organization** with a defined **Role**.
- **Metadata Update**: User profile information like Name and Email are synced with PropelAuth's database.
- **RBAC Transition**: Roles within organizations (e.g., changing a "Member" to an "Admin") can be updated via the `/user/{user_id}` endpoint.
- **Session Management**: The logout function leverages `logout_all_user_sessions` to ensure security across all devices.

### 4. Dependency Injection
All PropelAuth-related services are injected using the `injector` library, keeping the logic decoupled from the web framework. This allows you to easily swap the `auth_provider` or repository handlers for testing.

## 📅 Coming SOON

- [ ] **Google-based Authentication**: Social login integration.
- [ ] **Single Sign-On (SSO)**: Support for enterprise-level SSO.



