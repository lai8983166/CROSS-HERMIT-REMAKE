
void __fastcall FUN__text__0043b530(int param_1)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  undefined4 *puVar8;
  undefined4 local_58 [21];
  
  puVar8 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar8 = 0xcccccccc;
    puVar8 = puVar8 + 1;
  }
  if (*(int *)(param_1 + 0x2659c) == 0) {
    *(undefined2 *)(param_1 + 0x265ac) = 0xffff;
    *(undefined2 *)(param_1 + 0x265aa) = 0xffff;
  }
  else {
    uVar1 = *(uint *)(DAT_007a49fc + 0x196c);
    uVar3 = *(int *)(DAT_007a49fc + 0x1970) - 0x1e;
    if (((int)uVar3 < 0) || (0x23f < (int)uVar3)) {
      *(undefined2 *)(param_1 + 0x265ac) = 0xffff;
      *(undefined2 *)(param_1 + 0x265aa) = 0xffff;
    }
    else {
      uVar6 = uVar1 & 0x8000001f;
      if ((int)uVar6 < 0) {
        uVar6 = (uVar6 - 1 | 0xffffffe0) + 1;
      }
      uVar4 = (int)*(short *)(param_1 + 0x265a6) & 0x8000001f;
      if ((int)uVar4 < 0) {
        uVar4 = (uVar4 - 1 | 0xffffffe0) + 1;
      }
      uVar7 = uVar3 & 0x8000000f;
      if ((int)uVar7 < 0) {
        uVar7 = (uVar7 - 1 | 0xfffffff0) + 1;
      }
      uVar5 = (int)*(short *)(param_1 + 0x265a8) & 0x8000000f;
      if ((int)uVar5 < 0) {
        uVar5 = (uVar5 - 1 | 0xfffffff0) + 1;
      }
      *(short *)(param_1 + 0x265aa) =
           (short)((int)(uVar1 + ((int)uVar1 >> 0x1f & 0x1fU)) >> 5) +
           (short)((int)((int)*(short *)(param_1 + 0x265a6) +
                        ((int)*(short *)(param_1 + 0x265a6) >> 0x1f & 0x1fU)) >> 5) +
           (short)((int)(uVar6 + uVar4 + ((int)(uVar6 + uVar4) >> 0x1f & 0x1fU)) >> 5);
      *(short *)(param_1 + 0x265ac) =
           (short)((int)(uVar3 + ((int)uVar3 >> 0x1f & 0xfU)) >> 4) +
           (short)((int)((int)*(short *)(param_1 + 0x265a8) +
                        ((int)*(short *)(param_1 + 0x265a8) >> 0x1f & 0xfU)) >> 4) +
           (short)((int)(uVar7 + uVar5 + ((int)(uVar7 + uVar5) >> 0x1f & 0xfU)) >> 4);
      if ((*(short *)(*(int *)(param_1 + 0x2659c) + 4) <= *(short *)(param_1 + 0x265aa)) ||
         (*(short *)(*(int *)(param_1 + 0x2659c) + 6) <= *(short *)(param_1 + 0x265ac))) {
        *(undefined2 *)(param_1 + 0x265ac) = 0xffff;
        *(undefined2 *)(param_1 + 0x265aa) = 0xffff;
      }
    }
  }
  return;
}

