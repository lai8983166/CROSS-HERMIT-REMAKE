
void FUN__text__0042b6c0(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        ,undefined4 param_5)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [11];
  undefined4 uStack_1c;
  undefined4 *local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__0042b660();
  local_8[1] = param_1;
  local_8[2] = param_2;
  (*API_COMCTL32_DLL_ImageList_Create)(local_8[1],local_8[2],param_3,param_4,param_5);
  uVar1 = FUN__text__0056ce80();
  *local_8 = uVar1;
  uStack_1c = 0x42b743;
  FUN__text__0056ce80();
  return;
}

