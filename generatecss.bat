@echo off
echo Generating Tailwind CSS...

:: Assuming tailwindcss.exe is now in the bin directory at the project root
tailwindcss.exe -i .\therma_boiler\tailwind\styles.css -o .\therma_boiler\assets\tailwind.css --minify 

echo Tailwind CSS generated successfully.
pause
