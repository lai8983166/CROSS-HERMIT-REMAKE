
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__0048cb30(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [21];
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  iVar1 = *(short *)(&DAT_006b2da0 + (uint)*(ushort *)(*(int *)(param_1 + 600) + 0xc) * 0x40) * 0x48
  ;
  if (param_2 == 10) {
    *(undefined2 *)(param_1 + 0xe) = *(undefined2 *)(&DAT_006c2dd2 + iVar1);
    *(undefined2 *)(param_1 + 0x12) = *(undefined2 *)(&DAT_006c2dd6 + iVar1);
    if (*(byte *)(*(int *)(param_1 + 600) + 5) < 0x4b) {
      *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) << 1;
    }
    else {
      *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) * 3;
    }
    *(short *)(param_1 + 0xe) = *(short *)(param_1 + 0xe) + _UNK_006c30a2;
    *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) + _UNK_006c30a6;
  }
  else if (param_2 == 0x10) {
    *(undefined2 *)(param_1 + 0xe) = *(undefined2 *)(&DAT_006c2dd2 + iVar1);
    *(undefined2 *)(param_1 + 0x12) = *(undefined2 *)(&DAT_006c2dd6 + iVar1);
    if (*(byte *)(*(int *)(param_1 + 600) + 5) < 0x4b) {
      *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) << 1;
    }
    else {
      *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) * 3;
    }
    *(short *)(param_1 + 0xe) = *(short *)(param_1 + 0xe) + _UNK_006c3252;
    *(short *)(param_1 + 0x12) = *(short *)(param_1 + 0x12) + _UNK_006c3256;
  }
  return;
}

