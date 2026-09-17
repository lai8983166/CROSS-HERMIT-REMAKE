
void __thiscall FUN__text__00409e80(int param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (*(int *)(param_1 + 0x2c) != 0) {
    iVar2 = FUN__text__00424f80("PalMake==0",
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                DAT_005ff0f4 + 2,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(undefined4 *)(local_8 + 0x30 + param_3 * 4) = param_2;
  local_8 = 0x409ee4;
  FUN__text__0056ce80();
  return;
}

