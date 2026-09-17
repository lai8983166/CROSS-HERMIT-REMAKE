
void FUN__text__0043ab10(void)

{
  code *pcVar1;
  short sVar2;
  int iVar3;
  uint uVar4;
  undefined4 *puVar5;
  undefined4 local_8c [16];
  void *local_4c;
  undefined4 local_48;
  undefined4 local_44;
  void *local_40;
  undefined4 local_3c;
  undefined2 local_38;
  undefined4 *local_34;
  undefined4 *local_30;
  char *local_2c;
  short local_28;
  short local_24;
  short local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  void *local_c;
  int local_8;
  
  puVar5 = local_8c;
  for (iVar3 = 0x22; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_10 = 0x41;
  local_14 = 0x41;
  local_40 = (void *)FUN__text__00428a40(0x2102);
  local_c = local_40;
  if ((local_40 == (void *)0x0) &&
     (iVar3 = FUN__text__00424f80("mem!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9dc + 0xd,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_44 = FUN__text__00428a40((int)local_10 * (int)local_14 * 6);
  *(undefined4 *)(local_8 + 0x263b8) = local_44;
  if ((*(int *)(local_8 + 0x263b8) == 0) &&
     (iVar3 = FUN__text__00424f80("AppearTbl!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9dc + 0x10,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_48 = FUN__text__00428a40((int)local_10 * (int)local_14 * 2);
  *(undefined4 *)(local_8 + 0x263bc) = local_48;
  if ((*(int *)(local_8 + 0x263bc) == 0) &&
     (iVar3 = FUN__text__00424f80("AppearTblSort!=0",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ff9dc + 0x13,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  _memset(*(void **)(local_8 + 0x263bc),0,local_10 * 2 * (int)local_14);
  _memset(local_c,0,local_10 * 2 * (int)local_14);
  FUN__text__0043b110(local_c,(int)local_10,(int)local_14,(int)local_10 / 2,(int)local_14 / 2,
                      local_10 + -1);
  for (local_1c = 0; local_1c != local_14; local_1c = local_1c + 1) {
    for (local_18 = 0; local_18 != local_10; local_18 = local_18 + 1) {
      *(char *)(*(int *)(local_8 + 0x263b8) + ((int)local_1c * (int)local_10 + (int)local_18) * 6) =
           (char)local_18 - (char)((int)local_10 / 2);
      *(char *)(*(int *)(local_8 + 0x263b8) + 1 +
               ((int)local_1c * (int)local_10 + (int)local_18) * 6) =
           (char)local_1c - (char)((int)local_14 / 2);
      *(short *)(*(int *)(local_8 + 0x263b8) + 2 +
                ((int)local_1c * (int)local_10 + (int)local_18) * 6) =
           (local_10 + -1) -
           *(short *)((int)local_c + ((int)local_1c * (int)local_10 + (int)local_18) * 2);
      *(short *)(*(int *)(local_8 + 0x263b8) + 4 +
                ((int)local_1c * (int)local_10 + (int)local_18) * 6) =
           (local_10 + -1) -
           *(short *)((int)local_c + ((int)local_1c * (int)local_10 + (int)local_18) * 2);
    }
  }
  for (local_24 = 0; (int)local_24 != (int)local_10 * (int)local_14; local_24 = local_24 + 1) {
    local_28 = local_10 * local_14;
    local_20 = 0;
    while (local_28 = local_28 + -1, -1 < local_28) {
      if ((uint)*(ushort *)(*(int *)(local_8 + 0x263b8) + 2 + local_28 * 6) == (int)local_24) {
        *(short *)(*(int *)(local_8 + 0x263b8) + 4 + local_28 * 6) =
             *(short *)(*(int *)(local_8 + 0x263b8) + 4 + local_28 * 6) * 0x100 + local_20;
        local_20 = local_20 + 1;
      }
    }
  }
  for (local_28 = 0; (int)local_28 != (int)local_10 * (int)local_14; local_28 = local_28 + 1) {
    local_2c = (char *)(*(int *)(local_8 + 0x263b8) + local_28 * 6);
    uVar4 = (int)local_2c[1] & 0x80000001;
    if ((int)uVar4 < 0) {
      uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
    }
    if (uVar4 == 0) {
      uVar4 = (int)*local_2c & 0x80000001;
      if ((int)uVar4 < 0) {
        uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
      }
      if (((uVar4 != 0) && (iVar3 = FUN__text__0056db00((int)*local_2c), iVar3 < 7)) &&
         (iVar3 = FUN__text__0056db00((int)local_2c[1]), iVar3 < 7)) {
        *(short *)(local_2c + 4) = *(short *)(local_2c + 4) + -0x8000;
      }
    }
    else {
      uVar4 = (int)*local_2c & 0x80000001;
      if ((int)uVar4 < 0) {
        uVar4 = (uVar4 - 1 | 0xfffffffe) + 1;
      }
      if (((uVar4 == 0) && (iVar3 = FUN__text__0056db00((int)*local_2c), iVar3 < 7)) &&
         (iVar3 = FUN__text__0056db00((int)local_2c[1]), iVar3 < 7)) {
        *(short *)(local_2c + 4) = *(short *)(local_2c + 4) + -0x8000;
      }
    }
  }
  for (local_1c = 0; sVar2 = local_1c, (int)local_1c != (int)local_10 * (int)local_14 + -1;
      local_1c = local_1c + 1) {
    while (local_18 = sVar2 + 1, (int)local_18 != (int)local_10 * (int)local_14) {
      local_30 = (undefined4 *)(*(int *)(local_8 + 0x263b8) + local_1c * 6);
      local_34 = (undefined4 *)(*(int *)(local_8 + 0x263b8) + local_18 * 6);
      sVar2 = local_18;
      if (*(ushort *)(local_34 + 1) < *(ushort *)(local_30 + 1)) {
        local_3c = *local_30;
        local_38 = *(undefined2 *)(local_30 + 1);
        *local_30 = *local_34;
        *(undefined2 *)(local_30 + 1) = *(undefined2 *)(local_34 + 1);
        *local_34 = local_3c;
        *(undefined2 *)(local_34 + 1) = local_38;
      }
    }
  }
  for (local_28 = 0; (int)local_28 != (int)local_10 * (int)local_14; local_28 = local_28 + 1) {
    *(short *)(*(int *)(local_8 + 0x263b8) + 4 + local_28 * 6) = local_28;
  }
  *(short *)(local_8 + 0x263c0) = local_10;
  *(short *)(local_8 + 0x263c2) = local_14;
  local_4c = local_c;
  FUN__text__00428ad0(local_c);
  local_8 = 0x43b0fd;
  FUN__text__0056ce80();
  return;
}

