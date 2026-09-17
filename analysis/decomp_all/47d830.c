
void FUN__text__0047d830(int param_1)

{
  undefined2 uVar1;
  int iVar2;
  uint uVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar4 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = param_1 + 0x2f4;
  *(undefined1 *)(param_1 + 0x4e4) = 0;
  uVar1 = (undefined2)((uint)local_c >> 0x10);
  if (*(short *)(param_1 + 0x312) == *(short *)(param_1 + 0x314)) {
    uVar3 = (uint)*(short *)(param_1 + 0x30c);
    if ((uVar3 != *(byte *)(param_1 + 0x314 + *(short *)(param_1 + 0x312) * 2)) ||
       (uVar3 = (uint)*(short *)(param_1 + 0x30e),
       uVar3 != *(byte *)(param_1 + 0x315 + *(short *)(param_1 + 0x312) * 2))) {
      FUN__text__0047d190(param_1,CONCAT22(uVar1,*(undefined2 *)(param_1 + 0x30c)),
                          CONCAT22((short)(uVar3 >> 0x10),*(undefined2 *)(param_1 + 0x30e)));
    }
  }
  else {
    FUN__text__0047d190(param_1,CONCAT22(uVar1,(ushort)*(byte *)(param_1 + 0x316 +
                                                                *(short *)(param_1 + 0x312) * 2)),
                        CONCAT22(uVar1,(ushort)*(byte *)(param_1 + 0x317 +
                                                        *(short *)(param_1 + 0x312) * 2)));
    *(short *)(local_c + 0x1e) = *(short *)(local_c + 0x1e) + 1;
  }
  local_8 = 0x47d923;
  FUN__text__0056ce80();
  return;
}

