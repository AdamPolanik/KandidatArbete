# Climbing-hold detection comparison

## Table of Contents
- [Introduction](#introduction)
- [Objectives](#objectives)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction
This project focuses on the implementation and comparison of two distinct approaches for detecting climbing holds: an edge detection algorithm and a YOLO (You Only Look Once) model. The edge detection algorithm aims to identify the edges of climbing holds based on their contours, providing a traditional computer vision solution. In parallel, we trained a YOLO model, leveraging deep learning techniques to detect climbing holds in images.

The primary objective of this project is to evaluate the performance of both methods in terms of execution-speed and accuracy. By analyzing these metrics, we aim to determine the most efficient and effective approach for climbing hold detection, which often is an important first step in climbing related applications.

## Objectives
- Detect climbing holds using simple Edge-detection algorithm
- Detect climbing holds using a trained YOLO-model
- Compare execution-speed and accuracy of both approaches

## Technologies Used
- Programming Language: Python
- Tools: OpenCv, 

## Installation

```bash
# Clone the repository
git clone https://github.com/AdamPolanik/KandidatArbete.git

# Navigate to the project directory
cd KandidatArbete

# Install missing dependencies

# Run YOLO-detection 
python3 testProgramYOLO.py

# Run Edge-detection
python3 testProgramEdgeDetection.py
