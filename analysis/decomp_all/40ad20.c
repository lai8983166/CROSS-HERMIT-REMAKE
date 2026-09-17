
void FUN__text__0040ad20(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__0040ac90(param_1);
  *(undefined4 *)(param_1 + 4) = 0;
  if (*(int *)(param_1 + 0x20) != 0) {
    iVar2 = FUN__text__00424f80("aw->link==0",
                                "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxAnim.cpp",
                                DAT_005ff104 + 4,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x40ad8d;
  FUN__text__0056ce80();
  return;
}

