
void FUN__text__00440af0(short param_1,short param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  undefined4 local_1c;
  undefined1 local_18;
  undefined3 uStack_17;
  int local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar2 = local_68;
  for (iVar1 = 0x19; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_24 = (int)param_1;
  local_c = __ftol();
  local_28 = (int)param_2;
  local_10 = __ftol();
  if (*(short *)(*(int *)(local_8 + 0x2659c) + 4) <= local_c) {
    local_c = *(short *)(*(int *)(local_8 + 0x2659c) + 4) + -1;
  }
  if (*(short *)(*(int *)(local_8 + 0x2659c) + 6) <= local_10) {
    local_10 = *(short *)(*(int *)(local_8 + 0x2659c) + 6) + -1;
  }
  local_14 = (int)local_10 * (int)*(short *)(*(int *)(local_8 + 0x2659c) + 4) + (int)local_c;
  local_1c = FUN__text__0043d1a0();
  local_20 = FUN__text__0043d200();
  _local_18 = CONCAT31(uStack_17,*(undefined1 *)(local_20 + local_14));
  local_8 = 0x440c04;
  FUN__text__0056ce80();
  return;
}

