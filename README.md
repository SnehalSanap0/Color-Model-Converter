# Color Model Converter

This Python application allows users to convert colors between different color models (RGB, HSV, CMY) using a graphical user interface built with `tkinter`. The tool also includes interactive sliders, visualizations, quizzes, color information, and drawing functionalities for a comprehensive understanding of color models.

## Features

- **Color Model Conversions**:
  - **RGB to HSV Conversion**: Converts an RGB color to its HSV equivalent.
  - **HSV to RGB Conversion**: Converts an HSV color back to RGB.
  - **RGB to CMY Conversion**: Converts an RGB color to its CMY equivalent.
  - **CMY to RGB Conversion**: Converts a CMY color back to RGB.
- **Interactive Sliders**: Adjust RGB values with sliders to see live color changes.
- **Color Picker**: Select colors using the color chooser dialog.
- **Visualizations**:
  - Display color changes using `matplotlib`.
  - **Color Cube**: Visualize the RGB color space as a 3D color cube.
- **Quizzes**:
  - Test your knowledge of color models with the built-in quiz feature.
- **Color Information**:
  - View detailed information about various color models and their properties.
- **Drawing Canvas**:
  - Draw on a canvas using selected colors.
  - **Erase Tool**: Erase drawings on the canvas.

## Requirements

- Python 3.x
- `tkinter` (usually comes pre-installed with Python)
- `matplotlib` (install using `pip install matplotlib`)
- `numpy` (install using `pip install numpy`)

## Installation

1. **Clone the repository** or download the script.
2. **Install the dependencies**:
   ```bash
   pip install matplotlib numpy
   ```
3. **Run the script**:
   ```bash
   python Color Model Converter.py
   ```

## Usage

1. Launch the application by running the script.
2. Use the sliders to adjust the RGB values or select a color using the color picker.
3. View the converted values in HSV or CMY formats, and explore other options:
   - **Take a Quiz**: Test your understanding of color theory.
   - **View Color Information**: Learn about different color models and properties.
   - **Color Cube Visualization**: See how colors map in a 3D RGB color space.
   - **Drawing Canvas**: Use the drawing canvas to create colorful sketches. You can also erase any content if needed.
4. The color preview updates automatically as you adjust the sliders or make selections.

## Code Overview

- **Color Model Conversion Functions**: Functions for converting between RGB, HSV, and CMY.
- **Quiz and Information Sections**: Provide educational content and interactive quizzes.
- **GUI Setup**: Uses `tkinter` for the graphical user interface, including sliders, buttons, color selection dialogs, and canvas.
- **Visualization**: Uses `matplotlib` to display the selected color and the color cube.

## Contribution

Feel free to submit issues or pull requests for new features or improvements.
