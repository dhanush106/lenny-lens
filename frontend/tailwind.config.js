/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        chalk: '#E5E3D0',
        'chalk-subtle': '#DCD9C4',
        'chalk-dark': '#CECAA9',
        stoneLaurel: '#646557',
        'stoneLaurel-muted': '#848574',
        forestUmber: '#493606',
        'forestUmber-light': '#6B500C',
        fennel: '#C9C49F',
        'fennel-muted': '#B8B38E',
        'fennel-light': '#D8D3AE',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        serif: ['Newsreader', 'Georgia', 'serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
    },
  },
  plugins: [],
}

