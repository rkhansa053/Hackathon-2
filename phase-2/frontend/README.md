# Todo App Frontend

A modern, responsive todo application with authentication built using Next.js 16+ with App Router.

## Features

- User authentication (sign up and sign in)
- Task management (create, read, update, delete)
- Responsive design for mobile and desktop
- Real-time task synchronization
- Loading states and error handling
- JWT-based authentication

## Tech Stack

- Next.js 16+ with App Router
- React 18+
- TypeScript
- Tailwind CSS
- Better Auth (for authentication)
- REST API for backend communication

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install dependencies:

```bash
npm install
```

### Environment Variables

Copy the example environment file and update with your configuration:

```bash
cp .env.example .env.local
```

Required variables:

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for your FastAPI backend

### Running the Development Server

```bash
npm run dev
```

The application will be available at http://localhost:3000

### Building for Production

```bash
npm run build
npm run start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication pages
│   │   ├── signup/
│   │   └── signin/
│   ├── dashboard/         # Protected dashboard
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable UI components
│   ├── auth/              # Authentication components
│   ├── tasks/             # Task management components
│   ├── ui/                # Base UI components
│   └── navigation/        # Navigation components
├── lib/                   # Utilities and API clients
│   ├── auth/              # Authentication utilities
│   ├── api/               # API client and functions
│   └── utils/             # Utility functions
├── types/                 # TypeScript type definitions
└── public/                # Static assets
```

## API Integration

The application communicates with the backend API through the centralized API client. All authenticated requests automatically include the JWT token when available.

Key API endpoints:
- `/api/auth/signup` - User registration
- `/api/auth/signin` - User authentication
- `/api/auth/signout` - User logout
- `/api/auth/profile` - Get user profile
- `/api/tasks` - Task management (GET, POST, PUT, DELETE)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
