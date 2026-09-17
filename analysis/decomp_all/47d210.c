
void FUN__text__0047d210(int param_1,int param_2)

{
  uint uVar1;
  undefined2 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  short local_1c;
  short local_18;
  short local_14;
  short local_10;
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_68;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if ((param_2 != 0) && ('\n' < *(char *)(param_1 + 0x4e4))) {
    FUN__text__00437d90(param_1,0);
    goto LAB__text__0047d558;
  }
  if (param_2 == 0) {
    local_c = param_1 + 0x2f4;
  }
  else {
    local_c = param_1 + 0x3e0;
  }
  local_10 = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                          (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_14 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  uVar1 = (int)((int)*(short *)(param_1 + 0x4d0) +
               ((int)*(short *)(param_1 + 0x4d0) >> 0x1f & 0x1fU)) >> 5;
  local_18 = (short)uVar1;
  local_1c = (short)((int)((int)*(short *)(param_1 + 0x4d2) +
                          ((int)*(short *)(param_1 + 0x4d2) >> 0x1f & 0xfU)) >> 4);
  if ((local_10 == local_18) && (local_14 == local_1c)) goto LAB__text__0047d558;
  uVar2 = (undefined2)((uint)*(int *)(param_1 + 600) >> 0x10);
  iVar3 = FUN__text__00438ad0(CONCAT22(uVar2,local_10),
                              CONCAT22((short)((uint)local_c >> 0x10),local_14),uVar1 & 0xffff,
                              CONCAT22(uVar2,local_1c),local_c,
                              *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),param_2);
  if (iVar3 == 0) {
    if ((param_2 != 0) ||
       (((iVar3 = FUN__text__0043bfa0((int)local_18,(int)local_1c,
                                      *(undefined1 *)(*(int *)(param_1 + 600) + 0x30)), iVar3 != 0
         && (local_24 = ((int)local_18 - (int)local_10) * ((int)local_18 - (int)local_10) +
                        ((int)local_1c - (int)local_14) * ((int)local_1c - (int)local_14),
            local_24 < 100)) ||
        (uVar2 = (undefined2)((uint)*(int *)(param_1 + 600) >> 0x10),
        local_20 = FUN__text__0044ea80(CONCAT22(uVar2,local_10),local_14,local_18,
                                       CONCAT22(uVar2,local_1c),local_c,
                                       *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),0),
        local_20 == 2)))) {
      iVar3 = FUN__text__0043bfa0((int)local_18,(int)local_1c,
                                  *(undefined1 *)(*(int *)(param_1 + 600) + 0x30));
      if (iVar3 == 0) {
        uVar2 = (undefined2)((uint)*(int *)(param_1 + 600) >> 0x10);
        iVar3 = FUN__text__00438d00(CONCAT22(uVar2,local_10),local_14,local_18,
                                    CONCAT22(uVar2,local_1c),local_c,
                                    *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),0);
        if (iVar3 != 0) goto LAB__text__0047d526;
        iVar3 = FUN__text__0043c0c0((int)local_10,(int)local_14);
        if (1 < iVar3) {
          FUN__text__00470840(param_1);
          goto LAB__text__0047d558;
        }
      }
      iVar3 = FUN__text__00437d10(param_1);
      if (iVar3 != 0) goto LAB__text__0047d558;
      FUN__text__00437d90(param_1,param_2);
      uVar2 = (undefined2)((uint)*(int *)(param_1 + 600) >> 0x10);
      local_20 = FUN__text__00437e40(CONCAT22(uVar2,local_10),local_14,local_18,
                                     CONCAT22(uVar2,local_1c),local_c,
                                     *(undefined1 *)(*(int *)(param_1 + 600) + 0x30),param_2);
    }
    local_28 = local_20;
    if ((local_20 == -1) || (local_20 != 1)) goto LAB__text__0047d558;
  }
LAB__text__0047d526:
  *(undefined1 *)(local_c + 0x1c) = (undefined1)local_10;
  *(undefined1 *)(local_c + 0x1d) = (undefined1)local_14;
LAB__text__0047d558:
  local_8 = 0x47d565;
  FUN__text__0056ce80();
  return;
}

