_**Docker Commands**_

docker stop cv-engine-container
docker rm cv-engine-container
docker run -d -p 5001:5000 -v "%cd%/inputs:/app/inputs" --name cv-engine-container jeton-cv-eval-engine