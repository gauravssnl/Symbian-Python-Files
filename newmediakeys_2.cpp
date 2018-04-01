
#include "mediakeys.h"

  
//----------------------------------------------------------------------------


 void CMediaKeysTestUi::ConstructL()
 { 

    iInterfaceSelector =CRemConInterfaceSelector::NewL();
    iCoreTarget = CRemConCoreApiTarget::NewL(*iInterfaceSelector, *this);
    iInterfaceSelector->OpenTargetL();
    iTimer = CPeriodic::NewL(CActive::EPriorityUserInput);
    iNum=0;
 }
 
//----------------------------------------------------------------------------
CMediaKeysTestUi::CMediaKeysTestUi():iCb(NULL)
{
}

//---------------------------------------------------------------------------
CMediaKeysTestUi::~CMediaKeysTestUi()
{ 
   iTimer->Cancel();
   delete iTimer;
   delete iInterfaceSelector;
   delete iCoreTarget;// EKERN-EXEC 3  
   Py_XDECREF(iCb); 
}

//---------------------------------------------------------------------------

void CMediaKeysTestUi::CallPy()
{  
  PyObject *arglist;
  arglist = Py_BuildValue("(i)", iNum);
  PyEval_RestoreThread(PYTHON_TLS->thread_state);
  PyEval_CallObject(iCb, arglist);
  PyEval_SaveThread(); 
  Py_DECREF(arglist);
}


//---------------------------------------------------------------------------
  void CMediaKeysTestUi::MrccatoCommand(TRemConCoreApiOperationId aOperationId,
                                        TRemConCoreApiButtonAction aButtonAct)
  {
    TRequestStatus status;
    iNum=0;

     switch( aOperationId )
        {
        case ERemConCoreApiPausePlayFunction:
            {
            switch (aButtonAct)
                {
                  
                 case ERemConCoreApiButtonPress:
                   iNum=5;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=6;
                   break;

                case ERemConCoreApiButtonClick:
                   iNum=17;
                   break;

                default: break;
                }                               
     
            iCoreTarget->PausePlayFunctionResponse(status, KErrNone);
            User::WaitForRequest(status);
            break;
            }   
 
 
 
        case ERemConCoreApiStop:
            {
           switch (aButtonAct)
                {
                 case ERemConCoreApiButtonPress:
                   iNum=7;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=8;
                   break;

                case ERemConCoreApiButtonClick:
                   iNum=18;
                   break;
                
                default: break;
                }
                
            iCoreTarget->StopResponse(status, KErrNone);
            User::WaitForRequest(status);
            break;
            }
            
            
            
        case ERemConCoreApiRewind:
            {
           switch (aButtonAct)
                {
                 case ERemConCoreApiButtonPress:
                   iNum=9;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=10;
                   break;

                 case ERemConCoreApiButtonClick:
                   iNum=19;
                   break;
                
                default: break;
                }
            
            iCoreTarget->RewindResponse(status, KErrNone);
            User::WaitForRequest(status);   
            break;
            }       
        case ERemConCoreApiForward:
            {
           switch (aButtonAct)
                {
                 case ERemConCoreApiButtonPress:
                   iNum=15;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=16;
                   break;

                 case ERemConCoreApiButtonClick:
                   iNum=20;
                   break;
                            
                default: break;
                }

            iCoreTarget->ForwardResponse(status, KErrNone);
            User::WaitForRequest(status);
            break;
            }
        case ERemConCoreApiVolumeUp:
            { 
              
           switch (aButtonAct)
                {

                 case ERemConCoreApiButtonPress:
                   iNum=1;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=2;
                   break;

                 case ERemConCoreApiButtonClick:
                   iNum=21;
                   break;
                
                
                default: break;
                }

            iCoreTarget->VolumeUpResponse(status, KErrNone);
            User::WaitForRequest(status);   
            break;
            }       
        case ERemConCoreApiVolumeDown:
            {
           switch (aButtonAct)
                {
                 case ERemConCoreApiButtonPress:
                   iNum=3;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=4; 
                   break;
                   
                 case ERemConCoreApiButtonClick:
                   iNum=22;
                   break;
                  
                default: break;
                }

            
            iCoreTarget->VolumeDownResponse(status, KErrNone);
            User::WaitForRequest(status);   
            break;
            }
            
            
        case ERemConCoreApiFastForward:
            {
           switch (aButtonAct)
                {
                 case ERemConCoreApiButtonPress:
                   iNum=11;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=12;
                   break;

                 case ERemConCoreApiButtonClick:
                   iNum=23;
                   break;
                  
                
                default: break;
                }
            
            iCoreTarget->FastForwardResponse(status, KErrNone);
            User::WaitForRequest(status);
            break;
            } 
                         
        case ERemConCoreApiBackward:
            {
           switch (aButtonAct)
                {

                 case ERemConCoreApiButtonPress:
                   iNum=13;
                   break;
                    
                 case ERemConCoreApiButtonRelease:
                   iNum=14;
                   break;

                 case ERemConCoreApiButtonClick:
                   iNum=24;
                   break;
                  
                
                default: break;
                }
            
            iCoreTarget->BackwardResponse(status, KErrNone);
            User::WaitForRequest(status);
            break;
            }                   
        default: break;
       }
       
      
     if(iNum) 
     {
       if( iNum==1 || iNum==3 )
         iTimer->Start(200000,200000, TCallBack(CTimerCallBack, this));
       else
       {
         iTimer->Cancel();
         CallPy();
       }
     }
    
    }
