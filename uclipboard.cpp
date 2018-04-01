#include <coecntrl.h>
#include <baclipb.h>
#include <txtetext.h>
#include <coemain.h>

#include <txtetext.h>

#include <s32ucmp.h>
#include <s32std.h>

#include <Python.h>
#include <symbian_python_ext_util.h>

#define MAJOR_VERSION 1
#define MINOR_VERSION 0
#define BUILD_VERSION 0

//
// uset and uget : http://symbianic-life.blogspot.be/2010/03/integrate-with-symbian-clipboard.html
// changes : unicode support 
//           text can be of arbitrary length
//           line delimiter can be unix or whatever
// Author : Yury Schkatula
//

//TDesC * ReadFromClipboardL(RFs & aFs)
static PyObject* uGet(PyObject* /*self*/,PyObject* /*args*/)
{
    //TDesC *result = NULL;
    CClipboard *cb = CClipboard::NewForReadingLC(CCoeEnv::Static()->FsSession());//CleanupStack

    TStreamId stid = cb->StreamDictionary().At(KClipboardUidTypePlainText);
    PyObject* arg1;
    if (KNullStreamId != stid)
    {
        RStoreReadStream stream;
        stream.OpenL(cb->Store(), stid);
        TInt32 size ;
        size=stream.ReadInt32L();

        HBufC *buf = HBufC::NewLC(size);
        buf->Des().SetLength(size);

        TUnicodeExpander e;
        TMemoryUnicodeSink sink(&buf->Des()[0]);
        e.ExpandL(sink, stream, size);
        
        arg1 = Py_BuildValue("u#",buf->Ptr(),buf->Length());
          
        stream.Close();
        CleanupStack::PopAndDestroy(buf); 

    }
    CleanupStack::PopAndDestroy(cb);

    if (!arg1)
    // should have set an exception
      return NULL;
    return arg1;

}

//--------------------------------------------------------------------------

static PyObject* Get(PyObject* /*self*/,PyObject* /*args*/)
{
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

  CleanupStack::PopAndDestroy(BPlainText);
  CleanupStack::PopAndDestroy(cb);  
  PyObject* arg = Py_BuildValue("u#",buffer->Ptr(),len);
  CleanupStack::PopAndDestroy(buffer);
  
  return arg;
} 
//--------------------------------------------------------------------------

static PyObject* uSet(PyObject* /*self*/,PyObject* args)
//void WriteToClipboardL(RFs &aFs, const TDesC & aText)
{
  PyObject* obj_text;
  if (!PyArg_ParseTuple(args, "U", &obj_text))
     return NULL;

  TPtrC text((TUint16*) PyUnicode_AsUnicode(obj_text),
                        PyUnicode_GetSize(obj_text));


    CClipboard* cb=CClipboard::NewForWritingLC(CCoeEnv::Static()->FsSession());

    RStoreWriteStream stream;
    TStreamId stid = stream.CreateLC(cb->Store());
    stream.WriteInt32L(text.Length());

    TUnicodeCompressor c;
    TMemoryUnicodeSource source(text.Ptr());
    TInt bytes(0);
    TInt words(0);
    c.CompressL(stream, source, KMaxTInt, text.Length(), &bytes, &words);

    stream.WriteInt8L(0); // magic command! :)

    stream.CommitL();
    cb->StreamDictionary().AssignL(KClipboardUidTypePlainText, stid);
    cb->CommitL();

    stream.Close();
    CleanupStack::PopAndDestroy(); // stream.CreateLC
    CleanupStack::PopAndDestroy(cb);

 Py_INCREF(Py_None);
 return Py_None;


}

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

static const PyMethodDef met_uclipboard[] = {
    {"get", (PyCFunction)Get, METH_NOARGS},
    {"set", (PyCFunction)Set, METH_VARARGS},
    {"uset", (PyCFunction)uSet, METH_VARARGS},   
    {"uget", (PyCFunction)uGet, METH_NOARGS},   
    {0, 0}
};

//--------------------------------------------------------------------------

#ifndef EKA2
GLDEF_C TInt E32Dll(TDllReason)
{
  return KErrNone;
}
#endif


DL_EXPORT(void) MODULE_INIT_FUNC()
{
    PyObject* module= Py_InitModule3("uclipboard",(PyMethodDef*) met_uclipboard,"uclipboard for PyS60 by cyke64@gmail.com (c) 2012 Apache 2 License");
    PyObject *dict;
    dict = PyModule_GetDict(module);
    PyDict_SetItemString(dict,"version", Py_BuildValue("(iii)",MAJOR_VERSION,MINOR_VERSION,BUILD_VERSION));
	
 
  if (!module)
    {
      return;
    }
}



//--------------------------------------------------------------------------
