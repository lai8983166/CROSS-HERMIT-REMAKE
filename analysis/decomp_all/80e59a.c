
void FUN__text1__0080e59a(byte *param_1,undefined1 *param_2,int param_3)

{
  undefined1 *puVar1;
  undefined1 uVar2;
  undefined1 local_114 [256];
  int local_14;
  byte *local_10;
  undefined1 *local_c;
  byte *local_8;
  
  for (local_14 = 0; local_14 < 0x100; local_14 = local_14 + 1) {
    local_114[local_14] = (undefined1)local_14;
  }
  local_c = param_2;
  local_10 = param_1 + param_3;
  for (local_8 = param_1; local_8 < local_10; local_8 = local_8 + 1) {
    puVar1 = local_114 + *local_8;
    *local_c = *puVar1;
    local_c = local_c + 1;
    if (puVar1 != local_114) {
      uVar2 = *puVar1;
      FUN__text1__008487d0(local_114 + 1,local_114,(int)puVar1 - (int)local_114,uVar2);
      local_114[0] = uVar2;
    }
  }
  return;
}

