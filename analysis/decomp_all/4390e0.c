
void __thiscall FUN__text__004390e0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (*(int *)(param_2 + 0x14) != 0) {
    local_10 = param_2;
    iVar1 = local_10;
    local_8 = param_1;
    do {
      local_10 = iVar1;
      local_14 = *(short *)(local_10 + 2) * 0x20 -
                 (int)*(short *)(*(int *)(local_8 + 0xb0) + 0x265a6);
      iVar1 = *(short *)(local_10 + 4) * 0x10 - (int)*(short *)(*(int *)(local_8 + 0xb0) + 0x265a8);
      local_18 = iVar1 + 0x1e;
      FUN__text__00410310(local_14 + 4,iVar1 + 0x20,0x18,0xc,0xeff,0x800000ff,1);
      local_c = *(int *)(local_10 + 0x14);
      iVar1 = local_c;
    } while (*(int *)(local_c + 0x14) != 0);
  }
  local_8 = 0x4391ba;
  FUN__text__0056ce80();
  return;
}

