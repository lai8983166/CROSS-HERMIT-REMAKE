
/* WARNING: Switch with 1 destination removed at 0x005380cf */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN__text__005380d5(undefined4 *param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  
  uVar1 = param_2[1];
  param_1[1] = param_2[4];
  param_1[4] = uVar1;
  uVar1 = param_2[2];
  param_1[2] = param_2[8];
  param_1[8] = uVar1;
  uVar1 = param_2[3];
  param_1[3] = param_2[0xc];
  param_1[0xc] = uVar1;
  uVar1 = param_2[6];
  param_1[6] = param_2[9];
  param_1[9] = uVar1;
  uVar1 = param_2[7];
  param_1[7] = param_2[0xd];
  param_1[0xd] = uVar1;
  uVar1 = param_2[0xb];
  param_1[0xb] = param_2[0xe];
  param_1[0xe] = uVar1;
  if (param_1 != param_2) {
    *param_1 = *param_2;
    param_1[5] = param_2[5];
    param_1[10] = param_2[10];
    param_1[0xf] = param_2[0xf];
  }
  return;
}

