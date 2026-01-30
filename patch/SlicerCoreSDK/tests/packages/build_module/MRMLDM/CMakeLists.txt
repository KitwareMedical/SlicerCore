set(classes vtkMRMLDummyDisplayableManager)

foreach(class IN LISTS classes)
  vtk_object_factory_declare(BASE ${class} OVERRIDE ${class})
endforeach()

set_property(GLOBAL PROPERTY "_vtk_module_autoinit_include" "\"vtkAutoInit.h\"")
vtk_object_factory_configure(
  SOURCE_FILE vtk_object_factory_source
  HEADER_FILE vtk_object_factory_header
  EXPORT_MACRO ""
)

vtk_module_add_module(Dummy::MRMLDisplayableManager
  EXPORT_MACRO_PREFIX VTK_DUMMY_MRMLDISPLAYABLEMANAGER
  CLASSES ${classes}
  SOURCES ${vtk_object_factory_source}
  PRIVATE_HEADERS ${vtk_object_factory_header}
)

vtk_module_definitions(Dummy::MRMLDisplayableManager PRIVATE
  "vtkDummyMRMLDisplayableManager_AUTOINIT=1(vtkDummyMRMLDisplayableManager)")
