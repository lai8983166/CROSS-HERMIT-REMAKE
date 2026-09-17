
undefined4 * FUN__text1__0084b548(void)

{
  undefined4 *puVar1;
  LPVOID pvVar2;
  
  if (DAT_00876b34 == DAT_00876b24) {
    pvVar2 = HeapReAlloc(DAT_00876b40,0,DAT_00876b38,(DAT_00876b24 * 5 + 0x50) * 4);
    if (pvVar2 == (LPVOID)0x0) {
      return (undefined4 *)0x0;
    }
    DAT_00876b24 = DAT_00876b24 + 0x10;
    DAT_00876b38 = pvVar2;
  }
  puVar1 = (undefined4 *)((int)DAT_00876b38 + DAT_00876b34 * 0x14);
  pvVar2 = HeapAlloc(DAT_00876b40,8,0x41c4);
  puVar1[4] = pvVar2;
  if (pvVar2 != (LPVOID)0x0) {
    pvVar2 = VirtualAlloc((LPVOID)0x0,0x100000,0x2000,4);
    puVar1[3] = pvVar2;
    if (pvVar2 != (LPVOID)0x0) {
      puVar1[2] = 0xffffffff;
      *puVar1 = 0;
      puVar1[1] = 0;
      DAT_00876b34 = DAT_00876b34 + 1;
      *(undefined4 *)puVar1[4] = 0xffffffff;
      return puVar1;
    }
    HeapFree(DAT_00876b40,0,(LPVOID)puVar1[4]);
  }
  return (undefined4 *)0x0;
}

