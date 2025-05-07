#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('🎬 Starting Prompt-to-2D-Video Generator...');

// Ensure outputs directory exists
if (!fs.existsSync('outputs')) {
  fs.mkdirSync('outputs');
  console.log('✅ Created outputs directory');
}

// Check if .env file exists
if (!fs.existsSync('.env')) {
  console.log('⚠️ Warning: .env file not found. You need to create it with your API keys.');
  console.log('Example:');
  console.log('ANTHROPIC_API_KEY=your_api_key_here');
  console.log('GROQ_API_KEY=your_api_key_here');
}

// Determine Python command (try python3 first, then fall back to python)
const pythonCommand = fs.existsSync('/usr/bin/python3') ? 'python3' : 'python';

// Start backend
console.log(`🚀 Starting backend server with ${pythonCommand}...`);
const backendProcess = spawn(pythonCommand, ['backend/main.py'], {
  stdio: 'inherit',
  detached: false
});

// Start frontend
console.log('🚀 Starting frontend server...');
const frontendProcess = spawn('npm', ['run', 'dev'], {
  cwd: path.join(__dirname, 'frontend'),
  stdio: 'inherit',
  detached: false
});

// Handle graceful shutdown
const cleanup = () => {
  console.log('\n🛑 Shutting down services...');
  
  if (backendProcess) {
    backendProcess.kill();
  }
  
  if (frontendProcess) {
    frontendProcess.kill();
  }
  
  process.exit(0);
};

// Handle termination signals
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('SIGQUIT', cleanup);

// Log errors
backendProcess.on('error', (error) => {
  console.error('Backend error:', error);
  console.log('⚠️ Could not start the backend server. Make sure Python is installed and in your PATH.');
  console.log('Try running the backend manually: python3 backend/main.py');
});

frontendProcess.on('error', (error) => {
  console.error('Frontend error:', error);
});

// Log completion
console.log('✅ Services started. You can access:');
console.log('   - Frontend: http://localhost:3000');
console.log('   - Backend API: http://localhost:8000');
console.log('   - API Docs: http://localhost:8000/docs');
console.log('\nPress Ctrl+C to stop all services.'); 