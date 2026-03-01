/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: '**.googleapis.com' },
      { protocol: 'https', hostname: '**.yelp.com' },
      { protocol: 'https', hostname: '**.cloudflare.com' },
    ],
  },
}

export default nextConfig
