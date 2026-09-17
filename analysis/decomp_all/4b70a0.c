
void FUN__text__004b70a0(uint param_1,undefined4 param_2,undefined1 param_3)

{
  undefined2 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined2 *local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = (param_1 & 0xffff) * 10;
  local_c = (undefined2 *)(&DAT_0061c120 + iVar2);
  uVar1 = (undefined2)((uint)local_c >> 0x10);
  FUN__text__004b7230(CONCAT22(uVar1,*(undefined2 *)(&DAT_0061c124 + iVar2)),
                      CONCAT22(uVar1,*(undefined2 *)(&DAT_0061c126 + iVar2)),0,0,
                      CONCAT22(uVar1,(ushort)(byte)(&DAT_0061c128)[iVar2]),
                      CONCAT22(uVar1,*(undefined2 *)(&DAT_0061c122 + iVar2)),*local_c,param_2,
                      param_3);
  local_8 = 0x4b7119;
  FUN__text__0056ce80();
  return;
}

