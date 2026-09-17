
undefined4 __fastcall FUN__text__00410a60(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [17];
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(int *)(param_1 + 0x40) == 0) {
    uVar1 = 1;
  }
  else if (*(int *)(param_1 + 0x54) < *(int *)(param_1 + 0x50)) {
    *(int *)(param_1 + 0x54) = *(int *)(param_1 + 0x54) + 1;
    *(int *)(param_1 + 0x58) = *(int *)(param_1 + 0x58) + *(int *)(param_1 + 0x5c);
    if (0xff0000 < *(int *)(param_1 + 0x58)) {
      *(undefined4 *)(param_1 + 0x58) = 0xff0000;
    }
    if (*(int *)(param_1 + 0x58) < 0x100) {
      *(undefined4 *)(param_1 + 0x58) = 0xff;
    }
    uVar1 = 0;
  }
  else {
    *(undefined4 *)(param_1 + 0x40) = 0;
    uVar1 = 1;
  }
  return uVar1;
}

