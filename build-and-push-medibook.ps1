param(
    [string]$Image = "khalidaitsaid/medibook:latest"
)

$ErrorActionPreference = "Stop"

Write-Host "Checking Docker..."
docker info | Out-Null

Write-Host "Building $Image ..."
docker build -t $Image .

Write-Host "Logging in to Docker Hub if needed..."
docker login

Write-Host "Pushing $Image ..."
docker push $Image

Write-Host ""
Write-Host "Done. Use this image in Dokploy Raw Compose:"
Write-Host "MEDIBOOK_IMAGE=$Image"
