
/* WARNING: Instruction at (ram,0x00837d2e) overlaps instruction at (ram,0x00837d2d)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Removing unreachable block (ram,0x00837d26) */
/* WARNING: Removing unreachable block (ram,0x00837cb6) */
/* WARNING: Removing unreachable block (ram,0x00837e33) */
/* WARNING: Removing unreachable block (ram,0x00837e7c) */
/* WARNING: Removing unreachable block (ram,0x00837d33) */
/* WARNING: Removing unreachable block (ram,0x00837d32) */
/* WARNING: Removing unreachable block (ram,0x00837d16) */
/* WARNING: Removing unreachable block (ram,0x00837d57) */
/* WARNING: Removing unreachable block (ram,0x00837e25) */
/* WARNING: Removing unreachable block (ram,0x00837e4e) */
/* WARNING: Removing unreachable block (ram,0x00837e50) */
/* WARNING: Heritage AFTER dead removal. Example location: s0xfffffff0 : 0x00837d4c */
/* WARNING: Restarted to delay deadcode elimination for space: stack */

undefined4 FUN__text1__00837d03(void)

{
  HANDLE hObject;
  DWORD DVar1;
  byte abStack_118 [256];
  byte *pbStack_18;
  byte *pbStack_14;
  int iStack_10;
  undefined4 auStack_c [2];
  
  do {
    if (1 < iStack_10) {
      return 0;
    }
    pbStack_14 = (byte *)auStack_c[iStack_10];
    for (pbStack_18 = abStack_118; *pbStack_18 = *pbStack_14 ^ 0xd3, *pbStack_18 != 0;
        pbStack_18 = pbStack_18 + 1) {
      pbStack_14 = pbStack_14 + 1;
    }
    hObject = CreateMutexA((LPSECURITY_ATTRIBUTES)0x0,0,(LPCSTR)abStack_118);
    if (hObject == (HANDLE)0x0) {
      DVar1 = GetLastError();
      if (DVar1 == 6) {
        return 1;
      }
    }
    else {
      CloseHandle(hObject);
    }
    iStack_10 = iStack_10 + 1;
  } while( true );
}

