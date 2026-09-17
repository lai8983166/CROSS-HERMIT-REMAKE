
void __fastcall FUN__text__0040d7e0(undefined4 *param_1)

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
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[0xc] = 0;
  param_1[7] = 0;
  param_1[0xd] = 0;
  param_1[9] = 0;
  param_1[6] = 1;
  param_1[8] = 1;
  local_8 = param_1;
  FUN__text__004107b0();
  local_8 = (undefined4 *)0x40d878;
  FUN__text__0056ce80();
  return;
}

