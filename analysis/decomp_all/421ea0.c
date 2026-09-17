
void FUN__text__00421ea0(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar4 = local_48;
  for (iVar3 = 0x11; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar2 = FUN__text__0056e050(0,0,FUN__text__00421f50,param_1,4,param_1 + 0x24);
  *(undefined4 *)(param_1 + 0x20) = uVar2;
  if (*(int *)(param_1 + 0x20) == 0) {
    FUN__text__0042b2d0("ERROR:ThreadCreate(%08x):dont create thread !!\n",param_1);
    iVar3 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\system\\mtask.cpp",
                                DAT_005ff604 + 0xf,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x421f3e;
  FUN__text__0056ce80();
  return;
}

