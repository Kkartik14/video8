# Prompt-to-2D-Video Generator Frontend

This is a Next.js frontend for the Prompt-to-2D-Video Generator application. It interfaces with the FastAPI backend to create animated educational videos from natural language prompts.

## Features

- Modern, responsive UI built with Next.js and TailwindCSS
- Form for entering animation prompts and selecting LLM models (Claude or Groq)
- Example prompt suggestions
- Video playback with download option
- Tips for creating effective prompts

## Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Create a `.env.local` file in the frontend directory with:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Start the development server:

```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser.

## Building for Production

```bash
npm run build
npm run start
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`: URL of the FastAPI backend (default: http://localhost:8000)

## Project Structure

- `pages/`: Next.js pages
- `components/`: React components
- `styles/`: CSS files
- `utils/`: Utility functions
- `public/`: Static files 