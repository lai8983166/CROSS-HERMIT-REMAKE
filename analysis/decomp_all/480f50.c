
void __fastcall FUN__text__00480f50(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  undefined1 *local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (undefined1 *)(param_1 + 0x108f48);
  local_8 = param_1;
  _memset(local_c,0,0x2a);
  *local_c = 0;
  for (local_10 = 0; local_10 != 0x14; local_10 = local_10 + 1) {
    *(undefined2 *)(local_c + local_10 * 2 + 2) = 0xffff;
  }
  local_8 = 0x480fc2;
  FUN__text__0056ce80();
  return;
}

