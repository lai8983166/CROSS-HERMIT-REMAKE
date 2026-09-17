
undefined4 FUN__text1__008412f6(int param_1)

{
  undefined4 uVar1;
  
  if (((param_1 == 0) || (*(int *)(param_1 + 0x1c) == 0)) ||
     (*(int *)(*(int *)(param_1 + 0x1c) + 0x14) == 0)) {
    uVar1 = 0xfffffffe;
  }
  else {
    uVar1 = FUN__text1__008461cf(*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x14));
  }
  return uVar1;
}

