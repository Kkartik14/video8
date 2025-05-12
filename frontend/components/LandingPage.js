import { useRouter } from 'next/router';
import ThemeToggle from './ThemeToggle';

export default function LandingPage() {
  const router = useRouter();

  const handleGetStarted = () => {
    router.push('/app');
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Background image with overlay */}
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-b from-purple-900/30 to-blue-900/30 z-10" />
        <div 
          className="absolute inset-0 bg-cover bg-center z-0 bg-animate-pulse" 
          style={{ 
            backgroundImage: "url('/images/mountains-background.jpg')", 
            filter: "brightness(0.8)" 
          }}
        />
      </div>

      {/* Header */}
      <header className="relative z-20 pt-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <div className="flex items-center">
          <span className="text-purple-500 text-2xl font-bold mr-2">
            <svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" fill="none">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16" />
            </svg>
          </span>
          <span className="text-white text-xl font-semibold">
            Prompt-to-2D-Video
          </span>
        </div>
        <div className="flex items-center">
          <ThemeToggle />
        </div>
      </header>

      {/* Main content */}
      <main className="relative z-20 flex flex-col items-center justify-center h-screen px-4 sm:px-6 lg:px-8 -mt-16">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-5xl sm:text-6xl md:text-7xl font-bold text-white mb-6 landing-text-glow">
            <span className="block">Animations</span>
            <span className="block italic text-purple-400">Reimagined</span>
            <span className="block">Through AI</span>
          </h1>
          <p className="text-xl sm:text-2xl text-white/90 mt-6 mb-12">
            Create beautiful 2D animated videos with just a text prompt. No animation skills required.
          </p>
          <button 
            onClick={handleGetStarted}
            className="px-8 py-4 text-lg font-medium rounded-md text-white bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transform transition-all duration-300 hover-scale"
          >
            Start Creating
          </button>
          <p className="text-white/70 text-sm mt-4">
            Free to use, no credit card required
          </p>
        </div>

        {/* Feature highlights */}
        <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {[
            {
              title: "Natural Language Prompts",
              description: "Just describe what you want to see, and watch it come to life."
            },
            {
              title: "Educational Animations",
              description: "Perfect for explaining complex concepts with beautiful visuals."
            },
            {
              title: "Code & Script Access",
              description: "Download the generated code to learn and customize."
            }
          ].map((feature, index) => (
            <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 hover-scale">
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-white/80">{feature.description}</p>
            </div>
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-20 py-6 px-4 sm:px-6 lg:px-8 text-white/60 text-sm flex justify-between">
        <div>© {new Date().getFullYear()} Prompt-to-2D-Video Generator</div>
        <div className="flex space-x-4">
          <span>Terms</span>
          <span>Privacy</span>
        </div>
      </footer>
    </div>
  );
} 