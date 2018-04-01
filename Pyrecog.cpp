/*
* ====================================================================
*  Pyrecog.cpp
*
*  Recognizer plug-in
*
* Copyright (c) 2005-2006 Nokia Corporation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
* ====================================================================
*/

#include <apmrec.h>
#include <apmstd.h>
#include <f32file.h>

#ifdef EKA2
#include <ImplementationProxy.h>
const TInt KImplementationUid = 0x101F7DA1;
#endif

#ifdef EKA2
const TUid KUidPyrecog = {0xF0201513};
#else
const TUid KUidPyrecog = {0x10201513};
#endif

class CApaPyRecognizer : public CApaDataRecognizerType
{
public:
  CApaPyRecognizer():CApaDataRecognizerType(KUidPyrecog, CApaDataRecognizerType::EHigh) {
    iCountDataTypes = 1;
  }
  virtual ~CApaPyRecognizer(){};
  virtual TUint PreferredBufSize() {return 128;}
  virtual TDataType SupportedDataTypeL(TInt /*aIndex*/) const {
    return TDataType(_L8("x-application/x-python"));
  }
#ifdef EKA2
  static CApaDataRecognizerType* CreateRecognizerL();
#endif
private:
  virtual void DoRecognizeL(const TDesC& aName, const TDesC8& aBuffer);
};

void CApaPyRecognizer::DoRecognizeL(const TDesC& aName, const TDesC8& aBuffer)
{

    TParse parse;
    parse.Set(aName, NULL, NULL);
    TPtrC ext = parse.Ext();
    if (ext.CompareF(_L(".py")) == 0)
        {
        iConfidence = ECertain;
        iDataType = TDataType(_L8("x-application/x-python"));
        }
}

#ifdef EKA2
CApaDataRecognizerType* CApaPyRecognizer::CreateRecognizerL()
{
  return new (ELeave) CApaPyRecognizer();
}

const TImplementationProxy ImplementationTable[] =
{
  IMPLEMENTATION_PROXY_ENTRY(KImplementationUid, CApaPyRecognizer::CreateRecognizerL)
};

EXPORT_C const TImplementationProxy* ImplementationGroupProxy(TInt& aTableCount)
{
  aTableCount = sizeof(ImplementationTable) / sizeof(TImplementationProxy);
  return ImplementationTable;
}
#else
EXPORT_C CApaDataRecognizerType* CreateRecognizer()
{
  return new CApaPyRecognizer;
}

GLDEF_C TInt E32Dll(TDllReason /*aReason*/)
{
  return KErrNone;
}
#endif
