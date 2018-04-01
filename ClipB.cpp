#include <coecntrl.h>
#include <baclipb.h>
#include <txtetext.h>

#include <Python.h>
#include <symbian_python_ext_util.h>

//--------------------------------------------------------------------------

//static PyObject* Get(PyObject* /*self*/,PyObject* /*args*/)
/*{
  CPlainText* BPlainText = CPlainText::NewL();
	 CleanupStack::PushL(BPlainText);
	 CClipboard* cb =
CClipboard::NewForReadingL(CCoeEnv::Static()->FsSession());
	 CleanupStack::PushL(cb);
	 cb->StreamDictionary().At(KClipboardUidTypePlainText);
  BPlainText->PasteFromStoreL(cb->Store(), cb->StreamDictionary(), 0);
  TInt len = BPlainText->DocumentLength();

  HBufC* buffer=HBufC::NewLC(len) ;
  TPtr ptr(buffer->Des());
  BPlainText->Extract(ptr,0,len);

  //CleanupStack::PopAndDestroy(3); - ?
  
  return Py_BuildValue("u#",ptr,len);
  
}  */
//--------------------------------------------------------------------------

static PyObject* Set(PyObject* /*self*/,PyObject* args)
{
  PyObject* obj_text;
  if (!PyArg_ParseTuple(args, "U", &obj_text))
    return NULL;

  TPtrC text((TUint16*) PyUnicode_AsUnicode(obj_text),
                           PyUnicode_GetSize(obj_text));

 	CClipboard* cb=CClipboard::NewForWritingLC(CCoeEnv::Static()->FsSession());
	 cb->StreamDictionary().At(KClipboardUidTypePlainText);
	 CPlainText* BPlainText = CPlainText::NewL();
	 CleanupStack::PushL(BPlainText);
	 BPlainText->InsertL(0,text);
	 BPlainText->CopyToStoreL(cb->Store(), cb->StreamDictionary(), 0,BPlainText->DocumentLength());
	 cb->CommitL();
	 CleanupStack::PopAndDestroy(2);


 Py_INCREF(Py_None);
 return Py_None;
}
//--------------------------------------------------------------------------

static const PyMethodDef met_clipb[] = {
   // {"get", (PyCFunction)Get, METH_NOARGS},
    {"set", (PyCFunction)Set, METH_VARARGS},
    {0, 0}
};

//--------------------------------------------------------------------------

DL_EXPORT(void) MODULE_INIT_FUNC()
{
    Py_InitModule("clipb",(PyMethodDef*) met_clipb);
}
//--------------------------------------------------------------------------
