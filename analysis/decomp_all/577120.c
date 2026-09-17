
void __fastcall FUN__text__00577120(undefined4 param_1)

{
  int iVar1;
  uint uVar2;
  
  if (DAT_0080bb60 == 0) {
    DAT_0080bb60 = 0x200;
  }
  else if (DAT_0080bb60 < 0x14) {
    DAT_0080bb60 = 0x14;
  }
  DAT_0080ab50 = __calloc_dbg(DAT_0080bb60,4,2,"_file.c",0x83,param_1);
  if (DAT_0080ab50 == 0) {
    DAT_0080bb60 = 0x14;
    DAT_0080ab50 = __calloc_dbg(0x14,4,2,"_file.c",0x86,param_1);
    if (DAT_0080ab50 == 0) {
      __amsg_exit(0x1a);
    }
  }
  for (iVar1 = 0; iVar1 < 0x14; iVar1 = iVar1 + 1) {
    *(undefined ***)(DAT_0080ab50 + iVar1 * 4) = &PTR_DAT_00761eb0 + iVar1 * 8;
  }
  for (uVar2 = 0; (int)uVar2 < 3; uVar2 = uVar2 + 1) {
    if ((*(int *)((&DAT_0080a800)[(int)uVar2 >> 5] + (uVar2 & 0x1f) * 0x24) == -1) ||
       (*(int *)((&DAT_0080a800)[(int)uVar2 >> 5] + (uVar2 & 0x1f) * 0x24) == 0)) {
      *(undefined4 *)(&DAT_00761ec0 + uVar2 * 0x20) = 0xffffffff;
    }
  }
  return;
}

