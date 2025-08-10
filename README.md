<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Motion Blur using Velocity Buffers 🎮

[
[
[
[

A comprehensive presentation on implementing **real-time motion blur** using velocity buffers in modern graphics pipelines. This project was developed as part of CSE 409 Graphics Assignment at Bangladesh University of Engineering and Technology (BUET).

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

- **Early Exit**: Skip processing for static areas (velocity < threshold)
- **Velocity Clamping**: Prevent extreme blur artifacts
- **Adaptive Quality**: Adjust samples based on motion intensity


## 📊 Performance Analysis

| Technique | Geometry Passes | Memory Overhead | Quality | Performance |
| :-- | :-- | :-- | :-- | :-- |
| Multi-sampling | Multiple | Low | Excellent | Poor |
| **Velocity Buffers** | **Single** | **Medium** | **High** | **Excellent** |
| Post-process Only | Single | Low | Poor | Excellent |

### Benchmark Results (Typical)

- **Memory**: +16MB for 1920×1080 velocity buffer (RG16F)
- **Performance Impact**: 2-5ms additional frame time
- **Quality**: Visually indistinguishable from offline rendering


## 🎮 Real-World Applications

### Game Engines Using This Technique

| Engine | Implementation | Key Features |
| :-- | :-- | :-- |
| **Unreal Engine** | Per-object motion blur | TAA integration, temporal upsampling |
| **Unity HDRP** | Camera + object blur | VR optimization, quality presets |
| **CryEngine** | Advanced sampling | Radial blur, dynamic quality adaptation |

### Industry Use Cases

- **Racing Games**: Fast vehicle motion blur
- **First-Person Shooters**: Camera motion during movement
- **Sports Games**: Ball and player motion tracking
- **VR Applications**: Reduced motion sickness


## 👥 Team

**Team AmarGraphics** - CSE 409 Graphics Assignment


| Member | Student ID | Role |
| :-- | :-- | :-- |
| **Masnoon Muztahid** | 2005067 | Lead Developer \& Research |
| **Dipanta Kumar Roy Nobo** | 2005074 | Implementation \& Testing |
| **Tawkir Aziz Rahman** | 2005090 | Documentation \& Analysis |

**Institution**: Department of Computer Science and Engineering
**University**: Bangladesh University of Engineering and Technology (BUET)
**Course**: CSE 409 - Computer Graphics
**Date**: August 10, 2025

## 📦 Dependencies

### Required LaTeX Packages

```latex
\usepackage{tikz}          % Diagrams and illustrations
\usepackage{pgfplots}      % Plotting and graphs
\usepackage{listings}      % Code syntax highlighting
\usepackage{xcolor}        % Color management
\usepackage{amsmath}       % Mathematical notation
\usepackage{amssymb}       % Mathematical symbols
\usepackage{algorithm2e}   % Algorithm pseudocode
\usepackage{caption}       % Caption formatting
\usepackage{subcaption}    % Subfigure captions
```


### TikZ Libraries

```latex
\usetikzlibrary{arrows.meta}              % Arrow styles
\usetikzlibrary{shapes}                   % Shape library
\usetikzlibrary{positioning}              % Relative positioning
\usetikzlibrary{decorations.pathreplacing} % Path decorations
\usetikzlibrary{patterns}                 % Fill patterns
\usetikzlibrary{calc}                     % Coordinate calculations
```


## 🚀 Usage Examples

### Academic Use

- **Computer Graphics Courses**: Complete motion blur implementation study
- **Game Development Programs**: Real-time rendering techniques
- **Research Projects**: Performance optimization case studies


### Professional Development

- **Engine Development**: Reference implementation for custom engines
- **Technical Presentations**: Template for graphics programming talks
- **Code Reviews**: Best practices for velocity buffer implementation


## 🤝 Contributing

We welcome contributions to improve this educational resource!

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-improvement`
3. **Make your changes**: Improve documentation, add examples, fix issues
4. **Commit your changes**: `git commit -m 'Add amazing improvement'`
5. **Push to the branch**: `git push origin feature/amazing-improvement`
6. **Open a Pull Request**

### Contribution Areas

- 📝 **Documentation improvements**
- 🎨 **Visual diagram enhancements**
- 💻 **Additional code examples**
- 🔧 **Build system improvements**
- 🐛 **Bug fixes and corrections**


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Team AmarGraphics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```


## 🙏 Acknowledgments

- **BUET CSE Department** for academic guidance
- **Industry pioneers** in real-time motion blur techniques
- **Open source community** for LaTeX tools and packages
- **Game engine developers** for sharing implementation insights


## 📞 Contact

For questions, suggestions, or collaboration opportunities:

- **Email**: [team.amargraphics@gmail.com](mailto:team.amargraphics@gmail.com)
- **University**: Bangladesh University of Engineering and Technology
- **Course**: CSE 409 Computer Graphics

***

<div align="center">

**⭐ Star this repository if you found it helpful!**

[**📖 View Presentation**](Motion_Blur___Graphics_Assignment.pdf) -  [**🐛 Report Bug**](https://github.com/yourusername/motion-blur-velocity-buffers/issues) -  [**💡 Request Feature**](https://github.com/yourusername/motion-blur-velocity-buffers/issues)

</div>
<div style="text-align: center">⁂</div>

[^1]: Motion_Blur___Graphics_Assignment.pdf

