/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./dist/**/*.html', './src/js/**/*.js', './build.py'],
  theme: {
    extend: {
      colors: {
        ink: { DEFAULT: '#15120f', soft: '#221d19', line: '#3a322b' },
        cream: { DEFAULT: '#f6f0e6', dark: '#ece3d3' },
        wine: { DEFAULT: '#7b1e2b', dark: '#5e1520', light: '#a33a47' },
        ochre: { DEFAULT: '#c49a4a', light: '#dcbb78' },
        stone: { DEFAULT: '#6b6158' },
      },
      fontFamily: {
        serif: ['Georgia', '"Times New Roman"', 'serif'],
        sans: ['Verdana', 'Geneva', 'sans-serif'],
      },
      maxWidth: { prose: '68ch' },
    },
  },
  plugins: [],
};
