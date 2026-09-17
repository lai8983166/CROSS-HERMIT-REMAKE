
undefined4 FUN__text1__008410e6(int param_1,int param_2,uint param_3)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 local_8;
  
  local_8 = param_3;
  if (((param_1 == 0) || (*(int *)(param_1 + 0x1c) == 0)) || (**(int **)(param_1 + 0x1c) != 6)) {
    uVar1 = 0xfffffffe;
  }
  else {
    iVar2 = FUN__text1__00841580(1,param_2,param_3);
    if (iVar2 == *(int *)(param_1 + 0x30)) {
      *(undefined4 *)(param_1 + 0x30) = 1;
      if ((uint)(1 << ((byte)*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x10) & 0x1f)) <= param_3) {
        local_8 = (1 << ((byte)*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x10) & 0x1f)) - 1;
        param_2 = param_2 + (param_3 - local_8);
      }
      FUN__text1__00846198(*(undefined4 *)(*(int *)(param_1 + 0x1c) + 0x14),param_2,local_8);
      **(undefined4 **)(param_1 + 0x1c) = 7;
      uVar1 = 0;
    }
    else {
      uVar1 = 0xfffffffd;
    }
  }
  return uVar1;
}

