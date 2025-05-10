import { useState, useEffect } from 'react';
import { FaMoon, FaSun } from 'react-icons/fa';

const ThemeToggle = () => {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    // Check if user previously set a preference
    const isDark = localStorage.getItem('darkMode') === 'true';
    setDarkMode(isDark);
    
    // Apply theme class on initial load
    if (isDark) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, []);

  const toggleTheme = () => {
    // Toggle dark mode
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    
    // Update DOM and localStorage
    if (newDarkMode) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
    
    localStorage.setItem('darkMode', newDarkMode);
  };

  return (
    <button
      onClick={toggleTheme}
      className="p-2 rounded-md bg-gray-100 dark:bg-dark-100 
        text-gray-700 dark:text-gray-200 transition-all duration-300 
        hover:bg-gray-200 dark:hover:bg-dark-200"
      aria-label="Toggle dark mode"
    >
      {darkMode ? (
        <FaSun className="h-4 w-4 text-yellow-400" />
      ) : (
        <FaMoon className="h-4 w-4 text-blue-500" />
      )}
    </button>
  );
};

export default ThemeToggle; 