//---------------------------------------------------------------------------

TInt CMediaKeysTestUi::CTimerCallBack(TAny* aPtr) 
 {
    CMediaKeysTestUi* self = static_cast<CMediaKeysTestUi*>(aPtr);   
    self->CallPy();
    return 0;
 }
//---------------------------------------------------------------------------

#define Mediakey_type ((PyTypeObject*)SPyGetGlobalString("MediaKeys"))
struct obj_Mediakey {
  PyObject_VAR_HEAD  // PyObject_HEAD;
  CMediaKeysTestUi* iMediaKeysTestUi;
};


//---------------------------------------------------------------------------

static PyObject* New_Mediakey(obj_Mediakey* self, PyObject* args)

{

    PyObject *c = NULL;

    if (!PyArg_ParseTuple(args, "O:set_callback", &c))
    return NULL;


    obj_Mediakey *ir = PyObject_New(obj_Mediakey, Mediakey_type);
    if (!ir) return NULL;

    ir->iMediaKeysTestUi = 0;
    TRAPD(err,
          ir->iMediaKeysTestUi  = new CMediaKeysTestUi(); 
          ir->iMediaKeysTestUi->ConstructL();
          ir->iMediaKeysTestUi->iCb = c;
          Py_XINCREF(ir->iMediaKeysTestUi->iCb);

         );

    if (err)
    {
      PyObject_Del(ir);
      return SPyErr_SetFromSymbianOSErr(err);
    }

  return (PyObject*)ir;
}



//---------------------------------------------------------------------------

static void dealloc_Audiostream(obj_Mediakey* audiostream)
{ 
 //memory leaks ?
 delete audiostream->iMediaKeysTestUi;
 audiostream->iMediaKeysTestUi = NULL;
 
  audiostream->iMediaKeysTestUi->iTimer->Cancel();
  delete  audiostream->iMediaKeysTestUi->iTimer;
  delete audiostream->iMediaKeysTestUi->iInterfaceSelector;
  Py_XDECREF(audiostream->iMediaKeysTestUi->iCb);
 
  PyObject_Del(audiostream);    
}
 


static const PyTypeObject type_template_Mediakeys = {
    PyObject_HEAD_INIT(0)   
    0,                 /*ob_size*/
    "mediakeys.New",            /*tp_name*/
    sizeof(obj_Mediakey), /*tp_basicsize*/
    0,                 /*tp_itemsize*/
    /* methods */
    (destructor)dealloc_Audiostream, /*tp_dealloc*/
    0, /*tp_print*/

}; 


static const PyMethodDef mediakeys_methods[] =
{
  {"New", (PyCFunction)New_Mediakey, METH_VARARGS},
  {0, 0} 
};


#define DEFTYPE(name,type_template)  do {\
    PyTypeObject* tmp = PyObject_New(PyTypeObject, &PyType_Type);\
    *tmp = (type_template);\
    tmp->ob_type = &PyType_Type;\
    SPyAddGlobalString((name), (PyObject*)tmp);\
  } while (0)
 


extern "C" {

 DL_EXPORT(void) initaudiostream(void)
 {
    PyObject *m;
    DEFTYPE("MediaKeys",type_template_Mediakeys);
    m = Py_InitModule("mediakeys", (PyMethodDef*)mediakeys_methods); 
    PyModule_GetDict(m);    
 }
        

} 
















