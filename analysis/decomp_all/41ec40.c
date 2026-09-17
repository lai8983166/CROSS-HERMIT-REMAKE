
void FUN__text__0041ec40(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4
                        ,undefined4 param_5,undefined4 param_6,undefined4 param_7)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  undefined4 *local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  FUN__text__0041eb70();
  *local_8 = param_4;
  local_8[1] = param_3;
  if (local_8[4] == -1) {
    uVar2 = FUN__text__0041efd0();
    local_8[4] = uVar2;
  }
  local_c = FUN__text__0041f0e0(param_1,*local_8,local_8[4],param_5,param_6,param_7);
  if (local_c != 0) {
    iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\system\\directx\\DxTexPos.cpp"
                                ,DAT_005ff5bc + 0xb,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8[3] = param_2;
  local_8 = (undefined4 *)0x41ecf8;
  FUN__text__0056ce80();
  return;
}

