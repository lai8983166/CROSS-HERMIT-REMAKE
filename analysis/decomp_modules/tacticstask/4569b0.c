
void __fastcall FUN__text__004569b0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_9c [16];
  int local_5c;
  int local_58;
  int local_54;
  int local_50;
  short local_4c [32];
  int local_c;
  int local_8;
  
  puVar2 = local_9c;
  for (iVar1 = 0x26; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *(int *)(param_1 + 0x60) + 0x2450;
  local_8 = param_1;
  _memset(local_4c,0xff,0x40);
  local_54 = 0;
  for (local_50 = 0; local_50 != 0x20; local_50 = local_50 + 1) {
    if (*(short *)(local_c + local_50 * 2) != -1) {
      local_4c[local_54] = *(short *)(local_c + local_50 * 2);
      local_54 = local_54 + 1;
    }
  }
  for (local_50 = 0; local_50 != local_54; local_50 = local_50 + 1) {
    local_58 = FUN__text__00467e00("E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                   DAT_0060cdc0 + 0x10);
    local_58 = local_58 % local_54;
    local_5c = FUN__text__00467e00("E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                   DAT_0060cdc0 + 0x11);
    local_5c = local_5c % local_54;
    FUN__text__0042b050(local_4c + local_58,local_4c + local_5c);
  }
  local_50 = 0;
  while ((local_50 != local_54 &&
         (iVar1 = FUN__text__00430980((int)local_4c[local_50],0), iVar1 == 0))) {
    local_50 = local_50 + 1;
  }
  local_8 = 0x456b14;
  FUN__text__0056ce80();
  return;
}

