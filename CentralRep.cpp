#include <e32std.h>
#include <e32base.h>
#include <Python.h>
#include <symbian_python_ext_util.h>
#include <centralrepository.h>
#include <e32event.h>

//static PyObject* EmulKey(PyObject* , PyObject *args)
//{
//		TInt integr=-1;
//		PyArg_ParseTuple(args,"i",&integr);
//		TRawEvent lEvent;
//		lEvent.Set(TRawEvent::EKeyDown, integr);
//		UserSvr::AddEvent(lEvent);
//		lEvent.Set(TRawEvent::EKeyUp, integr);
//		UserSvr::AddEvent(lEvent); 
//		return Py_None;
//}

static PyObject* Get_Int(PyObject* , PyObject *args)
{
  TUint address;
		TUint parameter;
		TInt integr=-1;

		PyArg_ParseTuple(args,"II",&address,&parameter);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Get(parameter, integr);
  CleanupStack::PopAndDestroy(rep);
		if (res == KErrNone)
			return Py_BuildValue("i",integr);
		else
			return Py_BuildValue("i",res); 
}


static PyObject* Get_Str(PyObject* , PyObject *args)
{
	TUint address;
	TUint parameter;
 TBuf<255> gstring;
	PyArg_ParseTuple(args,"II",&address,&parameter);
	TUid uid= TUid::Uid(address);
	CRepository* rep = CRepository::NewLC(uid);
	TInt res = rep->Get(parameter, gstring);
 CleanupStack::PopAndDestroy(rep);
	gstring.Append(0);
	if (res == KErrNone)
		return Py_BuildValue("u",(TBuf<255>*)gstring.Ptr());
	else
		return Py_BuildValue("i",res);
} 

static PyObject* Get_Real(PyObject* , PyObject *args)
{		TUint address;
		TUint parameter;
		TReal value=-1;

		PyArg_ParseTuple(args,"II",&address,&parameter);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Get(parameter, value);
  CleanupStack::PopAndDestroy(rep);
		if (res == KErrNone)
			return Py_BuildValue("d",value);
		else
			return Py_BuildValue("i",res);
}

static PyObject* Set_Int(PyObject* , PyObject *args)
{
		TUint address;
		TUint parameter;
		TInt integr;
		
		PyArg_ParseTuple(args,"IIi",&address,&parameter,&integr);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Set(parameter, integr); 
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Set_Real(PyObject* , PyObject *args)
{
		TUint address;
		TUint parameter;
		TReal value=-1;
		
		PyArg_ParseTuple(args,"IId",&address,&parameter,&value);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Set(parameter, value);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Set_Str(PyObject* , PyObject *args)
{
		TUint address;
		TUint parameter;
		char* _str;

		PyArg_ParseTuple(args,"IIu",&address,&parameter,&_str);

		TBuf<255> string;

		string.Copy((TUint16*)_str);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Set(parameter, string);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Create_Int(PyObject* , PyObject *args)
{
		TUint address;
		TUint parameter;
		TInt integr;
		
		PyArg_ParseTuple(args,"IIi",&address,&parameter,&integr);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Create(parameter, integr);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Create_Real(PyObject* , PyObject *args)
{
		TUint address;
		TUint parameter;
		TReal value=-1;
		
		PyArg_ParseTuple(args,"IId",&address,&parameter,&value);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Create(parameter, value);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Create_Str(PyObject* , PyObject *args)
{
		TUint address;
		TUint parameter;
		char* _str;

		PyArg_ParseTuple(args,"IIu",&address,&parameter,&_str);

		TBuf<255> string;

		string.Copy((TUint16*)_str);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Create(parameter, string);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Delete(PyObject* , PyObject *args)
{		TUint address;
		TUint parameter;

		PyArg_ParseTuple(args,"II",&address,&parameter);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Delete(parameter);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Reset(PyObject* , PyObject *args)
{		TUint address;
		TUint parameter;

		PyArg_ParseTuple(args,"II",&address,&parameter);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Reset(parameter);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("i",res);
}

static PyObject* Move(PyObject* , PyObject *args)
{	TUint address;
		TUint parameter1;
		TUint parameter2;
		TUint mask;
		TUint32 errk;

		PyArg_ParseTuple(args,"IIII",&address,&parameter1,&parameter2,&mask);
		TUid uid= TUid::Uid(address);
		CRepository* rep = CRepository::NewLC(uid);
		TInt res = rep->Move(parameter1,parameter2,mask,errk);
  CleanupStack::PopAndDestroy(rep);
		return Py_BuildValue("(ii)",res,errk);
}

static const PyMethodDef methods[] =
	{
		{"get_int", (PyCFunction)Get_Int, METH_VARARGS},
		{"get_real", (PyCFunction)Get_Real, METH_VARARGS},
		{"get_str", (PyCFunction)Get_Str, METH_VARARGS},
		{"set_int",(PyCFunction)Set_Int,METH_VARARGS},
		{"set_real",(PyCFunction)Set_Real,METH_VARARGS},
		{"set_str",(PyCFunction)Set_Str,METH_VARARGS},
		{"create_int",(PyCFunction)Create_Int,METH_VARARGS},
		{"create_real",(PyCFunction)Create_Real,METH_VARARGS},
		{"create_str",(PyCFunction)Create_Str,METH_VARARGS},
		{"delete",(PyCFunction)Delete,METH_VARARGS},
		{"reset",(PyCFunction)Reset,METH_VARARGS},
		{"move",(PyCFunction)Move,METH_VARARGS},
//		{"emulkey",(PyCFunction)EmulKey,METH_VARARGS},
		{0, 0}
	};


DL_EXPORT(void) init_CentralRepository()
	{
		PyObject *module;
		module = Py_InitModule("CRepository",(PyMethodDef*)methods);
	}

#ifndef EKA2
//
// For Symbian or rather S60 3rd edition sdk
GLDEF_C TInt E32Dll(TDllReason)
{
  return KErrNone;
}
#endif
