# Quickstart Guide: Frontend Web Application

## Prerequisites

- Node.js 18.x or higher
- npm or yarn package manager
- Access to the FastAPI backend service
- Git for version control

## Environment Setup

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd <project-directory>
   cd frontend  # Navigate to frontend directory
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**:
   Copy the example environment file and update with your configuration:
   ```bash
   cp .env.example .env.local
   ```

   Update the following variables:
   - `NEXT_PUBLIC_API_BASE_URL`: Base URL for your FastAPI backend
   - `NEXT_PUBLIC_BETTER_AUTH_URL`: URL for Better Auth service (usually the same as API URL)

## Running the Application

### Development Mode

Start the development server:
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

### Production Build

To build and serve the application in production:
```bash
npm run build
npm run start
```

## Key Features and Navigation

### Authentication Flow
1. Visit `/signup` to create a new account
2. Use `/signin` to log in to an existing account
3. Protected routes automatically redirect unauthenticated users to login

### Task Management
1. After authentication, visit `/dashboard` to manage tasks
2. Create new tasks using the "Add Task" form
3. Toggle completion status with the checkbox
4. Edit or delete existing tasks as needed

## Development Commands

- `npm run dev` - Start development server with hot reloading
- `npm run build` - Create production build
- `npm run start` - Start production server
- `npm run lint` - Run ESLint to check for code issues
- `npm run test` - Run unit tests
- `npm run test:e2e` - Run end-to-end tests

## API Integration

The application connects to the backend API through the centralized client located at `src/lib/api/client.ts`. All API calls automatically include the JWT token when available.

Key API endpoints integrated:
- Authentication: `/api/auth/signup`, `/api/auth/signin`
- Tasks: `/api/tasks` (GET, POST, PUT, DELETE)

## Component Overview

### Authentication Components
- `AuthForm.tsx` - Generic authentication form component
- `LoginForm.tsx` - Specific login form implementation

### Task Components
- `TaskCard.tsx` - Individual task display and actions
- `TaskList.tsx` - Container for displaying multiple tasks
- `TaskForm.tsx` - Form for creating and editing tasks

### UI Components
- `Button.tsx` - Reusable button component
- `Input.tsx` - Form input with validation
- `Card.tsx` - Container for grouping related content

## Testing

Run unit tests:
```bash
npm run test:unit
```

Run integration tests:
```bash
npm run test:integration
```

Run end-to-end tests:
```bash
npm run test:e2e
```

## Troubleshooting

### Common Issues
- **API connection errors**: Verify NEXT_PUBLIC_API_BASE_URL is correctly set
- **Authentication issues**: Check that Better Auth is properly configured
- **Styling problems**: Ensure Tailwind CSS is properly configured
- **Environment variables not loading**: Make sure .env.local file exists and is correctly formatted

### Development Tips
- Use Next.js App Router conventions for new pages
- Import and use the API client for all backend communications
- Wrap protected routes with the AuthGuard component
- Follow the established component structure and naming conventions