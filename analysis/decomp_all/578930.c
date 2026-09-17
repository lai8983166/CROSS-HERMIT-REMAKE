
/* Library Function - Single Match
    __heapchk
   
   Library: Visual Studio 2003 Debug */

int __cdecl __heapchk(void)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 *unaff_FS_OFFSET;
  int local_20;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fa2b0;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  local_20 = -2;
  if (DAT_0080ab2c == 3) {
    FUN_00577040(9);
    local_8 = 0;
    FUN_0057a200();
    local_8 = 0xffffffff;
    FUN_00578992();
    iVar1 = thunk_FUN_005789e2();
    return iVar1;
  }
  if (DAT_0080ab2c == 2) {
    FUN_00577040(9);
    local_8 = 1;
    FUN_0057b500();
    local_8 = 0xffffffff;
    FUN_005789d7();
    iVar1 = FUN_005789e2();
    return iVar1;
  }
  iVar1 = (*API_KERNEL32_DLL_HeapValidate)(DAT_0080ab28,0,0);
  if (iVar1 == 0) {
    iVar1 = (*API_KERNEL32_DLL_GetLastError)();
    if (iVar1 == 0x78) {
      puVar2 = (undefined4 *)FUN_00576d30();
      *puVar2 = 0x78;
      puVar2 = (undefined4 *)FUN_00576d20();
      *puVar2 = 0x28;
    }
    else {
      local_20 = -4;
    }
  }
  *unaff_FS_OFFSET = uStack_14;
  return local_20;
}

