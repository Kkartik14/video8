import Head from 'next/head';
import LandingPage from '../components/LandingPage';

export default function Home() {
  return (
    <>
      <Head>
        <title>Prompt-to-2D-Video Generator - AI-Powered Animation Creation</title>
        <meta name="description" content="Create beautiful 2D animated educational videos with just a text prompt using AI and Manim" />
        <link rel="icon" href="/favicon.ico" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet" />
      </Head>
      <LandingPage />
    </>
  );
} 