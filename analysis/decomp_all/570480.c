
undefined4 FUN__text__00570480(undefined4 *param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 local_c;
  int local_8;
  
  local_c = 0;
  if (((param_1 == (undefined4 *)0x0) || (param_2 == 0)) || (param_3 == 0)) {
    iVar2 = FUN__text__00573780(0,0,0,0,&DAT_00592a18,"_CrtMemDifference: NULL state pointer.\n");
    if (iVar2 == 1) {
      pcVar1 = (code *)swi(3);
      uVar3 = (*pcVar1)();
      return uVar3;
    }
    local_c = 0;
  }
  else {
    for (local_8 = 0; local_8 < 5; local_8 = local_8 + 1) {
      param_1[local_8 + 6] =
           *(int *)(param_3 + 0x18 + local_8 * 4) - *(int *)(param_2 + 0x18 + local_8 * 4);
      param_1[local_8 + 1] =
           *(int *)(param_3 + 4 + local_8 * 4) - *(int *)(param_2 + 4 + local_8 * 4);
      if (((param_1[local_8 + 6] != 0) || (param_1[local_8 + 1] != 0)) &&
         ((local_8 != 0 && ((local_8 != 2 || ((DAT_007619c0 & 0x10) != 0)))))) {
        local_c = 1;
      }
    }
    param_1[0xb] = *(int *)(param_3 + 0x2c) - *(int *)(param_2 + 0x2c);
    param_1[0xc] = *(int *)(param_3 + 0x30) - *(int *)(param_2 + 0x30);
    *param_1 = 0;
  }
  return local_c;
}

