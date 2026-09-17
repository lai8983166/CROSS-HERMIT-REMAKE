
void FUN__text__00430400(int param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  short *local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = &DAT_007f4488;
  iVar1 = FUN__text__00469480(param_1);
  if (iVar1 != 0) {
    local_18 = (int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                    (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5;
    local_1c = (int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                    (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4;
    local_14 = FUN__text__0043bb90(local_18,local_1c);
    if ((-1 < local_14) && (local_14 < 0x20)) {
      FUN__text__004305c0(param_1,local_14);
    }
    if ((*(char *)(param_1 + 0x4e7) != *(char *)(param_1 + 0x4e9)) ||
       (*(char *)(param_1 + 0x4e8) != *(char *)(param_1 + 0x4ea))) {
      local_10 = FUN__text__00496e70(local_18,local_1c);
      if ((local_10 != 0) &&
         (iVar1 = FUN__text__00496f10(local_10,*(undefined1 *)(*(int *)(param_1 + 600) + 0xa4)),
         iVar1 != 0)) {
        if ((uint)*(byte *)(param_1 + 0x4e6) == (int)(char)local_10) goto LAB__text__004305aa;
        local_20 = (int)*local_c;
        FUN__text__00497530((int)*(short *)(param_1 + 2));
        iVar1 = FUN__text__004551c0(1,local_10);
        if (iVar1 != 0) {
          FUN__text__004549d0(0,1,local_10,0,0,1,1);
        }
      }
      *(undefined1 *)(param_1 + 0x4e5) = *(undefined1 *)(param_1 + 0x4e6);
      *(char *)(param_1 + 0x4e6) = (char)local_10;
    }
  }
LAB__text__004305aa:
  local_8 = 0x4305b7;
  FUN__text__0056ce80();
  return;
}

