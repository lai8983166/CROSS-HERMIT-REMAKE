
void FUN__text__00470840(int param_1)

{
  uint uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  short local_18 [2];
  short local_14 [2];
  undefined2 local_10;
  undefined2 local_c;
  undefined4 local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (undefined2)
            ((int)((int)*(short *)(param_1 + 0x4cc) +
                  ((int)*(short *)(param_1 + 0x4cc) >> 0x1f & 0x1fU)) >> 5);
  uVar1 = (int)((int)*(short *)(param_1 + 0x4ce) + ((int)*(short *)(param_1 + 0x4ce) >> 0x1f & 0xfU)
               ) >> 4;
  local_10 = (undefined2)uVar1;
  iVar2 = FUN__text__004709d0(param_1,CONCAT22((short)((uint)local_18 >> 0x10),local_c),
                              uVar1 & 0xffff,local_14,local_18);
  if (iVar2 != 0) {
    *(short *)(param_1 + 0x4d0) = local_14[0] * 0x20 + 0x10;
    *(short *)(param_1 + 0x4d2) = local_18[0] * 0x10 + 8;
  }
  local_8 = 0x4708eb;
  FUN__text__0056ce80();
  return;
}

