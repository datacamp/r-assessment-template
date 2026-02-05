#!/bin/bash

# Script to pull/update .cursor folder and .cursorrules file from assessment_authoring_cursor repository
# Source: https://github.com/datacamp/assessment_authoring_cursor

set -e

REPO_URL="https://github.com/datacamp/assessment_authoring_cursor"
REPO_NAME="assessment_authoring_cursor"

# Get the root directory of the current git repository
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Create a temporary directory for cloning
TEMP_DIR=$(mktemp -d)

echo "🔄 Fetching latest cursor rules from $REPO_URL..."

# Clone the repository to the temporary directory (shallow clone for speed)
git clone --depth 1 "$REPO_URL" "$TEMP_DIR/$REPO_NAME" 2>/dev/null || {
    echo "❌ Failed to clone repository. Please check your network connection and repository access."
    rm -rf "$TEMP_DIR"
    exit 1
}

# Copy .cursor folder if it exists in the source repo
if [ -d "$TEMP_DIR/$REPO_NAME/.cursor" ]; then
    echo "📁 Updating .cursor folder..."
    rm -rf "$REPO_ROOT/.cursor"
    cp -r "$TEMP_DIR/$REPO_NAME/.cursor" "$REPO_ROOT/.cursor"
    echo "✅ .cursor folder updated successfully"
else
    echo "⚠️  No .cursor folder found in source repository"
fi

# Copy .cursorrules file if it exists in the source repo
if [ -f "$TEMP_DIR/$REPO_NAME/.cursorrules" ]; then
    echo "📄 Updating .cursorrules file..."
    cp "$TEMP_DIR/$REPO_NAME/.cursorrules" "$REPO_ROOT/.cursorrules"
    echo "✅ .cursorrules file updated successfully"
else
    echo "⚠️  No .cursorrules file found in source repository"
fi

# Clean up temporary directory
rm -rf "$TEMP_DIR"

echo ""
echo "🎉 Cursor rules update complete!"
echo "   Location: $REPO_ROOT"
