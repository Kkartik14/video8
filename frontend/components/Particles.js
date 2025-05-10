import { useEffect, useRef } from 'react';

const Particles = ({ count = 30 }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;
    
    // Clear any existing particles
    containerRef.current.innerHTML = '';
    
    // Create particles
    for (let i = 0; i < count; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      
      // Random position
      const posX = Math.random() * 100;
      const posY = Math.random() * 100;
      particle.style.left = `${posX}%`;
      particle.style.top = `${posY}%`;
      
      // Random delay
      const delay = Math.random() * 60;
      particle.style.animationDelay = `${delay}s`;
      
      // Random direction
      particle.style.setProperty('--random', Math.random());
      
      containerRef.current.appendChild(particle);
    }
  }, [count]);

  return (
    <div ref={containerRef} className="particles-container">
      {/* Particles will be created by JavaScript */}
    </div>
  );
};

export default Particles; 