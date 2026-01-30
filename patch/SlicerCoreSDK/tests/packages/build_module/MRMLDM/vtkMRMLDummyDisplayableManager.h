#ifndef __vtkMRMLDummyDisplayableManager_h
#define __vtkMRMLDummyDisplayableManager_h

// Dummy includes
#include "vtkDummyMRMLDisplayableManagerModule.h"

// MRML DisplayableManager includes
#include <vtkMRMLAbstractThreeDViewDisplayableManager.h>

class VTK_DUMMY_MRMLDISPLAYABLEMANAGER_EXPORT vtkMRMLDummyDisplayableManager : public vtkMRMLAbstractThreeDViewDisplayableManager
{
public:
  static vtkMRMLDummyDisplayableManager* New();
  vtkTypeMacro(vtkMRMLDummyDisplayableManager, vtkMRMLAbstractThreeDViewDisplayableManager);
  void PrintSelf(ostream& os, vtkIndent indent) override;

protected:
  vtkMRMLDummyDisplayableManager();
  ~vtkMRMLDummyDisplayableManager() override;
};

#endif
