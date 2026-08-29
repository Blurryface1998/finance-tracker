# Finance Tracker Frontend

The React frontend for Finance Tracker.

## Overview

The frontend provides:

- Public landing page
- User registration and login
- Protected application routes
- Dashboard layout
- Transaction management
- Financial analytics
- Profile functionality
- Responsive navigation

## Tech Stack

- React
- Vite
- React Router
- Axios
- React Hook Form
- SCSS
- ESLint

## Structure

```text
frontend/
├── src/
│   ├── app/
│   ├── assets/
│   ├── features/
│   ├── services/
│   ├── shared/
│   └── styles/
├── public/
├── package.json
├── vite.config.js
└── eslint.config.js
```

### Main Components

**App**

Contains application routing, layouts, and global providers.

**Features**

Organizes functionality by application domain, including authentication, transactions, analytics, overview, profile, and landing pages.

**Services**

Contains API communication and feature-specific service functions.

**Shared**

Contains reusable UI components, layouts, utilities, and common application elements.

**Styles**

Contains global styles, variables, typography, and shared SCSS configuration.

## Local Setup

From the frontend directory:

```bash
npm install
npm run dev
```

The development server will be available at:

```text
http://localhost:5173
```

## Development

The frontend communicates with the FastAPI backend through Axios and uses React Router for application navigation.

Reusable components and SCSS modules are used to keep the interface consistent across application sections.
