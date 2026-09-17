
undefined4 FUN__text1__008407c0(int param_1)

{
  undefined4 uVar1;
  
  if ((param_1 == 0) || (*(int *)(param_1 + 0x1c) == 0)) {
    uVar1 = 0xfffffffe;
  }
  else {
    *(undefined4 *)(param_1 + 0x14) = 0;
    *(undefined4 *)(param_1 + 8) = 0;
    *(undefined4 *)(param_1 + 0x18) = 0;
    **(uint **)(param_1 + 0x1c) = -(uint)(*(int *)(*(int *)(param_1 + 0x1c) + 0xc) != 0) & 7;
    FUN__text1__00844c00(*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x14),param_1,0);
    uVar1 = 0;
  }
  return uVar1;
}

