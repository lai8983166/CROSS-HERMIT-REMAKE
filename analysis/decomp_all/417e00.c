
void __fastcall FUN__text__00417e00(undefined4 *param_1)

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
  param_1[0x4d] = 0;
  param_1[0x4e] = 0;
  param_1[0x5db] = 0xffffffff;
  param_1[0x5b] = 0;
  local_8 = param_1;
  _memset(param_1 + 0x4f,0,0x30);
  local_8[0x5dd] = 0;
  *(undefined1 *)(local_8 + 0x5c) = 0;
  local_8[0x5d8] = 0;
  local_8[0x5d9] = 0;
  local_8[0x5da] = 0;
  *(undefined1 *)(local_8 + 0x5dc) = 0;
  local_8[0x5de] = 0;
  local_8[0x5df] = 0;
  _memset(local_8 + 0x5d,0,0xd0);
  _memset(local_8 + 0x91,0,0x150c);
  _memset(local_8 + 3,0,0x100);
  _memset(local_8 + 0x43,0,0x28);
  FUN__text__0041ab10();
  local_8 = (undefined4 *)0x417f59;
  FUN__text__0056ce80();
  return;
}

