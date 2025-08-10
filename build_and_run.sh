#!/bin/bash
set -e

echo "🚀 Motion Blur Project Builder"
echo "=============================="
echo ""

# Create output directory if it doesn't exist
mkdir -p output

echo "📄 Step 1: Building LaTeX presentation..."
echo "----------------------------------------"

# Build LaTeX presentation (run twice for proper references)
echo "🔨 Compiling LaTeX presentation..."
if [ -f "main.tex" ]; then
    pdflatex -interaction=nonstopmode main.tex > latex_build.log 2>&1
    pdflatex -interaction=nonstopmode main.tex >> latex_build.log 2>&1
    
    if [ -f "main.pdf" ]; then
        cp main.pdf output/Motion_Blur_Presentation.pdf
        echo "✅ LaTeX PDF generated successfully: output/Motion_Blur_Presentation.pdf"
    else
        echo "❌ LaTeX compilation failed. Check latex_build.log for details."
        tail -20 latex_build.log
    fi
else
    echo "❌ main.tex not found, skipping LaTeX build"
fi

echo ""
echo "🎮 Step 2: Running Motion Blur Python Demo..."
echo "--------------------------------------------"

# Run Python motion blur demo
if [ -f "motion_blur_demo.py" ]; then
    python3 motion_blur_demo.py
    echo "✅ Python demo completed"
else
    echo "❌ motion_blur_demo.py not found, skipping Python demo"
fi

echo ""
echo "📊 Step 3: Build Summary"
echo "------------------------"

if [ -f "output/Motion_Blur_Presentation.pdf" ]; then
    echo "✅ LaTeX Presentation: output/Motion_Blur_Presentation.pdf"
else
    echo "❌ LaTeX Presentation: FAILED"
fi

if [ -f "output/motion_blur_comparison_frame_10.png" ]; then
    echo "✅ Motion Blur Demo: output/motion_blur_comparison_*.png"
    echo "✅ Velocity Buffer: output/velocity_buffer_visualization.png"
else
    echo "❌ Motion Blur Demo: FAILED (or no output generated yet)"
fi

echo ""
echo "📁 All outputs saved to 'output' directory"
echo "🎯 Project build complete!"

# List all generated files
echo ""
echo "📋 Generated Files:"
ls -la output/ 2>/dev/null || echo "No files generated yet"
