# Motion Blur using Velocity Buffers 🎮

[![LaTeX](https://img.shields.io/badge/LaTeX-Beamer-blue?logo=latex&logoColor//img.](https://img.shields.io/badge](https://img.shields.io/badge/github.com/topics/academic on implementing **real-time motion blur** using velocity buffers in modern graphics pipelines. This project was developed as part of CSE 409 Graphics Assignment at Bangladesh University of Engineering and Technology (BUET).

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Implementation](#technical-implementation)
- [Project Structure](#project-structure)
- [Building the Presentation](#building-the-presentation)
- [Key Concepts](#key-concepts)
- [Visual Examples](#visual-examples)
- [Performance Analysis](#performance-analysis)
- [Real-World Applications](#real-world-applications)
- [Team](#team)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

Motion blur is a critical visual effect in modern computer graphics that simulates the natural blurring that occurs when objects move during camera exposure. This project presents a detailed study of **velocity buffer-based motion blur**, which has become the industry standard for real-time applications like video games.

### What Makes This Special?

- **Performance-focused**: Single geometry pass implementation
- **Industry-standard**: Used in Unreal Engine, Unity HDRP, and CryEngine
- **Mathematically rigorous**: Complete mathematical derivations and examples
- **Practical insights**: Real-world optimization techniques and trade-offs

## ✨ Features

### Core Technical Features
- 🎯 **Per-pixel motion vectors** - Accurate movement tracking
- ⚡ **Single-pass rendering** - Optimized for real-time performance
- 🎨 **Flexible post-processing** - Quality/performance tuning
- 🔧 **Deferred rendering compatible** - Modern pipeline integration

### Presentation Features
- 📊 **14 comprehensive slides** covering theory to implementation
- 💻 **Syntax-highlighted GLSL code** examples
- 📈 **Visual diagrams** and mathematical formulations
- 🎮 **Real engine comparisons** (Unreal, Unity, CryEngine)
- 📱 **Professional LaTeX Beamer** formatting

## 🔧 Technical Implementation

### Velocity Buffer Computation Pipeline

```glsl
// Vertex Shader - Compute motion vectors
layout(location = 0) in vec3 position;
uniform mat4 currentMVP, previousMVP;
out vec4 currentPos, previousPos;

void main() {
    vec4 worldPos = vec4(position, 1.0);
    currentPos = currentMVP * worldPos;
    previousPos = previousMVP * worldPos;
    gl_Position = currentPos;
}
```

```glsl
// Fragment Shader - Screen-space velocity
in vec4 currentPos, previousPos;
uniform vec2 screenSize;
out vec2 velocity;

void main() {
    vec2 currNDC = currentPos.xy / currentPos.w;
    vec2 prevNDC = previousPos.xy / previousPos.w;
    vec2 currScreen = (currNDC * 0.5 + 0.5) * screenSize;
    vec2 prevScreen = (prevNDC * 0.5 + 0.5) * screenSize;
    velocity = currScreen - prevScreen;
}
```

### Mathematical Foundation

The core formula for velocity computation:

```
V = Screen_current - Screen_previous
```

Where:
- `Screen = (NDC × 0.5 + 0.5) × ScreenSize`
- `NDC = ProjectedPosition.xy / ProjectedPosition.w`

## 📁 Project Structure

```
motion-blur-velocity-buffers/
├── Motion_Blur___Graphics_Assignment.pdf    # Generated presentation PDF
├── main.tex                                 # Main LaTeX Beamer document
├── preamble.tex                            # LaTeX configuration
├── images/                                 # Presentation assets
│   └── carSpeedingBlurred.png             # Motion blur example image
├── README.md                              # This file
└── LICENSE                                # Project license
```

## 🔨 Building the Presentation

### Prerequisites

Make sure you have the following installed:

- **LaTeX Distribution**: TeX Live (recommended) or MikTeX
- **Required Packages**: Listed in the dependencies section below

### Compilation Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/motion-blur-velocity-buffers.git
cd motion-blur-velocity-buffers

# Compile the presentation
pdflatex main.tex
pdflatex main.tex  # Run twice for proper references

# Alternative: Using latexmk for automatic compilation
latexmk -pdf main.tex
```

### Quick Build Script

```bash
#!/bin/bash
# build.sh
echo "Building Motion Blur Presentation..."
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
echo "Build complete! Output: main.pdf"
```

## 💡 Key Concepts

### 1. Velocity Buffer Fundamentals
- **Storage Format**: RG16F (Red=horizontal, Green=vertical velocity)
- **Range**: ±1024 pixels for extreme motion cases
- **Memory Efficiency**: Half-precision floats reduce bandwidth

### 2. Sampling Strategy
- **Optimal Sample Count**: 8-16 samples (quality/performance sweet spot)
- **Weight Distribution**: Distance-based falloff for natural blur
- **Methods**: Fixed, adaptive, jittered, and weighted sampling

### 3. Performance Optimizations
- **Early Exit**: Skip processing for static areas (velocity 

**⭐ Star this repository if you found it helpful!**

[**📖 View Presentation**](Motion_Blur___Graphics_Assignment.pdf) -  [**🐛 Report Bug**](https://github.com/yourusername/motion-blur-velocity-buffers/issues) -  [**💡 Request Feature**](https://github.com/yourusername/motion-blur-velocity-buffers/issues)



[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/82696765/d7b57dbc-c4a6-4b0a-987f-a51ed0a01e8c/Motion_Blur___Graphics_Assignment.pdf
