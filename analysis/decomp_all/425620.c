
void __thiscall
FUN__text__00425620(short *param_1,undefined4 param_2,int param_3,undefined4 param_4,int param_5,
                   undefined2 param_6)

{
  undefined2 uVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_58 [16];
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  short *local_8;
  
  puVar4 = local_58;
  for (iVar3 = 0x15; uVar2 = local_14, iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_14._0_2_ = (undefined2)param_2;
  uVar1 = (undefined2)local_14;
  local_14 = uVar2;
  local_8 = param_1;
  if ((char)param_1[3] == '\0') {
    local_10 = (int)param_1[2];
    for (local_c = 0; local_c != *local_8; local_c = local_c + 1) {
      local_14 = param_2;
      local_18 = param_3 + param_5 * local_c;
      FUN__text__004096d0(CONCAT22((short)((uint)local_18 >> 0x10),uVar1),
                          CONCAT22((short)((uint)(param_5 * local_c) >> 0x10),(undefined2)local_18),
                          param_6,0xffffffff);
      local_10 = local_10 + 1;
      if (*local_8 <= local_10) {
        local_10 = 0;
      }
    }
  }
  else if (param_1[1] != 0) {
    local_10 = (param_1[1] + -1) % (int)*param_1;
    for (local_c = 0; local_c != *local_8; local_c = local_c + 1) {
      local_14 = param_2;
      local_18 = param_3 + param_5 * local_c;
      FUN__text__004096d0(CONCAT22((short)((uint)local_18 >> 0x10),uVar1),
                          CONCAT22((short)((uint)(param_5 * local_c) >> 0x10),(undefined2)local_18),
                          param_6,0xffffffff);
      local_10 = local_10 + -1;
      if (local_10 < 0) {
        local_10 = *local_8 + -1;
      }
    }
  }
  local_8 = (short *)0x42577a;
  FUN__text__0056ce80();
  return;
}

