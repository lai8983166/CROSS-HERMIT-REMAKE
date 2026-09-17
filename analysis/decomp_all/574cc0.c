
/* Library Function - Single Match
    void __cdecl CatchIt(struct EHExceptionRecord *,struct EHRegistrationNode *,struct _CONTEXT
   *,void *,struct _s_FuncInfo const *,struct _s_HandlerType const *,struct _s_CatchableType const
   *,struct _s_TryBlockMapEntry const *,int,struct EHRegistrationNode *,unsigned char)
   
   Library: Visual Studio */

void __cdecl
CatchIt(EHExceptionRecord *param_1,EHRegistrationNode *param_2,_CONTEXT *param_3,void *param_4,
       _s_FuncInfo *param_5,_s_HandlerType *param_6,_s_CatchableType *param_7,
       _s_TryBlockMapEntry *param_8,int param_9,EHRegistrationNode *param_10,uchar param_11)

{
  int iVar1;
  
  if (param_7 != (_s_CatchableType *)0x0) {
    FUN__text__00574f20(param_1,param_2,param_6,param_7);
  }
  if (param_10 == (EHRegistrationNode *)0x0) {
    FUN__text__0056d070(param_2,param_1);
  }
  else {
    FUN__text__0056d070(param_10,param_1);
  }
  FUN__text__00574b90(param_2,param_4,param_5,param_8->tryLow);
  *(__ehstate_t *)(param_2 + 8) = param_8->tryHigh + 1;
  iVar1 = FUN__text__00574d80(param_1,param_2,param_3,param_5,param_6->addressOfHandler,param_9,
                              0x100);
  if (iVar1 != 0) {
    FUN__text__0056d000(iVar1,param_2);
  }
  return;
}

