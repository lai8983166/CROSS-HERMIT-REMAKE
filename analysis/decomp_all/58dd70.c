
int FUN__text__0058dd70(uint param_1,int param_2)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  
  iVar2 = (int)param_1 >> 5;
  cVar1 = *(char *)((&DAT_0080a800)[iVar2] + 4 + (param_1 & 0x1f) * 0x24);
  if (param_2 == 0x8000) {
    *(byte *)((&DAT_0080a800)[iVar2] + 4 + (param_1 & 0x1f) * 0x24) =
         *(byte *)((&DAT_0080a800)[iVar2] + 4 + (param_1 & 0x1f) * 0x24) & 0x7f;
  }
  else {
    if (param_2 != 0x4000) {
      puVar3 = (undefined4 *)FUN__text__00576d20();
      *puVar3 = 0x16;
      return -1;
    }
    *(byte *)((&DAT_0080a800)[iVar2] + 4 + (param_1 & 0x1f) * 0x24) =
         *(byte *)((&DAT_0080a800)[iVar2] + 4 + (param_1 & 0x1f) * 0x24) | 0x80;
  }
  return (-(uint)(((int)cVar1 & 0x80U) != 0) & 0xffffc000) + 0x8000;
}

