import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          orange: '#FF6B35',
          yellow: '#FFB800',
          green: '#52C41A',
          blue: '#1890FF',
        },
      },
    },
  },
  plugins: [],
}

export default config
