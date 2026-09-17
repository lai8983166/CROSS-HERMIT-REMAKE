
void __thiscall FUN__text__004941a0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x116098 + param_2 * 0x2c;
  local_8 = param_1;
LAB__text__004941d0:
  FUN__text__00427b70(local_c + 0x10);
  do {
    do {
      local_10 = FUN__text__00427bf0();
      if (local_10 == 0) {
        local_8 = 0x4942aa;
        FUN__text__0056ce80();
        return;
      }
      local_14 = *(int *)(local_10 + 8);
      if ((local_14 == 0) &&
         (iVar2 = FUN__text__00424f80("wk!=0",
                                      "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlKeySelect.cpp",
                                      DAT_00619298 + 0xe,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    } while (local_14 == 0);
    for (local_18 = 0; local_18 != *(int *)(local_8 + 0x108b50); local_18 = local_18 + 1) {
      if (local_14 == *(int *)(local_8 + 0x108b60 + local_18 * 4)) {
        FUN__text__00427c90(local_10);
        FUN__text__00427e70(local_10);
        goto LAB__text__004941d0;
      }
    }
  } while( true );
}

