
undefined4 FUN__text1__0084da4c(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  
  uVar2 = 0xffffffff;
  if ((*(uint *)(param_1 + 0xc) & 0x40) == 0) {
    if ((*(uint *)(param_1 + 0xc) & 0x83) != 0) {
      uVar2 = FUN__text1__0084d552(param_1);
      FUN__text1__0084dc59(param_1);
      iVar1 = FUN__text1__0084dba6(*(undefined4 *)(param_1 + 0x10));
      if (iVar1 < 0) {
        uVar2 = 0xffffffff;
      }
      else if (*(int *)(param_1 + 0x1c) != 0) {
        FUN__text1__008497d3(*(int *)(param_1 + 0x1c));
        *(undefined4 *)(param_1 + 0x1c) = 0;
      }
    }
  }
  else {
    uVar2 = 0xffffffff;
  }
  *(undefined4 *)(param_1 + 0xc) = 0;
  return uVar2;
}

