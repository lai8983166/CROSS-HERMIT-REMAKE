
void __thiscall FUN__text__004391c0(int param_1,int param_2,undefined4 param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  short local_1c;
  short local_18;
  ushort local_14;
  ushort local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  for (local_c = 0; local_c != *(short *)(param_2 + 0x20); local_c = local_c + 1) {
    local_10 = (ushort)*(byte *)(param_2 + 0x22 + local_c * 2);
    local_14 = (ushort)*(byte *)(param_2 + 0x23 + local_c * 2);
    local_18 = local_10 * 0x20 - *(short *)(*(int *)(local_8 + 0xb0) + 0x265a6);
    local_1c = (local_14 * 0x10 - *(short *)(*(int *)(local_8 + 0xb0) + 0x265a8)) + 0x1e;
    FUN__text__00410310(local_18 + 4,local_1c + 2,0x18,0xc,900,param_3,1);
  }
  local_8 = 0x43929e;
  FUN__text__0056ce80();
  return;
}

