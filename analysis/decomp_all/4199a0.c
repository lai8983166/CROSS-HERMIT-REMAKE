
void __thiscall FUN__text__004199a0(int *param_1,undefined4 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  undefined1 local_18 [4];
  undefined4 local_14;
  undefined4 local_10;
  int local_c;
  int *local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*param_1 != 0) {
    local_8 = param_1;
    iVar1 = FUN__text__00419780(param_2);
    if (iVar1 == 0) {
      _memset(local_8 + 0x5d4,0,0x10);
      local_8[0x5d4] = 0x10;
      local_8[0x5d5] = 0;
      local_8[0x5d6] = local_8[0x5d9];
      local_8[0x5d7] = 0;
      local_1c = param_3;
      if (param_3 == 1) {
        local_10 = 0x100;
      }
      else {
        local_10 = 0;
      }
      (**(code **)(*(int *)*local_8 + 0x18))
                (*local_8,local_8 + 0x4e,local_8 + 0x5d4,local_8[0x4d],0,0,local_10);
      local_20 = FUN__text__0056ce80();
      local_c = local_20;
      if (local_20 == -0x7788fff6) {
        local_14 = 0;
      }
      else if (local_20 == 0) {
        FUN__text__0041ab10();
        local_24 = param_3;
        if (param_3 == 1) {
          FUN__text__0041afd0(local_8[0x5d9],local_8[0x4e]);
          *(undefined1 *)((int)local_8 + 0x1781) = 1;
        }
        FUN__text__00419c60(local_18);
        goto LAB__text__00419b16;
      }
    }
    FUN__text__004198b0();
  }
LAB__text__00419b16:
  local_8 = (int *)0x419b23;
  FUN__text__0056ce80();
  return;
}

