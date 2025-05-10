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
    
    const drawCircle = (x, y, radius, color, phase = 0) => {
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.stroke();
      
      // Draw moving point on circle
      const pointX = x + radius * Math.cos(time + phase);
      const pointY = y + radius * Math.sin(time + phase);
      ctx.beginPath();
      ctx.arc(pointX, pointY, 5, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      
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
      ctx.lineWidth = 2;
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
      ctx.lineWidth = 2;
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
    
    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Get dimensions
      const { width, height } = canvas;
      const centerX = width / 2;
      const centerY = height / 2;
      
      // Determine if dark mode based on body class
      const isDarkMode = document.body.classList.contains('dark');
      const bgColor = isDarkMode ? '#1E293B' : '#F9FAFB';
      
      // Background with opacity
      ctx.fillStyle = bgColor;
      ctx.globalAlpha = 0.2;
      ctx.fillRect(0, 0, width, height);
      ctx.globalAlpha = 1;
      
      // Draw animated circles
      const circle1 = drawCircle(centerX, centerY, 80, '#3B82F6');
      drawCircle(centerX, centerY, 120, '#8B5CF6', Math.PI / 3);
      drawCircle(centerX, centerY, 160, '#10B981', Math.PI / 6);
      
      // Draw rotating triangle
      drawTriangle(centerX, centerY, 180, '#F59E0B', time * 0.7);
      
      // Draw rotating square
      drawSquare(centerX, centerY, 260, '#EF4444', -time * 0.5);
      
      // Draw math symbols that orbit around
      const symbolRadius = 220;
      const numSymbols = 8;
      for (let i = 0; i < numSymbols; i++) {
        const angle = (i / numSymbols) * Math.PI * 2 + time * 0.2;
        const x = centerX + symbolRadius * Math.cos(angle);
        const y = centerY + symbolRadius * Math.sin(angle);
        drawMathSymbol(x, y, 24, '#06B6D4');
      }
      
      // Draw connecting lines
      ctx.beginPath();
      ctx.moveTo(circle1.pointX, circle1.pointY);
      ctx.lineTo(centerX + 90 * Math.cos(time * 0.7), centerY + 90 * Math.sin(time * 0.7));
      ctx.strokeStyle = '#3B82F6';
      ctx.stroke();
      
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
    <div className="hero-animation-container w-full h-full absolute top-0 left-0 opacity-30 dark:opacity-50 pointer-events-none">
      <canvas 
        ref={canvasRef} 
        className="w-full h-full"
      />
    </div>
  );
};

export default HeroAnimation; 