
void FUN__text1__0083d8bf(undefined4 param_1,undefined4 param_2)

{
  void *pvVar1;
  int iVar2;
  undefined4 *local_1c;
  
  iVar2 = FUN__text1__0083d81c(param_1,1);
  pvVar1 = DAT_008752c0;
  if (-1 < iVar2) {
    if (DAT_0087542c == DAT_00875430) {
      DAT_00875430 = DAT_00875430 << 1;
      if (DAT_00875430 == 0) {
        DAT_00875430 = 0x100;
      }
      DAT_008752c0 = operator_new(DAT_00875430 << 2);
      FUN__text1__00848490(DAT_008752c0,pvVar1,DAT_0087542c << 2);
      FUN__text1__00848476(pvVar1);
    }
    FUN__text1__008487d0
              ((int)DAT_008752c0 + iVar2 * 4 + 4,(void *)((int)DAT_008752c0 + iVar2 * 4),
               (DAT_0087542c - iVar2) * 4);
    local_1c = operator_new(8);
    if (local_1c == (undefined4 *)0x0) {
      local_1c = (undefined4 *)0x0;
    }
    else {
      *local_1c = param_1;
      local_1c[1] = param_2;
    }
    *(undefined4 **)((int)DAT_008752c0 + iVar2 * 4) = local_1c;
    DAT_0087542c = DAT_0087542c + 1;
  }
  return;
}

