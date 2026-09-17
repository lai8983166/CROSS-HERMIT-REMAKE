
undefined4 FUN__text1__0083e6c1(int param_1,int param_2,uint param_3)

{
  int iVar1;
  undefined4 uVar2;
  uint local_14;
  uint local_c;
  
  local_c = param_3;
  if ((((param_1 == 0) || (*(int *)(param_1 + 0x1c) == 0)) || (param_2 == 0)) ||
     (*(int *)(*(int *)(param_1 + 0x1c) + 4) != 0x2a)) {
    uVar2 = 0xfffffffe;
  }
  else {
    iVar1 = *(int *)(param_1 + 0x1c);
    uVar2 = FUN__text1__00841580(*(undefined4 *)(param_1 + 0x30),param_2,param_3);
    *(undefined4 *)(param_1 + 0x30) = uVar2;
    if (param_3 < 3) {
      uVar2 = 0;
    }
    else {
      if (*(int *)(iVar1 + 0x24) - 0x106U < param_3) {
        local_c = *(int *)(iVar1 + 0x24) - 0x106;
        param_2 = param_2 + (param_3 - local_c);
      }
      FUN__text1__00848490(*(undefined4 *)(iVar1 + 0x30),param_2,local_c);
      *(uint *)(iVar1 + 100) = local_c;
      *(uint *)(iVar1 + 0x54) = local_c;
      *(uint *)(iVar1 + 0x40) = (uint)**(byte **)(iVar1 + 0x30);
      *(uint *)(iVar1 + 0x40) =
           (*(int *)(iVar1 + 0x40) << ((byte)*(undefined4 *)(iVar1 + 0x50) & 0x1f) ^
           (uint)*(byte *)(*(int *)(iVar1 + 0x30) + 1)) & *(uint *)(iVar1 + 0x4c);
      for (local_14 = 0; local_14 <= local_c - 3; local_14 = local_14 + 1) {
        *(uint *)(iVar1 + 0x40) =
             (*(int *)(iVar1 + 0x40) << ((byte)*(undefined4 *)(iVar1 + 0x50) & 0x1f) ^
             (uint)*(byte *)(*(int *)(iVar1 + 0x30) + 2 + local_14)) & *(uint *)(iVar1 + 0x4c);
        *(undefined2 *)(*(int *)(iVar1 + 0x38) + (local_14 & *(uint *)(iVar1 + 0x2c)) * 2) =
             *(undefined2 *)(*(int *)(iVar1 + 0x3c) + *(int *)(iVar1 + 0x40) * 2);
        *(undefined2 *)(*(int *)(iVar1 + 0x3c) + *(int *)(iVar1 + 0x40) * 2) = (undefined2)local_14;
      }
      uVar2 = 0;
    }
  }
  return uVar2;
}

