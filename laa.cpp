#include <e32std.h>
#include <Python.h>
#include <symbian_python_ext_util.h>
#include <apgcli.h> // for RApaLsSession
#include <apacmdln.h> // for CApaCommandLine

static PyObject* Execute(PyObject* , PyObject *args)
{		
	TUint address;
	PyArg_ParseTuple(args,"I",&address);
	TUid uid= TUid::Uid(address);
	RApaLsSession apaLsSession;
    apaLsSession.Connect();
    TUid aAppUid=uid;
    TApaAppInfo appInfo;
    TInt retVal = apaLsSession.GetAppInfo(appInfo, aAppUid);
 
    if(retVal == KErrNone)
        {
        CApaCommandLine* cmdLine = CApaCommandLine::NewL();
        cmdLine->SetExecutableNameL(appInfo.iFullName);
        cmdLine->SetCommandL(EApaCommandRun);
        apaLsSession.StartApp(*cmdLine);
        delete cmdLine;
		return Py_BuildValue("i",retVal);
        }
    else
        {
        return Py_BuildValue("i",retVal);
        }
}

static PyObject* Execute2(PyObject* , PyObject *args)
{		
	TUint address;
	char* _str;
	PyArg_ParseTuple(args,"Iu",&address,&_str);
	TBuf16<512> string;
	string.Copy((TUint16*)_str);
	TUid uid= TUid::Uid(address);
	RApaLsSession apaLsSession;
    apaLsSession.Connect();
    TUid aAppUid=uid;
    TApaAppInfo appInfo;
    TInt retVal = apaLsSession.GetAppInfo(appInfo, aAppUid);
 
    if(retVal == KErrNone)
        {
        CApaCommandLine* cmdLine = CApaCommandLine::NewL();
        cmdLine->SetExecutableNameL(appInfo.iFullName);
        cmdLine->SetCommandL(EApaCommandRun);
		cmdLine->SetDocumentNameL(string);
        apaLsSession.StartApp(*cmdLine);
        delete cmdLine;
		return Py_BuildValue("i",retVal);
        }
    else
        {
        return Py_BuildValue("i",retVal);
        }
}


static const PyMethodDef light_methods[] =
	{
		{"execute", (PyCFunction)Execute, METH_VARARGS},
		{"execute_param", (PyCFunction)Execute2, METH_VARARGS},
		{0, 0}
	};


DL_EXPORT(void) init_light()
	{
		PyObject *module;
		module = Py_InitModule("laa2",(PyMethodDef*) light_methods);
	}

#ifndef EKA2
//
// For Symbian or rather S60 3rd edition sdk
GLDEF_C TInt E32Dll(TDllReason)
{
  return KErrNone;
}
#endif
