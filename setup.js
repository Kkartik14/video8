#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

console.log('🎬 Prompt-to-2D-Video Generator Setup');
console.log('=====================================\n');

// Create necessary directories
if (!fs.existsSync('outputs')) {
  fs.mkdirSync('outputs');
  console.log('✅ Created outputs directory');
}

if (!fs.existsSync('frontend/.env.local')) {
  fs.writeFileSync('frontend/.env.local', 'NEXT_PUBLIC_API_URL=http://localhost:8000\n');
  console.log('✅ Created frontend/.env.local file');
}

// Determine Python command (try python3 first, then fall back to python)
const pythonCommand = fs.existsSync('/usr/bin/python3') ? 'python3' : 'python';
console.log(`ℹ️ Using Python command: ${pythonCommand}`);

// Check for .env file
const envExists = fs.existsSync('.env');
if (!envExists) {
  console.log('\n⚠️ No .env file found. You need to create one with your API keys.');
  rl.question('Would you like to create one now? (y/n): ', (answer) => {
    if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
      rl.question('Enter your ANTHROPIC_API_KEY (leave blank if not using Claude): ', (claude) => {
        rl.question('Enter your GROQ_API_KEY (leave blank if not using Groq): ', (groq) => {
          let envContent = '';
          if (claude) {
            envContent += `ANTHROPIC_API_KEY=${claude}\n`;
          }
          if (groq) {
            envContent += `GROQ_API_KEY=${groq}\n`;
          }
          fs.writeFileSync('.env', envContent);
          console.log('✅ Created .env file with your API keys');
          continueSetup();
        });
      });
    } else {
      console.log('⚠️ You will need to create a .env file with your API keys before using the application.');
      continueSetup();
    }
  });
} else {
  console.log('✅ .env file already exists');
  continueSetup();
}

function continueSetup() {
  console.log('\n📋 Installing dependencies...');
  try {
    // Check Python dependencies
    console.log(`\n🐍 Installing Python dependencies using ${pythonCommand}...`);
    execSync(`${pythonCommand} -m pip install -r requirements.txt`, { stdio: 'inherit' });
    console.log('✅ Python dependencies installed');
    
    // Check Node.js dependencies
    console.log('\n🟢 Installing Node.js dependencies...');
    execSync('npm install', { stdio: 'inherit' });
    console.log('✅ Root Node.js dependencies installed');
    
    // Check frontend dependencies
    console.log('\n🔷 Installing frontend dependencies...');
    execSync('cd frontend && npm install', { stdio: 'inherit' });
    console.log('✅ Frontend dependencies installed');
    
    // Build frontend
    console.log('\n🏗️ Building frontend...');
    execSync('cd frontend && npm run build', { stdio: 'inherit' });
    console.log('✅ Frontend built successfully');
    
    console.log('\n🎉 Setup completed successfully!');
    console.log('\nTo start the application in development mode:');
    console.log('  npm start');
    console.log('\nTo start the application in production mode:');
    console.log('  npm run start:prod');
    
    rl.close();
  } catch (error) {
    console.error('❌ Error during setup:', error.message);
    rl.close();
  }
} 