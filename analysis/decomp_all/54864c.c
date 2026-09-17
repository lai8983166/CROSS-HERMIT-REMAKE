
int __fastcall FUN__text__0054864c(int param_1)

{
  int iVar1;
  bool bVar2;
  uint local_18;
  uint local_14;
  undefined4 local_10;
  undefined4 *local_8;
  
  if (*(int *)(param_1 + 0x10) == 0) {
    bVar2 = *(int *)(param_1 + 0x50) == 0;
    if (bVar2) {
      local_10 = 0;
      local_18 = 8;
    }
    else {
      local_10 = 0x200;
      local_18 = 1;
    }
    iVar1 = FUN__text__0052755e(*(undefined4 *)(param_1 + 4),param_1 + 0x58,
                                (undefined4 *)(param_1 + 0x5c),0,local_10,
                                (undefined4 *)(param_1 + 0x54),bVar2);
    if (-1 < iVar1) {
      local_14 = 0;
      if (local_18 != 0) {
        local_8 = (undefined4 *)(param_1 + 0x10);
        do {
          iVar1 = FUN__text__005275d7(*(undefined4 *)(param_1 + 4),*(undefined4 *)(param_1 + 0x58),
                                      *(undefined4 *)(param_1 + 0x5c),1,local_10,
                                      *(undefined4 *)(param_1 + 0x54),bVar2,local_8);
          if (iVar1 < 0) {
            return iVar1;
          }
          iVar1 = (**(code **)(*(int *)*local_8 + 0x3c))((int *)*local_8,0,local_8 + 8);
          if (iVar1 < 0) {
            return iVar1;
          }
          local_14 = local_14 + 1;
          local_8 = local_8 + 1;
        } while (local_14 < local_18);
      }
      iVar1 = 0;
    }
  }
  else {
    iVar1 = 0;
  }
  return iVar1;
}

