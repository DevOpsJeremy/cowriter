#!/bin/bash
# Build Windows executable in Linux CI environment

set -e

echo "Building Cowriter Windows executable in Linux container..."

# Build using Docker
docker build -f Dockerfile.windows --target export --output dist .

echo "Build complete! Windows executable: dist/Cowriter.exe"
echo "File info:"
file dist/Cowriter.exe
ls -lh dist/Cowriter.exe
