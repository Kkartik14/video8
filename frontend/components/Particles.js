import { useEffect, useRef } from 'react';

const Particles = ({ count = 40 }) => {
  const containerRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    
    // Clear any existing particles
    container.innerHTML = '';
    
    // Define colors based on our new palette - more subdued
    const colors = [
      'rgba(139, 92, 246, 0.4)', // Purple
      'rgba(255, 51, 102, 0.4)', // Red/Pink
      'rgba(0, 180, 216, 0.4)', // Blue
      'rgba(0, 208, 132, 0.4)', // Green
    ];
    
    // Create particles
    for (let i = 0; i < count; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      
      // Randomize particle properties
      const size = Math.random() * 1.5 + 0.5; // Between 0.5-2px
      const randomColor = colors[Math.floor(Math.random() * colors.length)];
      const left = Math.random() * 100;
      const delay = Math.random() * 5;
      const duration = Math.random() * 30 + 60; // Between 60-90s
      
      // Set style for each particle
      particle.style.cssText = `
        left: ${left}%;
        width: ${size}px;
        height: ${size}px;
        background: ${randomColor};
        opacity: ${Math.random() * 0.5 + 0.1};
        animation-delay: -${delay}s;
        animation-duration: ${duration}s;
        --random: ${Math.random()};
      `;
      
      container.appendChild(particle);
    }

    // Add a few larger particles
    for (let i = 0; i < Math.floor(count / 20); i++) {
      const specialParticle = document.createElement('div');
      specialParticle.className = 'particle';
      
      const size = Math.random() * 2 + 1; // Between 1-3px
      const randomColor = colors[Math.floor(Math.random() * colors.length)];
      const left = Math.random() * 100;
      const delay = Math.random() * 5;
      const duration = Math.random() * 40 + 70; // Between 70-110s
      
      specialParticle.style.cssText = `
        left: ${left}%;
        width: ${size}px;
        height: ${size}px;
        background: ${randomColor};
        opacity: ${Math.random() * 0.4 + 0.2};
        animation-delay: -${delay}s;
        animation-duration: ${duration}s;
        --random: ${Math.random()};
      `;
      
      container.appendChild(specialParticle);
    }
    
    return () => {
      // Cleanup on unmount
      if (container) {
        container.innerHTML = '';
      }
    };
  }, [count]);

  return (
    <div ref={containerRef} className="particles-container">
      {/* Particles will be created in the useEffect hook */}
    </div>
  );
};

export default Particles; 