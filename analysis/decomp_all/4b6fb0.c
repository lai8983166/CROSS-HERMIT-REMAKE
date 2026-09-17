
ushort __thiscall FUN__text__004b6fb0(int param_1,short param_2,uint param_3)

{
  ushort uVar1;
  int iVar2;
  ushort uVar3;
  undefined4 *puVar4;
  undefined4 local_54 [20];
  
  puVar4 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  uVar3 = 0;
  uVar1 = 0;
  while( true ) {
    if ((int)*(short *)(param_1 + 0x594) <= (int)(uint)uVar1) {
      return uVar3;
    }
    if (param_2 == 0) {
      uVar3 = (ushort)((int)(((param_3 & 0xffff) - (uVar1 + 1)) + (int)*(short *)(param_1 + 0x594))
                      % (int)*(short *)(param_1 + 0x594));
    }
    else {
      uVar3 = (ushort)((longlong)(ulonglong)((param_3 & 0xffff) + 1 + (uint)uVar1) %
                      (longlong)(int)*(short *)(param_1 + 0x594));
    }
    if (*(short *)(param_1 + 0x596 + (uint)uVar3 * 2) != -1) break;
    uVar1 = uVar1 + 1;
  }
  return uVar3;
}

