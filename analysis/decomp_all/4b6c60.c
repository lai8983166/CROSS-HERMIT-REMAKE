
/* WARNING: Removing unreachable block (ram,0x004b6d60) */

void FUN__text__004b6c60(void)

{
  int iVar1;
  undefined2 uVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_64 [16];
  undefined1 local_24 [4];
  uint local_20;
  uint local_18;
  undefined *local_14;
  short local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar3 = local_64;
  for (iVar1 = 0x18; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = -1;
  local_c = local_c & 0xffff0000;
  do {
    if (1 < (local_c & 0xffff)) {
LAB__text__004b6d5a:
      local_10 = local_10 + 1;
      local_8 = 0x4b6d7f;
      FUN__text__0056ce80();
      return;
    }
    FUN__text__004d5c40(local_24,(local_c & 0xffff) + 0x20);
    if (((local_18 & 0xffff) != 0) && ((local_20 & 1) != 0)) {
      FUN__text__004db2b0(5);
      iVar1 = ((local_c & 0xffff) + 0x17) * 0x10;
      local_14 = &DAT_0061bae0 + iVar1;
      uVar2 = (undefined2)((uint)local_14 >> 0x10);
      FUN__text__004d67f0(0xd,0x4c,CONCAT22(uVar2,*(undefined2 *)(&DAT_0061bae2 + iVar1)),
                          CONCAT22(uVar2,*(undefined2 *)(&DAT_0061baec + iVar1)),
                          CONCAT22(uVar2,*(undefined2 *)(&DAT_0061baee + iVar1)),
                          CONCAT22(uVar2,*(undefined2 *)(&DAT_0061bae4 + iVar1)),
                          CONCAT22(uVar2,*(undefined2 *)(&DAT_0061bae6 + iVar1)),
                          CONCAT22(uVar2,*(undefined2 *)(&DAT_0061bae8 + iVar1)),
                          CONCAT22(extraout_var,*(undefined2 *)(&DAT_0061baea + iVar1)),4);
      local_10 = (short)local_c;
      goto LAB__text__004b6d5a;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  } while( true );
}

