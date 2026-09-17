
void FUN__text__005749b0(EHExceptionRecord *param_1,EHRegistrationNode *param_2,_CONTEXT *param_3,
                        void *param_4,_s_FuncInfo *param_5,int param_6,int param_7,
                        EHRegistrationNode *param_8)

{
  int iVar1;
  uint local_10;
  _s_TryBlockMapEntry *local_c;
  uint local_8;
  
  iVar1 = FUN__text__005753b0();
  if ((*(int *)(iVar1 + 0x68) == 0) ||
     (iVar1 = FUN__text__0056d1f0(param_1,param_2,param_3,param_4,param_5,param_7,param_8),
     iVar1 == 0)) {
    local_c = (_s_TryBlockMapEntry *)FUN__text__0056d350(param_5,param_7,param_6,&local_10,&local_8)
    ;
    for (; local_10 < local_8; local_10 = local_10 + 1) {
      if (((local_c->tryLow <= param_6) && (param_6 <= local_c->tryHigh)) &&
         ((local_c->pHandlerArray[local_c->nCatches + -1].pType == (TypeDescriptor *)0x0 ||
          ((char)local_c->pHandlerArray[local_c->nCatches + -1].pType[1].hash == '\0')))) {
        CatchIt(param_1,param_2,param_3,param_4,param_5,
                local_c->pHandlerArray + local_c->nCatches + -1,(_s_CatchableType *)0x0,local_c,
                param_7,param_8,'\x01');
      }
      local_c = local_c + 1;
    }
  }
  return;
}

