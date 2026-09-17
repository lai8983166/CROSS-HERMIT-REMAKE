
void FUN__text__00574710(EHExceptionRecord *param_1,EHRegistrationNode *param_2,_CONTEXT *param_3,
                        void *param_4,_s_FuncInfo *param_5,char param_6,int param_7,
                        EHRegistrationNode *param_8)

{
  int iVar1;
  int local_28;
  int local_24;
  _s_HandlerType *local_20;
  undefined4 *local_1c;
  uint local_18;
  _s_TryBlockMapEntry *local_14;
  uint local_10;
  uchar local_c;
  int local_8;
  
  local_c = '\0';
  local_8 = *(int *)(param_2 + 8);
  if ((local_8 < -1) || (param_5->maxState <= local_8)) {
    FUN__text__00575630();
  }
  if ((((*(int *)param_1 == -0x1f928c9d) && (*(int *)(param_1 + 0x10) == 3)) &&
      (*(int *)(param_1 + 0x14) == 0x19930520)) && (*(int *)(param_1 + 0x1c) == 0)) {
    iVar1 = FUN__text__005753b0();
    if (*(int *)(iVar1 + 0x6c) == 0) {
      return;
    }
    iVar1 = FUN__text__005753b0();
    param_1 = *(EHExceptionRecord **)(iVar1 + 0x6c);
    iVar1 = FUN__text__005753b0();
    param_3 = *(_CONTEXT **)(iVar1 + 0x70);
    local_c = '\x01';
    iVar1 = FUN__text__00585990(param_1,1);
    if (iVar1 == 0) {
      FUN__text__00575630();
    }
    if (((*(int *)param_1 == -0x1f928c9d) && (*(int *)(param_1 + 0x10) == 3)) &&
       ((*(int *)(param_1 + 0x14) == 0x19930520 && (*(int *)(param_1 + 0x1c) == 0)))) {
      FUN__text__00575630();
    }
  }
  if (((*(int *)param_1 == -0x1f928c9d) && (*(int *)(param_1 + 0x10) == 3)) &&
     (*(int *)(param_1 + 0x14) == 0x19930520)) {
    local_14 = (_s_TryBlockMapEntry *)
               FUN__text__0056d350(param_5,param_7,local_8,&local_18,&local_10);
    for (; local_18 < local_10; local_18 = local_18 + 1) {
      if ((local_14->tryLow <= local_8) && (local_8 <= local_14->tryHigh)) {
        local_20 = local_14->pHandlerArray;
        for (local_28 = local_14->nCatches; 0 < local_28; local_28 = local_28 + -1) {
          local_1c = *(undefined4 **)(*(int *)(param_1 + 0x1c) + 0xc);
          for (local_24 = **(int **)(*(int *)(param_1 + 0x1c) + 0xc); local_1c = local_1c + 1,
              0 < local_24; local_24 = local_24 + -1) {
            iVar1 = FUN__text__00574ad0(local_20,*local_1c,*(undefined4 *)(param_1 + 0x1c));
            if (iVar1 != 0) {
              CatchIt(param_1,param_2,param_3,param_4,param_5,local_20,(_s_CatchableType *)*local_1c
                      ,local_14,param_7,param_8,local_c);
              goto LAB__text__00574852;
            }
          }
          local_20 = local_20 + 1;
        }
      }
LAB__text__00574852:
      local_14 = local_14 + 1;
    }
    if (param_6 != '\0') {
      ___DestructExceptionObject(param_1,1);
    }
  }
  else if (param_6 == '\0') {
    FUN__text__005749b0(param_1,param_2,param_3,param_4,param_5,local_8,param_7,param_8);
  }
  else {
    FUN__text__00575580();
  }
  return;
}

