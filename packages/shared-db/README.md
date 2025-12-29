# Shared Database

Reusable database utilities, schemas, and migration templates for PostgreSQL with Row Level Security (RLS).

## Features

- 🗄️ Common database schemas (users, audit logs)
- 🔒 Row Level Security (RLS) policies
- 🔄 Alembic migration templates
- ⚡ Async SQLAlchemy setup
- 🛡️ RLS context helpers

## Structure

```
shared-db/
├── schemas/               # SQL schema files
│   ├── 00_extensions.sql  # PostgreSQL extensions
│   ├── 01_users.sql       # User table (required for all apps)
│   ├── 02_rls_base.sql    # Base RLS policies
│   └── functions.sql      # Helper functions
├── utils/                 # Python utilities
│   ├── connection.py      # Database connection setup
│   ├── rls.py             # RLS helper functions
│   └── base_model.py      # Base SQLAlchemy model
└── migrations/            # Alembic templates
```

## Usage in Applications

### 1. Python Backend Setup

```python
# app/core/database.py
from shared_db.utils.connection import create_async_engine, get_session_maker
from shared_db.utils.base_model import Base

# Create engine using shared utility
engine = create_async_engine(DATABASE_URL)
SessionLocal = get_session_maker(engine)

# Use shared base model
from shared_db.models import User  # Common User model
```

### 2. Initialize Database

```bash
# Run shared schemas first
psql $DATABASE_URL -f packages/shared-db/schemas/00_extensions.sql
psql $DATABASE_URL -f packages/shared-db/schemas/01_users.sql
psql $DATABASE_URL -f packages/shared-db/schemas/02_rls_base.sql

# Then run app-specific schemas
psql $DATABASE_URL -f apps/your-app/backend/database/init/*.sql
```

### 3. Use RLS Helpers

```python
from shared_db.utils.rls import set_rls_context, clear_rls_context

async def protected_endpoint(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Set RLS context for this session
    await set_rls_context(db, current_user.id)

    # Now all queries respect RLS policies
    sessions = await db.execute(select(ChatSession))
    return sessions.scalars().all()
```

## Shared Schemas

### Users Table (Required)

All apps must use the shared `users` table:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    full_name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);
```

### RLS Policies

Standard RLS policies provided:
- Users can only see their own profile
- Users can update their own profile
- Cross-app data isolation via `app.user_id` context

## Extending for Your App

### App-Specific Tables

```sql
-- apps/your-app/backend/database/init/01_app_tables.sql

-- Reference the shared users table
CREATE TABLE your_app_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Enable RLS
ALTER TABLE your_app_data ENABLE ROW LEVEL SECURITY;

-- Use shared RLS pattern
CREATE POLICY your_app_data_select_own ON your_app_data
    FOR SELECT
    USING (user_id = current_setting('app.user_id', true)::UUID);
```

## Database Connection

```python
# Shared connection utility
from shared_db.utils.connection import (
    create_async_engine,
    get_session_maker,
    get_db  # FastAPI dependency
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

@app.get("/items")
async def get_items(db: AsyncSession = Depends(get_db)):
    # Use database session
    ...
```

## Migrations

Use Alembic with shared base:

```python
# alembic/env.py
from shared_db.utils.base_model import Base
from shared_db.models import User  # Import shared models

# Import app-specific models
from app.models import YourModel

target_metadata = Base.metadata
```

## Environment Variables

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

## Best Practices

1. **Always use shared users table** - Don't create app-specific user tables
2. **Extend, don't modify** - App tables can reference shared tables but shouldn't modify them
3. **Use RLS context** - Always set user context for proper data isolation
4. **Consistent naming** - Follow snake_case for tables, camelCase for Python models
