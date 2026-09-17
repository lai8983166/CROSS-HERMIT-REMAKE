
undefined4 __thiscall FUN__text1__0083d7e9(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 uVar2;
  
  iVar1 = FUN__text1__0083d81c(param_2,0,param_1);
  if (iVar1 < 0) {
    uVar2 = 0xffffffff;
  }
  else {
    uVar2 = *(undefined4 *)(*(int *)(DAT_008752c0 + iVar1 * 4) + 4);
  }
  return uVar2;
}

