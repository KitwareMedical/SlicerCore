#include "vtkMRMLDummyDisplayableManager.h"

#include <vtkObjectFactory.h>

//---------------------------------------------------------------------------
vtkStandardNewMacro(vtkMRMLDummyDisplayableManager)

//---------------------------------------------------------------------------
vtkMRMLDummyDisplayableManager::vtkMRMLDummyDisplayableManager()
{

}

//---------------------------------------------------------------------------
vtkMRMLDummyDisplayableManager::~vtkMRMLDummyDisplayableManager()
{
  
}

//---------------------------------------------------------------------------
void vtkMRMLDummyDisplayableManager::PrintSelf(ostream& os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
  os << indent << "vtkMRMLDummyDisplayableManager: " << this->GetClassName() << "\n";
}
