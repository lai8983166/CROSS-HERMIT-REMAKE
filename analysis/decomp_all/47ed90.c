
void FUN__text__0047ed90(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_74 [16];
  char local_34;
  ushort local_30;
  ushort local_2c;
  short local_28;
  short local_24;
  int local_20;
  int local_1c;
  char *local_18;
  int local_14;
  char *local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_74;
  for (iVar2 = 0x1c; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_1 + 0x290;
  local_10 = (char *)(param_1 + 0x293);
  local_14 = FUN__text__0047a8e0(param_1);
  local_34 = *local_10;
  if (local_34 == '\0') {
    local_18 = (char *)FUN__text__0047a800(param_1);
    local_20 = (int)*local_18;
    local_1c = *(int *)(local_18 + 4);
    local_24 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                            (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
    local_28 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                            (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
    local_2c = (ushort)*(byte *)(local_1c + *(char *)(local_c + 0x19) * 0xc);
    local_30 = (ushort)*(byte *)(local_1c + 1 + *(char *)(local_c + 0x19) * 0xc);
    FUN__text__0043c0c0(local_2c,local_30);
    if (((*(char *)(local_c + 0x19) < '\0') || (local_20 <= *(char *)(local_c + 0x19))) &&
       (iVar2 = FUN__text__00424f80("(0<=ai->round_no) && (ai->round_no<cnt)",
                                    "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                    DAT_00618e7c + 0x24,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    iVar2 = FUN__text__0043c1d0((int)local_24,(int)local_28,(int)(short)local_2c,
                                (int)(short)local_30,3);
    if (iVar2 == 0) {
      FUN__text__0047d190(param_1,*(undefined1 *)(local_1c + *(char *)(local_c + 0x19) * 0xc),
                          *(undefined1 *)(local_1c + 1 + *(char *)(local_c + 0x19) * 0xc));
      FUN__text__00475270(param_1,4);
    }
    else if (*(int *)(local_1c + 4 + *(char *)(local_c + 0x19) * 0xc) == 0) {
      iVar2 = FUN__text__0047f090(param_1);
      if (iVar2 == 0) {
        FUN__text__00475270(param_1,4);
      }
      else {
        FUN__text__00475270(param_1,0xf);
      }
    }
    else {
      *(undefined4 *)(local_14 + 0x38) =
           *(undefined4 *)(local_1c + 4 + *(char *)(local_c + 0x19) * 0xc);
      FUN__text__00475270(param_1,0x1a);
    }
  }
  local_8 = 0x47efa9;
  FUN__text__0056ce80();
  return;
}

