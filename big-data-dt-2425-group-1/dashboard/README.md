# Installatie-instructies voor Docker-images

## Stap 1 - Vereisten
Zorg ervoor dat Docker desktop is geinstalleerd. 
Installatie kan hier gedownload worden: [Docker](https://www.docker.com/products/docker-desktop)

## Stap 2 - Repository clonen
Clone de repository van onze GitLab
```bash
git clone https://gitlab.fdmci.hva.nl/langelw/big-data-dt-2425-group-1.git
```

## Stap 3 - Docker-image maken
Gebruik de dockerfile in de map dashboard om de Docker image te genereren
```bash
cd big-data-dt-2425-group-1
cd dashboard
docker build -t waternet-dashboard:latest . 
```

## Stap 4 - Docker-container uitvoeren
Start een container op basis van de Docker-image
```bash
docker run -p 8501:8501 --name waternet-dashboard waternet-dashboard
```
