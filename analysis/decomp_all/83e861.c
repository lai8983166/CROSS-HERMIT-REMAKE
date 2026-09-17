
undefined4 FUN__text1__0083e861(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  
  if ((((param_1 == 0) || (*(int *)(param_1 + 0x1c) == 0)) || (*(int *)(param_1 + 0x20) == 0)) ||
     (*(int *)(param_1 + 0x24) == 0)) {
    uVar2 = 0xfffffffe;
  }
  else {
    *(undefined4 *)(param_1 + 0x14) = 0;
    *(undefined4 *)(param_1 + 8) = 0;
    *(undefined4 *)(param_1 + 0x18) = 0;
    *(undefined4 *)(param_1 + 0x2c) = 2;
    iVar1 = *(int *)(param_1 + 0x1c);
    *(undefined4 *)(iVar1 + 0x14) = 0;
    *(undefined4 *)(iVar1 + 0x10) = *(undefined4 *)(iVar1 + 8);
    if (*(int *)(iVar1 + 0x18) < 0) {
      *(undefined4 *)(iVar1 + 0x18) = 0;
    }
    *(uint *)(iVar1 + 4) = (-(uint)(*(int *)(iVar1 + 0x18) != 0) & 0x47) + 0x2a;
    *(undefined4 *)(param_1 + 0x30) = 1;
    *(undefined4 *)(iVar1 + 0x20) = 0;
    FUN__text1__00841800(iVar1);
    FUN__text1__0083f242(iVar1);
    uVar2 = 0;
  }
  return uVar2;
}

