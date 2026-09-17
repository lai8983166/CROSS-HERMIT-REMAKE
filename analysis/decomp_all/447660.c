
void __thiscall FUN__text__00447660(int param_1,undefined1 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  uint local_20;
  undefined4 local_1c;
  int local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_10 = 0x199;
  local_14 = 0x165;
  local_8 = param_1;
  for (local_c = 0; local_c != 0xc; local_c = local_c + 1) {
    local_18 = local_10 + *(int *)(&DAT_00605c78 + local_c * 4);
    local_1c = local_14;
    local_20 = (uint)(*(int *)(local_8 + 0x1bcc) == local_c);
    FUN__text__00447720(local_18,local_14,(int)*(char *)(local_8 + local_c + 0x1bd0),local_20,
                        (int)*(short *)(local_8 + 0x1bde),param_2);
  }
  local_8 = 0x44770d;
  FUN__text__0056ce80();
  return;
}

