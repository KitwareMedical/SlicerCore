# Slicer Core

SlicerCore is an alternative build-system for the 3DSlicer project.  
It is intended to build a Python Package (wheel) from the core libraries and loadables modules of 3DSlicer.

## About Slicer

Slicer, or 3D Slicer, is a free, open source software package for visualization and image analysis.

3D Slicer is natively designed to be available on multiple platforms, including Windows, Linux and macOS.

For 3DSlicer community announcements and support, visit:

    https://discourse.slicer.org

For documentation, tutorials, and more information, please see:

    https://www.slicer.org

For 3DSlicer source code, please see:

    https://github.com/Slicer/Slicer


## About Slicer Core

Slicer Core in a single sentence:
***Slicer Core is the Python package consisting of all 3DSlicer modules that do not depend on Qt.***

Slicer Core contains the following libraries of 3DSlicer:
- `Base/Logic`
- `Libs/*`
- `Modules/Loadables/[MRML|MRMLDM|Logic|VTKWidgets]`

This enables using 3DSlicer powerful MRML nodes system and associated medical-oriented algorithms in pure Python.

## Using Slicer Core

SlicerCore provides access to the main Slicer libraries through the slicer package namespace :

```py
from slicer import vtkMRMLScalarVolumeNode
volume_node = vtkMRMLScalarVolumeNode()
```

Although the library can be used as is, additional convenience classes are provided in the trame-slicer Python package to initialize application logic and scene, wrap 2D and 3D views, provide applications on the web and more.

For more examples, please visit the **[trame-slicer](https://github.com/KitwareMedical/trame-slicer)** project.

## Documentation and Examples

- **[3DSlicer Developper Guide](https://slicer.readthedocs.io/en/latest/developer_guide/index.html)**
    - Note that only some parts of the developper guide applies to Slicer Core as some modules and classes are not available.
- **[3DSlicer API Documentation](https://apidocs.slicer.org/main/index.html)**
- **[Trame Slicer](https://github.com/KitwareMedical/trame-slicer)**

## Acknowledgments

This project uses [3D Slicer](https://www.slicer.org/) source code, an open-source software platform for medical image informatics, image processing, and three-dimensional visualization:  
Fedorov A., Beichel R., Kalpathy-Cramer J., Finet J., Fillion-Robin J-C., Pujol S., Bauer C., Jennings D., Fennessy F.M., Sonka M., Buatti J., Aylward S.R., Miller J.V., Pieper S., Kikinis R. [3D Slicer as an Image Computing Platform for the Quantitative Imaging Network](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3466397/pdf/nihms383480.pdf). Magnetic Resonance Imaging. 2012 Nov;30(9):1323-41. PMID: 22770690. PMCID: PMC3466397.

## License

Apache License, Version 2.0.
See LICENSE file for details.
