
void FUN__text__0047cc90(int param_1)

{
  code *pcVar1;
  undefined1 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_68 [16];
  char local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  undefined1 local_14;
  undefined3 uStack_13;
  int local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_68;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(short *)(param_1 + 0x4fa) != -1) {
    if ((0xf9 < *(short *)(param_1 + 0x4fa)) &&
       (iVar3 = FUN__text__00424f80("wk->cdmg_uw < (250)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e68 + 8,0), iVar3 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_c = FUN__text__0047a8e0(param_1);
    local_28 = *(char *)(local_c + 0x1e);
    if (local_28 == '\0') {
      local_10 = local_8 + 0x80aec + *(short *)(param_1 + 0x4fa) * 0x520;
      iVar3 = FUN__text__00469ad0(local_10);
      if ((((iVar3 == 0) || (*(char *)(local_c + 0x1c) != '\0')) &&
          (iVar3 = FUN__text__0046ae20(param_1,local_10), iVar3 != 0)) &&
         (iVar3 = FUN__text__00469480(local_10), iVar3 != 0)) {
        iVar3 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
        local_18 = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0x1fU)) >> 5);
        iVar3 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
        local_1c = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0xfU)) >> 4);
        iVar3 = (int)(short)((uint)*(undefined4 *)(local_10 + 0x2ec) >> 0x10);
        local_20 = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0x1fU)) >> 5);
        iVar3 = (int)(short)((uint)*(undefined4 *)(local_10 + 0x2f0) >> 0x10);
        local_24 = (short)((int)(iVar3 + (iVar3 >> 0x1f & 0xfU)) >> 4);
        uVar2 = FUN__text__004ddbb0(param_1);
        _local_14 = CONCAT31(uStack_13,uVar2);
        iVar3 = FUN__text__0043c1d0((int)local_18,(int)local_1c,(int)local_20,(int)local_24,uVar2);
        if (iVar3 != 0) goto LAB__text__0047ce4e;
      }
    }
    FUN__text__00492e60(param_1 + 0x4fa);
  }
LAB__text__0047ce4e:
  local_8 = 0x47ce5b;
  FUN__text__0056ce80();
  return;
}

