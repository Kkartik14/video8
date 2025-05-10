import { useEffect, useRef } from 'react';

const HeroAnimation = () => {
  const canvasRef = useRef(null);
  
  useEffect(() => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let time = 0;
    
    // Resize canvas to parent dimensions
    const resizeCanvas = () => {
      const { width, height } = canvas.parentElement.getBoundingClientRect();
      canvas.width = width;
      canvas.height = height;
    };
    
    // Initial sizing
    resizeCanvas();
    
    // Handle window resize
    window.addEventListener('resize', resizeCanvas);
    
    // New colors matching our theme
    const colors = {
      blue: '#00B4D8',
      purple: '#8B5CF6',
      green: '#00D084',
      red: '#FF3366'
    };

    // Draw a point
    const drawPoint = (x, y, radius, color) => {
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
    };
    
    const drawCircle = (x, y, radius, color, phase = 0) => {
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.stroke();
      
      // Draw moving point on circle
      const pointX = x + radius * Math.cos(time + phase);
      const pointY = y + radius * Math.sin(time + phase);
      drawPoint(pointX, pointY, 2, color);
      
      return { pointX, pointY };
    };
    
    const drawTriangle = (x, y, size, color, rotation = 0) => {
      ctx.beginPath();
      const height = size * Math.sqrt(3) / 2;
      
      // Calculate vertices
      const points = [
        { x: x, y: y - height * 2/3 }, // top
        { x: x - size/2, y: y + height/3 }, // bottom left
        { x: x + size/2, y: y + height/3 }  // bottom right
      ];
      
      // Apply rotation
      const rotatedPoints = points.map(point => {
        const dx = point.x - x;
        const dy = point.y - y;
        return {
          x: x + dx * Math.cos(rotation) - dy * Math.sin(rotation),
          y: y + dx * Math.sin(rotation) + dy * Math.cos(rotation)
        };
      });
      
      // Draw the triangle
      ctx.moveTo(rotatedPoints[0].x, rotatedPoints[0].y);
      ctx.lineTo(rotatedPoints[1].x, rotatedPoints[1].y);
      ctx.lineTo(rotatedPoints[2].x, rotatedPoints[2].y);
      ctx.closePath();
      
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    };
    
    const drawSquare = (x, y, size, color, rotation = 0) => {
      ctx.beginPath();
      const halfSize = size / 2;
      
      // Calculate vertices
      const points = [
        { x: x - halfSize, y: y - halfSize }, // top left
        { x: x + halfSize, y: y - halfSize }, // top right
        { x: x + halfSize, y: y + halfSize }, // bottom right
        { x: x - halfSize, y: y + halfSize }  // bottom left
      ];
      
      // Apply rotation
      const rotatedPoints = points.map(point => {
        const dx = point.x - x;
        const dy = point.y - y;
        return {
          x: x + dx * Math.cos(rotation) - dy * Math.sin(rotation),
          y: y + dx * Math.sin(rotation) + dy * Math.cos(rotation)
        };
      });
      
      // Draw the square
      ctx.moveTo(rotatedPoints[0].x, rotatedPoints[0].y);
      ctx.lineTo(rotatedPoints[1].x, rotatedPoints[1].y);
      ctx.lineTo(rotatedPoints[2].x, rotatedPoints[2].y);
      ctx.lineTo(rotatedPoints[3].x, rotatedPoints[3].y);
      ctx.closePath();
      
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.stroke();
    };
    
    const drawMathSymbol = (x, y, size, color) => {
      ctx.font = `${size}px serif`;
      ctx.fillStyle = color;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      
      // Randomly select a math symbol
      const symbols = ['∑', '∫', '∂', 'π', '√', '∞', 'θ', 'λ', 'Δ', 'Ω'];
      const symbol = symbols[Math.floor(time * 0.1) % symbols.length];
      
      ctx.fillText(symbol, x, y);
    };

    // Draw a sine or cosine wave
    const drawWave = (startX, startY, width, amplitude, frequency, color, type = 'sine') => {
      ctx.beginPath();
      ctx.moveTo(startX, startY);
      
      for (let i = 0; i <= width; i += 5) {
        const x = startX + i;
        let y;
        
        if (type === 'sine') {
          y = startY + Math.sin((i / width) * Math.PI * 2 * frequency + time) * amplitude;
        } else {
          y = startY + Math.cos((i / width) * Math.PI * 2 * frequency + time) * amplitude;
        }
        
        ctx.lineTo(x, y);
      }
      
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Moving point on the wave
      const phaseShift = time % (Math.PI * 2);
      const pointPosition = (width / 4) * (1 + Math.sin(phaseShift));
      const pointX = startX + pointPosition;
      let pointY;
      
      if (type === 'sine') {
        pointY = startY + Math.sin((pointPosition / width) * Math.PI * 2 * frequency + time) * amplitude;
      } else {
        pointY = startY + Math.cos((pointPosition / width) * Math.PI * 2 * frequency + time) * amplitude;
      }
      
      drawPoint(pointX, pointY, 2, color);
    };

    // Draw a grid - very subtle
    const drawGrid = (spacing, color, opacity) => {
      const width = canvas.width;
      const height = canvas.height;
      
      ctx.strokeStyle = color;
      ctx.lineWidth = 0.5;
      ctx.globalAlpha = opacity;
      
      // Vertical lines
      for (let x = spacing; x < width; x += spacing) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      
      // Horizontal lines
      for (let y = spacing; y < height; y += spacing) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }
      
      ctx.globalAlpha = 1;
    };

    // Draw axes
    const drawAxes = (centerX, centerY, length, color) => {
      // X-Axis
      ctx.beginPath();
      ctx.moveTo(centerX - length, centerY);
      ctx.lineTo(centerX + length, centerY);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5;
      ctx.stroke();
      
      // X-Axis arrow
      ctx.beginPath();
      ctx.moveTo(centerX + length, centerY);
      ctx.lineTo(centerX + length - 10, centerY - 5);
      ctx.lineTo(centerX + length - 10, centerY + 5);
      ctx.closePath();
      ctx.fillStyle = color;
      ctx.fill();
      
      // Y-Axis
      ctx.beginPath();
      ctx.moveTo(centerX, centerY + length);
      ctx.lineTo(centerX, centerY - length);
      ctx.stroke();
      
      // Y-Axis arrow
      ctx.beginPath();
      ctx.moveTo(centerX, centerY - length);
      ctx.lineTo(centerX - 5, centerY - length + 10);
      ctx.lineTo(centerX + 5, centerY - length + 10);
      ctx.closePath();
      ctx.fill();
    };
    
    // Create gradient
    const createGradient = () => {
      const { width, height } = canvas;
      const gradient = ctx.createLinearGradient(0, 0, width, height);
      gradient.addColorStop(0, colors.purple);
      gradient.addColorStop(0.33, colors.red);
      gradient.addColorStop(0.66, colors.blue);
      gradient.addColorStop(1, colors.green);
      return gradient;
    };
    
    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Get dimensions
      const { width, height } = canvas;
      const centerX = width / 2;
      const centerY = height / 2;
      
      // Determine if dark mode based on body class
      const isDarkMode = document.body.classList.contains('dark');
      
      // Background with opacity
      ctx.fillStyle = isDarkMode ? '#0A0A0A' : '#F9FAFB';
      ctx.globalAlpha = 0.1;
      ctx.fillRect(0, 0, width, height);
      ctx.globalAlpha = 1;
      
      // Draw a subtle grid
      drawGrid(60, isDarkMode ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.025)', 0.2);
      
      // Draw sine wave along x-axis
      drawWave(width * 0.25, height * 0.7, width * 0.5, 30, 1.5, colors.blue, 'sine');
      
      // Draw animated circles
      const circle1 = drawCircle(centerX, centerY, 70, colors.purple);
      drawCircle(centerX, centerY, 100, colors.blue, Math.PI / 3);
      drawCircle(centerX, centerY, 130, colors.green, Math.PI / 6);
      
      // Draw rotating triangle
      drawTriangle(centerX, centerY, 160, colors.red, time * 0.5);
      
      // Draw math symbols that orbit around
      const symbolRadius = 180;
      const numSymbols = 6;
      for (let i = 0; i < numSymbols; i++) {
        const angle = (i / numSymbols) * Math.PI * 2 + time * 0.2;
        const x = centerX + symbolRadius * Math.cos(angle);
        const y = centerY + symbolRadius * Math.sin(angle);
        drawMathSymbol(x, y, 20, colors.blue);
      }
      
      // Draw connecting lines 
      ctx.beginPath();
      ctx.setLineDash([5, 10]);
      ctx.moveTo(circle1.pointX, circle1.pointY);
      ctx.lineTo(centerX + 80 * Math.cos(time * 0.5), centerY + 80 * Math.sin(time * 0.5));
      ctx.strokeStyle = colors.purple;
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.setLineDash([]);
      
      // Update time for animation
      time += 0.01;
      
      // Continue animation
      animationFrameId = requestAnimationFrame(render);
    };
    
    // Start animation
    render();
    
    // Cleanup
    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);
  
  return (
    <div className="hero-animation-container w-full h-full absolute top-0 left-0 opacity-25 dark:opacity-40 pointer-events-none">
      <canvas 
        ref={canvasRef} 
        className="w-full h-full"
      />
    </div>
  );
};

export default HeroAnimation; 