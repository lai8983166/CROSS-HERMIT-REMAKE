
void __fastcall FUN__text__0041d2e0(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 *local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[6] = 0;
  param_1[7] = 0;
  param_1[0x92] = 0;
  param_1[0x94] = 0;
  param_1[0x96] = 0;
  param_1[0x97] = 0x3ff00000;
  *(undefined1 *)(param_1 + 8) = 0;
  *(undefined1 *)((int)param_1 + 0x21) = 0;
  *(undefined1 *)((int)param_1 + 0x22) = 0;
  *(undefined1 *)((int)param_1 + 0x23) = 0;
  local_8 = param_1;
  FUN__text__0041e6b0();
  local_8 = (undefined4 *)0x41d3b1;
  FUN__text__0056ce80();
  return;
}

