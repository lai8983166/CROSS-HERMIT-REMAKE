
void FUN__text__0047dbd0(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_64 [16];
  int local_24;
  int local_20;
  int local_1c;
  short local_18;
  short local_14;
  short local_10;
  short local_c;
  undefined4 local_8;
  
  puVar2 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(short *)(param_1 + 0x3fe) == *(short *)(param_1 + 0x400)) {
    local_14 = (short)((int)((int)*(short *)(param_1 + 0x4d0) +
                            ((int)*(short *)(param_1 + 0x4d0) >> 0x1f & 0x1fU)) >> 5);
    local_18 = (short)((int)((int)*(short *)(param_1 + 0x4d2) +
                            ((int)*(short *)(param_1 + 0x4d2) >> 0x1f & 0xfU)) >> 4);
    if (*(short *)(param_1 + 0x312) != *(short *)(param_1 + 0x314)) {
      local_c = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                             (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
      local_10 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                              (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
      local_24 = ((int)local_14 - (int)local_c) * ((int)local_14 - (int)local_c) +
                 ((int)local_18 - (int)local_10) * ((int)local_18 - (int)local_10);
      if (local_24 < 9) goto LAB__text__0047dea2;
    }
  }
  local_c = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                         (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
  local_10 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                          (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
  local_14 = (short)((int)((int)*(short *)(param_1 + 0x4dc) +
                          ((int)*(short *)(param_1 + 0x4dc) >> 0x1f & 0x1fU)) >> 5);
  local_18 = (short)((int)((int)*(short *)(param_1 + 0x4de) +
                          ((int)*(short *)(param_1 + 0x4de) >> 0x1f & 0xfU)) >> 4);
  if ((local_c == local_14) && (local_10 == local_18)) {
    local_14 = (short)((int)((int)*(short *)(param_1 + 0x4d8) +
                            ((int)*(short *)(param_1 + 0x4d8) >> 0x1f & 0x1fU)) >> 5);
    local_18 = (short)((int)((int)*(short *)(param_1 + 0x4da) +
                            ((int)*(short *)(param_1 + 0x4da) >> 0x1f & 0xfU)) >> 4);
    if ((local_c == local_14) &&
       ((local_10 == local_18 && (*(short *)(param_1 + 0x3fe) == *(short *)(param_1 + 0x400))))) {
      local_1c = FUN__text__0056db00((int)*(short *)(param_1 + 0x4dc) -
                                     (*(int *)(param_1 + 0x2ec) >> 0x10));
      local_20 = FUN__text__0056db00((int)*(short *)(param_1 + 0x4de) -
                                     (*(int *)(param_1 + 0x2f0) >> 0x10));
      if ((local_1c < 3) && (local_20 < 3)) {
        local_14 = (short)((int)((int)*(short *)(param_1 + 0x4d0) +
                                ((int)*(short *)(param_1 + 0x4d0) >> 0x1f & 0x1fU)) >> 5);
        local_18 = (short)((int)((int)*(short *)(param_1 + 0x4d2) +
                                ((int)*(short *)(param_1 + 0x4d2) >> 0x1f & 0xfU)) >> 4);
        if (((local_c == local_14) && (local_10 == local_18)) &&
           (iVar1 = FUN__text__0043c0c0((int)local_14,(int)local_18), 1 < iVar1)) {
          FUN__text__00470840(param_1);
        }
      }
    }
  }
LAB__text__0047dea2:
  local_8 = 0x47deaf;
  FUN__text__0056ce80();
  return;
}

