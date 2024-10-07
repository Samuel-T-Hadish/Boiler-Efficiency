/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./therma_boiler/pages/**/*.py", // scans all Python files in the pages directory
    "./therma_boiler/components/**/*.py", // scans all Python files in the components directory
    "./therma_boiler/app/**/*.py", // scans all Python files in the app directory
    "./therma_boiler/app.py", // scans all Python files in the lib directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
