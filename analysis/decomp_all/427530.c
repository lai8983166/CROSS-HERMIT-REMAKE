
void __fastcall FUN__text__00427530(undefined4 *param_1)

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
  local_8 = param_1;
  _memset(param_1 + 3,0,0xc);
  _memset(local_8 + 6,0,0xc);
  local_8[2] = 0;
  local_8[9] = 0;
  local_8 = (undefined4 *)0x4275aa;
  FUN__text__0056ce80();
  return;
}

