
void FUN__text__004d58e0(int *param_1,short param_2)

{
  undefined4 *puVar1;
  int iVar2;
  int *piVar3;
  undefined4 *puVar4;
  undefined4 local_16c [16];
  undefined1 local_12c [32];
  short local_10c;
  int local_108 [4];
  undefined1 local_f8;
  undefined4 local_f4;
  undefined4 auStack_f0 [56];
  undefined *local_10;
  undefined *local_c;
  undefined4 local_8;
  
  puVar1 = local_16c;
  for (iVar2 = 0x5a; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar1 = 0xcccccccc;
    puVar1 = puVar1 + 1;
  }
  local_c = &DAT_007e17e8 + param_2 * 0x4a0;
  local_10 = &DAT_007cf34c + param_2 * 0x124;
  local_108[0] = 0;
  for (local_10c = 0; local_10c < 7; local_10c = local_10c + 1) {
    puVar1 = (undefined4 *)
             FUN__text__004d56a0(local_12c,
                                 CONCAT22((short)((uint)*(undefined4 *)
                                                         (local_c + local_10c * 8 + 0x10) >> 0x10),
                                          (ushort)(byte)local_c[local_10c * 8 + 0xc]),
                                 *(undefined4 *)(local_c + local_10c * 8 + 0x10));
    puVar4 = auStack_f0 + local_10c * 8;
    for (iVar2 = 8; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar1;
      puVar1 = puVar1 + 1;
      puVar4 = puVar4 + 1;
    }
    local_108[0] = local_108[0] + *(int *)(local_c + local_10c * 8 + 0x10);
  }
  local_108[1] = FUN__text__004d5850(local_c + 0xb0);
  local_108[2] = local_108[0] + local_108[1];
  local_108[3] = (int)PTR_DAT_006253c4 - local_108[2];
  if (local_108[3] < 0) {
    local_108[3] = 0;
  }
  local_f8 = FUN__text__004d5590(local_108[2]);
  local_f4 = *(undefined4 *)(local_10 + 0x11c);
  piVar3 = local_108;
  for (iVar2 = 0x3e; iVar2 != 0; iVar2 = iVar2 + -1) {
    *param_1 = *piVar3;
    piVar3 = piVar3 + 1;
    param_1 = param_1 + 1;
  }
  local_8 = 0x4d5a58;
  FUN__text__0056ce80();
  return;
}

