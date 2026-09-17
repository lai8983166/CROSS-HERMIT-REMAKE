
void __fastcall FUN__text__00492f40(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = 0;
  do {
    local_8 = param_1;
    if (local_c == 0x200) {
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlDamage.cpp",
                                  DAT_00619264 + 9,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
LAB__text__00493002:
      local_8 = 0x49300f;
      FUN__text__0056ce80();
      return;
    }
    if ((*(byte *)(param_1 + 0x2b6f0 + local_c * 8) & 0x80) == 0) {
      FUN__text__00492f00(param_1 + 0x2b6f0 + local_c * 8);
      *(byte *)(local_8 + 0x2b6f0 + local_c * 8) = *(byte *)(local_8 + 0x2b6f0 + local_c * 8) | 0x80
      ;
      goto LAB__text__00493002;
    }
    local_c = local_c + 1;
  } while( true );
}

