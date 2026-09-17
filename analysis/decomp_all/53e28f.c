
undefined4 * __fastcall FUN__text__0053e28f(undefined4 *param_1)

{
  undefined4 *puVar1;
  int iVar2;
  
  *param_1 = &PTR_DAT_005d11d0;
  param_1[1] = 1;
  param_1[2] = 0;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[10] = 0;
  param_1[0xb] = 0;
  param_1[0xd] = 0;
  param_1[0xc] = 0;
  puVar1 = param_1 + 0x10;
  iVar2 = 2;
  do {
    puVar1[-2] = 0;
    *puVar1 = 0;
    puVar1 = puVar1 + 1;
    iVar2 = iVar2 + -1;
  } while (iVar2 != 0);
  puVar1 = param_1 + 0x14;
  for (iVar2 = 0x104; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar1 = 0;
    puVar1 = puVar1 + 1;
  }
  param_1[0x118] = 0;
  param_1[0x11c] = 0;
  param_1[0x123] = 0;
  param_1[0x124] = 0;
  param_1[0x11a] = 0;
  return param_1;
}

