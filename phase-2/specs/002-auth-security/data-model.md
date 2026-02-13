# Data Model: Auth Security

## User Entity

### User
- **id**: UUID (Primary Key)
  - Unique identifier for the user
  - Generated as UUID4
  - Immutable after creation
- **email**: String (Required, Unique, Max 255 chars)
  - User's email address
  - Used for login and identification
  - Validated as proper email format
- **hashed_password**: String (Required)
  - Bcrypt hashed password
  - Never stored in plaintext
  - Updated when password changes
- **created_at**: DateTime (Required)
  - Timestamp of user creation
  - Auto-generated on creation
  - Immutable after creation
- **updated_at**: DateTime (Required)
  - Timestamp of last update
  - Auto-updated on modification
  - Updated on each change
- **is_active**: Boolean (Default: True)
  - Flag indicating if account is active
  - Used to deactivate accounts
  - Can be toggled by admin or user

## Authentication Token Entities

### JWT Access Token
- **payload**: Object
  - Contains user identity claims
  - `sub`: User ID (UUID)
  - `email`: User email address
  - `iat`: Issued at timestamp
  - `exp`: Expiration timestamp
- **signature**: String
  - HMAC SHA256 signature
  - Verified against secret key
  - Ensures token integrity
- **expiration**: DateTime
  - Token validity period
  - Typically 15-30 minutes
  - Enforces short-lived tokens

### Refresh Token
- **id**: UUID (Primary Key)
  - Unique identifier for the refresh token
  - Generated as UUID4
  - Immutable after creation
- **user_id**: UUID (Foreign Key)
  - Reference to associated user
  - Links token to user account
  - Enables token revocation per user
- **token_hash**: String (Required)
  - Bcrypt hash of the refresh token
  - Never stores raw token
  - Prevents token theft
- **expires_at**: DateTime (Required)
  - Expiration timestamp
  - Typically 7 days from issue
  - Enforces token rotation
- **revoked**: Boolean (Default: False)
  - Indicates if token is revoked
  - Used for immediate logout
  - Supports security measures
- **created_at**: DateTime (Required)
  - Timestamp of token creation
  - Used for rotation policies
  - Audit trail

## Session Entity (if needed)

### Session
- **id**: UUID (Primary Key)
  - Unique session identifier
  - Generated as UUID4
  - Immutable after creation
- **user_id**: UUID (Foreign Key)
  - Reference to authenticated user
  - Links session to user
  - Enables session management
- **session_token**: String (Required, Unique)
  - Encrypted session identifier
  - Stored as secure cookie
  - Enables persistent login
- **expires_at**: DateTime (Required)
  - Session expiration time
  - Typically 30 days from creation
  - Enforces automatic logout
- **last_activity**: DateTime (Required)
  - Last interaction timestamp
  - Updated periodically
  - Supports idle timeout
- **user_agent**: String (Optional)
  - Browser/device information
  - Used for security checks
  - Helps detect suspicious activity
- **ip_address**: String (Optional)
  - IP address at creation
  - Used for security checks
  - Helps detect suspicious activity
- **is_active**: Boolean (Default: True)
  - Active session indicator
  - Disabled on logout
  - Supports forced logout
- **created_at**: DateTime (Required)
  - Session creation timestamp
  - Auto-generated on creation
  - Audit trail
- **updated_at**: DateTime (Required)
  - Last update timestamp
  - Auto-updated on modification
  - Updated on activity