#!/bin/bash

# =========================================
# Medibook Docker Build & Push Helper
# =========================================
# Usage: ./build-and-push.sh username
# Example: ./build-and-push.sh moncompte

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if username is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Erreur: Veuillez fournir votre Docker Hub username${NC}"
    echo -e "${YELLOW}Usage: ./build-and-push.sh your_username${NC}"
    echo -e "${YELLOW}Example: ./build-and-push.sh moncompte${NC}"
    exit 1
fi

USERNAME=$1
IMAGE_NAME="medibook"
IMAGE_TAG="v1"
FULL_IMAGE="$USERNAME/$IMAGE_NAME:$IMAGE_TAG"

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}Medibook Docker Build & Push${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Step 1: Verify Docker is installed
echo -e "${BLUE}📦 Vérification de Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker n'est pas installé. Veuillez installer Docker.${NC}"
    exit 1
fi
DOCKER_VERSION=$(docker --version)
echo -e "${GREEN}✅ $DOCKER_VERSION${NC}"
echo ""

# Step 2: Check Docker login
echo -e "${BLUE}🔐 Vérification de la connexion Docker Hub...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Non connecté à Docker Hub. Veuillez vous connecter.${NC}"
    echo -e "${BLUE}Exécution: docker login${NC}"
    docker login
fi
echo -e "${GREEN}✅ Connecté à Docker Hub${NC}"
echo ""

# Step 3: Build the image
echo -e "${BLUE}🔨 Construction de l'image Docker...${NC}"
echo -e "${YELLOW}Image: $FULL_IMAGE${NC}"
docker build -t $FULL_IMAGE .
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image construite avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors de la construction${NC}"
    exit 1
fi
echo ""

# Step 4: Verify image exists
echo -e "${BLUE}🔍 Vérification de l'image...${NC}"
IMAGES=$(docker images | grep "$USERNAME/$IMAGE_NAME" | awk '{print $3}')
if [ -z "$IMAGES" ]; then
    echo -e "${RED}❌ Image non trouvée${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Image trouvée: $FULL_IMAGE${NC}"
echo ""

# Step 5: Push to Docker Hub
echo -e "${BLUE}📤 Publication sur Docker Hub...${NC}"
echo -e "${YELLOW}Cela peut prendre quelques minutes...${NC}"
docker push $FULL_IMAGE
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image publiée avec succès${NC}"
else
    echo -e "${RED}❌ Erreur lors de la publication${NC}"
    exit 1
fi
echo ""

# Step 6: Verify on Docker Hub
echo -e "${BLUE}✅ Résumé du Déploiement${NC}"
echo -e "${GREEN}================================${NC}"
echo -e "Image Docker Hub: ${GREEN}$FULL_IMAGE${NC}"
echo -e "Repository: ${GREEN}https://hub.docker.com/r/$USERNAME/$IMAGE_NAME${NC}"
echo -e "Prêt pour Dokploy deployment${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Step 7: Instructions for Dokploy
echo -e "${BLUE}📋 Prochaines étapes pour Dokploy:${NC}"
echo ""
echo "1. Connectez-vous à Dokploy:"
echo "   http://IP_VM:3000"
echo ""
echo "2. Dans docker-compose.yml pour Dokploy, utilisez:"
echo "   image: $FULL_IMAGE"
echo ""
echo "3. Remplacez le port attribué (ex: 8005:8161)"
echo ""
echo "4. Cliquez 'Deploy'"
echo ""
echo -e "${GREEN}✅ Déploiement préparé avec succès!${NC}"
