
void FUN__text__0047da30(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  char local_18;
  char *local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00470a50(param_1);
  if ((iVar2 != 0) &&
     (iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e70 + 9,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = (short)((int)((int)*(short *)(param_1 + 0x4dc) +
                         ((int)*(short *)(param_1 + 0x4dc) >> 0x1f & 0x1fU)) >> 5);
  local_10 = (short)((int)((int)*(short *)(param_1 + 0x4de) +
                          ((int)*(short *)(param_1 + 0x4de) >> 0x1f & 0xfU)) >> 4);
  iVar2 = FUN__text__0043bfa0((int)local_c,(int)local_10,
                              *(undefined1 *)(*(int *)(param_1 + 600) + 0x30));
  if (iVar2 != 0) {
    iVar2 = FUN__text__0043c0c0((int)local_c,(int)local_10);
    if ((iVar2 == 0) || (iVar2 = FUN__text__004707b0(param_1), iVar2 == 0)) {
      local_14 = (char *)FUN__text__0047a8e0(param_1);
      if ((*(char *)(*(int *)(param_1 + 600) + 0x9f) == '\x01') &&
         (((local_18 = *(char *)(param_1 + 0x290), local_18 == '\x04' || (local_18 == '\x17')) &&
          (*local_14 == '\x01')))) {
        local_14[0x3c] =
             (char)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                         (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
        local_14[0x3d] =
             (char)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                         (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      }
    }
    else {
      FUN__text__00470840(param_1);
    }
  }
  local_8 = 0x47dbbe;
  FUN__text__0056ce80();
  return;
}

