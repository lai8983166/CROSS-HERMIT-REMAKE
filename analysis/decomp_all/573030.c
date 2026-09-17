
undefined1 * FUN__text__00573030(void)

{
  bool bVar1;
  int iVar2;
  undefined1 *puVar3;
  int local_8;
  
  bVar1 = true;
  if (DAT_00761b2c == (undefined1 *)0x0) {
    DAT_00761b2c = (undefined1 *)__malloc_dbg(0x351,2,"setlocal.c",0x167);
  }
  *DAT_00761b2c = 0;
  for (local_8 = 1;
      __strcats(DAT_00761b2c,3,*(undefined4 *)(&UNK_00761b28 + local_8 * 0xc),&DAT_005f9dc0,
                (&DAT_00761b2c)[local_8 * 3]), local_8 < 5; local_8 = local_8 + 1) {
    FUN__text__0056cda0(DAT_00761b2c,&DAT_005f9dac);
    iVar2 = _strcmp((&DAT_00761b2c)[local_8 * 3],(&DAT_00761b2c)[(local_8 + 1) * 3]);
    if (iVar2 != 0) {
      bVar1 = false;
    }
  }
  puVar3 = DAT_00761b2c;
  if (bVar1) {
    __free_dbg(DAT_00761b2c,2);
    DAT_00761b2c = (undefined1 *)0x0;
    puVar3 = PTR_DAT_00761b44;
  }
  return puVar3;
}

