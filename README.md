# Cycloid Generator

This project is a fork of two existing projects by RoTechnic: [CycloidalDesign](https://github.com/roTechnic/CycloidalDesign) and [internalECGears](https://github.com/roTechnic/internalECGears). The aim of this fork is to combine and extend the functionality of these projects while introducing performance improvements and an easier user experience.

## About

Cycloid Generator is a powerful tool that allows you to generate external and internal cycloid shapes. It provides a user-friendly GUI menu that enables you to configure various parameters related to the shape, including the type of shape, the number of pins, pin radius, pitch radius, contraction, and geometric complexity.

## Features

This version of Cycloid Generator stands out from RoTechnic's original work in two key ways:

1. **Consolidation and Enhanced Usability:** The original projects, CycloidalDesign and internalECGears, have been combined into a single repository, simplifying the overall workflow. Additionally, this version introduces a graphical user interface (GUI) menu that allows users to conveniently configure the parameters for generating cycloid shapes.

2. **Optimized Drawing Algorithm:** One of the significant enhancements in this fork is the optimization of the drawing algorithm. Unlike the original scripts, which drew numerous lines to plot the curves, this version incorporates a complexity parameter. The complexity value determines the resolution of the geometry. By adjusting the complexity, users can control the number of lines required to render the same curve. This improvement proves especially advantageous for individuals who experienced crashes when using the original scripts in software like Fusion 360.

## Usage

To use Cycloid Generator, follow these steps:

1. Download the cycloid_generator.py file.

2. Copy the file to the scripts folder: `%AppData%\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts`

3. Open Fusion 360, go to the Utilities tab, and click Add-Ins > Scripts and Add-Ins.

4. Under the My Scripts section, select cycloid_gneerator and press Run.

5. Enter your required values in the GUI menu.

6. Press OK, read the warning message, and press OK again.

7. Wait patiently, as generating may take a minute or two. Do not try to click anything or interact with Fusion 360 until generation has complete, or you may crash your program.

8. Continue with your cool project!

## Contributing

Contributions to Cycloid Generator are welcome! If you would like to contribute, please follow these guidelines:

1. Fork the repository on GitHub.

2. Create a new branch with a descriptive name for your feature or bug fix.

3. Implement your changes.

4. Commit your changes and push the branch to your forked repository.

5. Open a pull request on the main repository, describing your changes in detail.

## License

Cycloid Generator is released under the [MIT License](LICENSE). Please review the license file for more information.

## Acknowledgements

Cycloid Generator is built upon the fantastic work by RoTechnic in the original projects:

- [CycloidalDesign](https://github.com/roTechnic/CycloidalDesign)
- [internalECGears](https://github.com/roTechnic/internalECGears)

A huge thanks to RoTechnic for their valuable contributions and inspiration.

## Thanks
Happy cycloid generating!
