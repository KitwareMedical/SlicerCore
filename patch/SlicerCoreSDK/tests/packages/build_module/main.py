from slicer import (
    vtkMRMLDisplayableManagerGroup,
    vtkMRMLApplicationLogic,
    vtkMRMLDummyDisplayableManager,
    vtkMRMLThreeDViewDisplayableManagerFactory
)

from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow
)

managers = [
    vtkMRMLDummyDisplayableManager,
]

factory = vtkMRMLThreeDViewDisplayableManagerFactory()
factory.SetMRMLApplicationLogic(vtkMRMLApplicationLogic())
for manager in managers:
    if not factory.IsDisplayableManagerRegistered(manager.__name__):
        assert factory.RegisterDisplayableManager(manager.__name__)

renderer = vtkRenderer()
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
displayable_manager_group = vtkMRMLDisplayableManagerGroup()
displayable_manager_group.Initialize(factory, renderer)
for manager in managers:
    assert displayable_manager_group.GetDisplayableManagerByClassName(manager.__name__)
