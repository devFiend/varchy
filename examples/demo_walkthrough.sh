#!/usr/bin/env bash
set -e

# ==============================================================================
# Varchy 1-Minute Live Demo & Verification Script
# ==============================================================================

echo "🏛️ Welcome to Varchy Architecture Demo"
echo "--------------------------------------------------"

DEMO_DIR=$(mktemp -d -t varchy-demo-XXXXXX)
echo "📁 Created temporary demo workspace at: $DEMO_DIR"
cd "$DEMO_DIR"

echo ""
echo "👉 Step 1: Initialize workspace"
varchy init --name "MarkdownNotes" --desc "Local-first encrypted notes" --template local_first

echo ""
echo "👉 Step 2: Generate architecture blueprint (offline mock engine)"
varchy generate \
  --idea "A local-first encrypted collaborative markdown notebook" \
  --provider mock \
  --template local_first

echo ""
echo "👉 Step 3: Run the 100-Point Deterministic Readiness Gate"
varchy validate

echo ""
echo "👉 Step 4: Step to the next actionable implementation task"
varchy task next

echo ""
echo "👉 Step 5: Inspect compiled specifications"
echo "Generated files:"
ls -la
echo ""
echo "Docs folder contents:"
ls -la docs/

echo ""
echo "✨ Demo completed successfully! Cleaned up at: $DEMO_DIR"
