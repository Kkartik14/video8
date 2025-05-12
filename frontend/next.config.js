/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost'],
  },
  // Add async redirects to maintain backward compatibility
  async redirects() {
    return [
      {
        source: '/generator',
        destination: '/app',
        permanent: true,
      },
    ]
  },
}

module.exports = nextConfig 