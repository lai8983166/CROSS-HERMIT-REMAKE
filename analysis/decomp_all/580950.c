
/* Library Function - Single Match
    ___init_time
   
   Library: Visual Studio 2003 Debug */

int __cdecl ___init_time(threadlocinfo *_LocInfo)

{
  undefined *puVar1;
  int iVar2;
  
  if (DAT_0080a638 == 0) {
    PTR_PTR_00765160 = (undefined *)&PTR_PTR_00765168;
    ___free_lc_time(DAT_0080a608);
    __free_dbg(DAT_0080a608,2);
    DAT_0080a608 = (undefined *)0x0;
    iVar2 = 0;
  }
  else {
    puVar1 = (undefined *)__calloc_dbg(1,0xac,2,"inittime.c",0x48);
    if (puVar1 == (undefined *)0x0) {
      iVar2 = 1;
    }
    else {
      iVar2 = FUN__text__00580a30(puVar1);
      if (iVar2 == 0) {
        PTR_PTR_00765160 = puVar1;
        ___free_lc_time(DAT_0080a608);
        __free_dbg(DAT_0080a608,2);
        iVar2 = 0;
        DAT_0080a608 = puVar1;
      }
      else {
        ___free_lc_time(puVar1);
        __free_dbg(puVar1,2);
        iVar2 = 1;
      }
    }
  }
  return iVar2;
}

