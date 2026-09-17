
void __thiscall
FUN__text__00438f70(int param_1,ushort param_2,ushort param_3,int param_4,int param_5,
                   undefined4 param_6,undefined4 param_7,int param_8)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  ushort local_20;
  ushort local_1c;
  short local_18;
  ushort local_14;
  ushort local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined4 *)(param_1 + 0x14) = param_6;
  local_18 = 0;
  local_10 = param_2;
  local_14 = param_3;
  local_8 = param_1;
  do {
    local_10 = local_10 + *(short *)(&DAT_005ff984 + param_4 * 4);
    local_14 = local_14 + *(short *)(&DAT_005ff986 + param_4 * 4);
    if (((((short)local_10 < 0) || (*(int *)(local_8 + 0x48) <= (int)(short)local_10)) ||
        ((short)local_14 < 0)) ||
       ((*(int *)(local_8 + 0x4c) <= (int)(short)local_14 ||
        (local_c = FUN__text__004388e0(CONCAT22((short)local_14 >> 0xf,param_2),param_3,local_10,
                                       (int)(short)local_14,param_7), local_c == 0)))) break;
    local_18 = local_18 + 1;
    local_1c = local_10;
    local_20 = local_14;
  } while (local_18 < param_8);
  if (local_18 != 0) {
    *(ushort *)(param_5 + 0x18) = local_1c & 0xff;
    *(ushort *)(param_5 + 0x1a) = local_20 & 0xff;
    *(undefined1 *)(param_5 + 0x1c) = (undefined1)param_2;
    *(undefined1 *)(param_5 + 0x1d) = (undefined1)param_3;
    *(undefined2 *)(param_5 + 0x1e) = 0;
    *(undefined2 *)(param_5 + 0x20) = 1;
    *(undefined1 *)(param_5 + 0x22) = (undefined1)local_1c;
    *(undefined1 *)(param_5 + 0x23) = (undefined1)local_20;
  }
  local_8 = 0x4390d4;
  FUN__text__0056ce80();
  return;
}

