
undefined4 __fastcall FUN__text__0045a190(int param_1)

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
  if (*(int *)(param_1 + 0x3c) == 0) {
    uVar1 = 0;
  }
  else {
    *(int *)(param_1 + 0x40) = *(int *)(param_1 + 0x40) + -1;
    if (*(int *)(param_1 + 0x40) < 0) {
      *(undefined4 *)(param_1 + 0x3c) = 0;
      *(undefined4 *)(param_1 + 0x48) = 1;
      uVar1 = 1;
    }
    else {
      *(int *)(param_1 + 0x44) = *(int *)(param_1 + 0x44) + -1;
      if (*(int *)(param_1 + 0x44) < 0) {
        *(undefined4 *)(param_1 + 0x44) = 1;
        *(uint *)(param_1 + 0x48) = *(uint *)(param_1 + 0x48) ^ 1;
      }
      uVar1 = 0;
    }
  }
  return uVar1;
}

