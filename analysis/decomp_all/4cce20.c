
/* WARNING: Removing unreachable block (ram,0x004ccf20) */

void __thiscall FUN__text__004cce20(int param_1,int param_2)

{
  short sVar1;
  short sVar2;
  int iVar3;
  undefined2 uVar4;
  undefined4 *puVar5;
  undefined4 local_60 [16];
  undefined2 local_20;
  short local_1c [4];
  uint local_14;
  undefined1 local_10 [4];
  undefined1 local_c;
  int local_8;
  
  puVar5 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar5 = 0xcccccccc;
    puVar5 = puVar5 + 1;
  }
  local_8 = param_1;
  local_c = 0;
  local_1c[0] = 5;
  local_1c[1] = 5;
  local_1c[2] = 5;
  local_1c[3] = 5;
  if ((*(char *)(param_1 + 0x1cc) != -1) &&
     (*(short *)(*(int *)(param_1 + 0x38 + param_2 * 0x1c8) + 2) == 2)) {
    sVar1 = *(short *)(param_1 + 0x30 + param_2 * 0x1c8);
    sVar2 = local_1c[*(ushort *)(param_1 + 0x32 + param_2 * 0x1c8)];
    *(short *)(param_1 + 0x30 + param_2 * 0x1c8) = *(short *)(param_1 + 0x30 + param_2 * 0x1c8) + 1;
    if (sVar2 < sVar1) {
      *(short *)(param_1 + 0x32 + param_2 * 0x1c8) =
           *(short *)(param_1 + 0x32 + param_2 * 0x1c8) + 1;
      *(ushort *)(param_1 + 0x32 + param_2 * 0x1c8) =
           *(ushort *)(param_1 + 0x32 + param_2 * 0x1c8) & 3;
      *(undefined2 *)(param_1 + 0x30 + param_2 * 0x1c8) = 0;
    }
    local_20 = *(undefined2 *)(param_1 + 0x32 + param_2 * 0x1c8);
    iVar3 = (uint)*(ushort *)(param_1 + 0x32 + param_2 * 0x1c8) * 0x12 + 0x1a8;
    uVar4 = (undefined2)((uint)iVar3 >> 0x10);
    FUN__text__004d29e0(0x14,0,1,0x36,
                        CONCAT22(uVar4,*(undefined2 *)(param_1 + 0x34 + param_2 * 0x1c8)),
                        CONCAT22(uVar4,*(undefined2 *)(param_1 + 0x36 + param_2 * 0x1c8)),iVar3,0,
                        0x12,0x18,100,100,0xff,0x80,0x80,0x80);
  }
  iVar3 = FUN__text__004128f0(0x39,0);
  if ((iVar3 != 0) && (local_c = 1, DAT_007a49fc != 0)) {
    FUN__text__0041e500();
  }
  FUN__text__004ccb30(0,0,local_10,&local_14);
  if ((local_14 & 7) != 0) {
    local_c = 1;
  }
  local_8 = 0x4cd04b;
  FUN__text__0056ce80();
  return;
}

