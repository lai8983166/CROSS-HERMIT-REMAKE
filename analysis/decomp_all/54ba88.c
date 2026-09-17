
undefined4 FUN__text__0054ba88(int param_1,int param_2,uint param_3)

{
  int iVar1;
  uint uVar2;
  undefined4 uVar3;
  
  if (((param_1 == 0) || (*(int **)(param_1 + 0x1c) == (int *)0x0)) ||
     (**(int **)(param_1 + 0x1c) != 6)) {
    uVar3 = 0xfffffffe;
  }
  else {
    iVar1 = FUN__text__0055d3c0(1,param_2,param_3);
    if (iVar1 == *(int *)(param_1 + 0x30)) {
      *(undefined4 *)(param_1 + 0x30) = 1;
      uVar2 = 1 << ((byte)*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x10) & 0x1f);
      if (uVar2 <= param_3) {
        uVar2 = uVar2 - 1;
        param_2 = param_2 + (param_3 - uVar2);
        param_3 = uVar2;
      }
      FUN__text__0055d382(*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x14),param_2,param_3);
      **(undefined4 **)(param_1 + 0x1c) = 7;
      uVar3 = 0;
    }
    else {
      uVar3 = 0xfffffffd;
    }
  }
  return uVar3;
}

