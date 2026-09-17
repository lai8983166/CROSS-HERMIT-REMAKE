
/* WARNING: Removing unreachable block (ram,0x0047e4bb) */
/* WARNING: Removing unreachable block (ram,0x0047e4d8) */
/* WARNING: Removing unreachable block (ram,0x0047e4e6) */
/* WARNING: Removing unreachable block (ram,0x0047e563) */
/* WARNING: Removing unreachable block (ram,0x0047e4cf) */
/* WARNING: Removing unreachable block (ram,0x0047e572) */

void FUN__text__0047e460(undefined4 param_1,short param_2,short param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  char local_1c;
  int local_18;
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00468d80(param_1);
  if ((iVar2 == 0) &&
     (iVar2 = FUN__text__00424f80("IsUwHuman(wk)",
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e74 + 7,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (int *)(local_8 + 0xdc8ec);
  for (local_10 = 0; local_10 != *local_c; local_10 = local_10 + 1) {
    iVar2 = FUN__text__0046abc0(param_1,local_c[local_10 + 1]);
    if ((iVar2 != 0) || (iVar2 = FUN__text__0046ad60(param_1,local_c[local_10 + 1]), iVar2 != 0)) {
      local_14 = (int)((*(int *)(local_c[local_10 + 1] + 0x2ec) >> 0x10) +
                      (*(int *)(local_c[local_10 + 1] + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
      local_18 = (int)((*(int *)(local_c[local_10 + 1] + 0x2f0) >> 0x10) +
                      (*(int *)(local_c[local_10 + 1] + 0x2f0) >> 0x1f & 0xfU)) >> 4;
      local_1c = FUN__text__004ddbb0(local_c[local_10 + 1]);
      iVar2 = FUN__text__0043c1d0(local_14,local_18,(int)param_2,(int)param_3,(int)local_1c);
      if (iVar2 != 0) break;
    }
  }
  local_8 = 0x47e676;
  FUN__text__0056ce80();
  return;
}

