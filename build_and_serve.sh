#!/bin/bash

set -e

# Save the root directory
ROOT_DIR=$(pwd)

echo "🏗️  Building gallery..."
docker run -v "$(pwd):/work" ghcr.io/thumbsup/thumbsup /bin/sh -c "cd /work/ && thumbsup --config config.json"

echo "✨ Customizing HTML..."
bash customize_html.sh

echo "🚀 Starting local server..."
echo "📱 Open http://localhost:8000 in your browser"
echo "Press Ctrl+C to stop the server"

# Change to build_output and start server
cd build_output
python3 -m http.server 8000

# Return to root directory after server stops
cd "$ROOT_DIR"
echo "✅ Returned to $(pwd)"
