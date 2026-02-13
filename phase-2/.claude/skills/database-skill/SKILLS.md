---
name: database-skill
description: Design and manage database schemas, tables, and migrations. Use for data modeling and persistence layers.
---

# Database Skill – Schema Design & Migrations

## Instructions

1. **Schema design**
   - Identify entities and relationships
   - Normalize tables appropriately
   - Define primary and foreign keys
   - Choose correct data types

2. **Table creation**
   - Create scalable and readable table structures
   - Apply indexes for frequently queried fields
   - Enforce constraints (NOT NULL, UNIQUE, CHECK)
   - Use naming conventions consistently

3. **Migrations**
   - Write forward and rollback migrations
   - Keep migrations atomic and reversible
   - Avoid destructive changes without backups
   - Version and document schema changes

## Best Practices
- Prefer explicit schemas over implicit defaults  
- Use migrations for all schema changes  
- Index only when needed to avoid overhead  
- Keep schemas backward-compatible when possible  
- Separate concerns between data, logic, and views  

## Example Structure
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
