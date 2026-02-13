---
name: backend-skill
description: Generate backend routes, handle HTTP requests and responses, and connect applications to databases securely and efficiently.
---

# Backend Skill – API & Database Handling

## Instructions

1. **Routing**
   - Define RESTful or RPC-style routes
   - Use clear and consistent endpoint naming
   - Separate public and protected routes

2. **Request & Response Handling**
   - Parse and validate incoming requests
   - Handle query params, path params, headers, and body
   - Return structured and meaningful HTTP responses
   - Use proper status codes (200, 201, 400, 401, 404, 500)

3. **Database Integration**
   - Connect to databases using secure credentials
   - Perform CRUD operations safely
   - Use ORM/ODM or query builders when appropriate
   - Handle connection pooling and errors gracefully

## Best Practices
- Validate all inputs before processing
- Keep controllers thin and move logic to services
- Use async/await with proper error handling
- Never expose sensitive data in responses
- Use environment variables for secrets
- Log errors without leaking internal details

## Example Structure
```js
// routes/user.routes.js
import express from "express";
import { createUser, getUser } from "../controllers/user.controller.js";

const router = express.Router();

router.post("/users", createUser);
router.get("/users/:id", getUser);

export default router;
