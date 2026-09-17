
void __thiscall FUN__text__00464f80(int param_1,int param_2,int param_3)

{
  ushort uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  byte *local_18;
  ushort local_14;
  undefined2 uStack_12;
  uint local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (*(short *)(param_1 + 0x48) != -1) {
    *(undefined2 *)(param_2 + 0xc) = (undefined2)param_3;
    local_18 = (byte *)(*(int *)(param_1 + 0x4c) + param_3 * 2);
    uVar1 = *(ushort *)(*(int *)(param_1 + 0x50) + (uint)*local_18 * 2);
    _local_14 = CONCAT22(uStack_12,uVar1);
    local_c = (int)(uVar1 & 0xff00) >> 8;
    local_10 = uVar1 & 0xff;
    local_8 = param_1;
    FUN__text__00409ff0(param_2,local_c,local_10,local_18[1] & 3);
  }
  local_8 = 0x46502e;
  FUN__text__0056ce80();
  return;
}

