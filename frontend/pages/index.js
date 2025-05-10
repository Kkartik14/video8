import { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import PromptForm from '../components/PromptForm';
import VideoResult from '../components/VideoResult';
import InfoSection from '../components/InfoSection';
import { generateVideo } from '../utils/api';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [videoPath, setVideoPath] = useState(null);
  const [scriptPath, setScriptPath] = useState(null);
  const [narrationScript, setNarrationScript] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await generateVideo(formData.prompt, formData.model);
      setVideoPath(result.video_path);
      setScriptPath(result.script_path);
      setNarrationScript(result.narration_script);
    } catch (err) {
      console.error("Error generating video:", err);
      
      if (err.toString().includes('ERR_CONNECTION_REFUSED')) {
        setError("Could not connect to the backend server. Please make sure it's running at " + 
                 (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'));
      } else {
        setError(err.toString());
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Prompt-to-2D-Video Generator</title>
        <meta name="description" content="Generate beautiful 2D animations from natural language prompts" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Header />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            🎬 Prompt-to-2D-Video Generator
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Convert natural language prompts into animated educational videos using LLM and Manim.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <PromptForm onSubmit={handleSubmit} isLoading={isLoading} />
            
            {error && (
              <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-red-700">{error}</p>
                    {error.includes('backend server') && (
                      <p className="text-sm text-red-700 mt-2">
                        Try running the backend manually: <code className="bg-red-100 px-1 rounded">python3 backend/main.py</code>
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            {videoPath && <VideoResult videoPath={videoPath} scriptPath={scriptPath} narrationScript={narrationScript} />}
          </div>
          
          <div className="lg:col-span-1">
            <InfoSection />
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
} 