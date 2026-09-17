
void __fastcall FUN__text__0048cd90(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; local_8 = param_1, iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  while( true ) {
    local_c = FUN__text__00427de0();
    if (local_c == 0) {
      local_8 = 0x48ce4f;
      FUN__text__0056ce80();
      return;
    }
    local_10 = *(int *)(local_c + 8);
    local_14 = local_8 + 0x80aec + (uint)*(byte *)(local_10 + 1) * 0x520;
    iVar2 = FUN__text__00468d10(local_14);
    if ((iVar2 == 0) &&
       (iVar2 = FUN__text__00424f80("IsUwUsed(wk)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCommand.cpp",
                                    DAT_00618f84 + 0x10,0), iVar2 != 0)) break;
    FUN__text__0048dcd0(local_14,local_c);
  }
  pcVar1 = (code *)swi(3);
  (*pcVar1)();
  return;
}

