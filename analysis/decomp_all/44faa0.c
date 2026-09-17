
void __thiscall FUN__text__0044faa0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  short local_20;
  short local_1c;
  int local_18;
  byte *local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_1 + 0xac;
  local_10 = *(int *)(param_1 + 0xb4 + param_2 * 4);
  local_8 = param_1;
  for (local_18 = 0; local_18 != *(int *)(local_10 + 0x14); local_18 = local_18 + 1) {
    local_14 = (byte *)FUN__text__0044e650(param_2,local_18);
    local_1c = (ushort)*local_14 * 0x20 - *(short *)(*(int *)(local_8 + 0xa8) + 0x265a6);
    local_20 = ((ushort)local_14[1] * 0x10 - *(short *)(*(int *)(local_8 + 0xa8) + 0x265a8)) + 0x1e;
    FUN__text__00410310((int)local_1c,(int)local_20,0x20,0x10,0xeff,0x8000ff00,1);
  }
  local_8 = 0x44fb9d;
  FUN__text__0056ce80();
  return;
}

