---
name: auth-skill
description: Implement secure user authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Auth Skill – Secure Authentication

## Instructions

1. **Signup & Signin**
   - Implement user registration with validated inputs
   - Securely authenticate users with verified credentials
   - Prevent duplicate accounts and enumeration attacks

2. **Password Security**
   - Hash passwords using industry-standard algorithms (bcrypt, argon2)
   - Never store or log plain-text passwords
   - Safely compare hashed passwords during signin

3. **JWT Tokens**
   - Generate signed JWT access tokens
   - Validate tokens on protected routes
   - Handle token expiration and refresh strategies
   - Use secure secrets and proper algorithms

4. **Better Auth Integration**
   - Configure Better Auth correctly
   - Integrate signup, signin, and session handling
   - Follow Better Auth best practices and defaults
   - Ensure compatibility with existing auth flows

## Best Practices
- Always validate user input before processing
- Use HTTP-only, secure cookies when possible
- Set reasonable token expiration times
- Rotate secrets and tokens when compromised
- Avoid exposing sensitive auth errors
- Follow the principle of least privilege

## Example Structure
```ts
// Signup
const hashedPassword = await hash(password);
await createUser({ email, password: hashedPassword });

// Signin
const isValid = await compare(password, user.password);
if (!isValid) throw new AuthError();

// JWT
const token = signJwt({ userId: user.id });

// Middleware
verifyJwt(token);
