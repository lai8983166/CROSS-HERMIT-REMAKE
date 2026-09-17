
void FUN_005708b0(int param_1)

{
  byte bVar1;
  code *pcVar2;
  byte bVar3;
  int iVar4;
  uint local_5c;
  int local_58;
  int local_50;
  byte local_4c [20];
  undefined1 local_38 [52];
  
  local_50 = 0;
  while( true ) {
    if (*(int *)(param_1 + 0x10) < 0x10) {
      local_58 = *(int *)(param_1 + 0x10);
    }
    else {
      local_58 = 0x10;
    }
    if (local_58 <= local_50) break;
    bVar1 = *(byte *)(param_1 + local_50 + 0x20);
    if (DAT_00764370 < 2) {
      local_5c = *(ushort *)(PTR_DAT_00764164 + (uint)bVar1 * 2) & 0x157;
    }
    else {
      local_5c = FUN_0057bb50(bVar1,0x157);
    }
    bVar3 = bVar1;
    if (local_5c == 0) {
      bVar3 = 0x20;
    }
    local_4c[local_50] = bVar3;
    FUN_0056d810(local_38 + local_50 * 3,"%.2X ",bVar1);
    local_50 = local_50 + 1;
  }
  local_4c[local_50] = 0;
  iVar4 = FUN_00573780(0,0,0,0," Data: <%s> %s\n",local_4c,local_38);
  if (iVar4 == 1) {
    pcVar2 = (code *)swi(3);
    (*pcVar2)();
    return;
  }
  return;
}

