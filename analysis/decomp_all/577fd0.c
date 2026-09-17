
/* Library Function - Single Match
    __heap_alloc_base
   
   Library: Visual Studio 2003 Debug */

void __heap_alloc_base(uint param_1)

{
  undefined4 *unaff_FS_OFFSET;
  undefined4 uStack_14;
  undefined *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &DAT_005fa250;
  puStack_10 = &DAT_00576b9c;
  uStack_14 = *unaff_FS_OFFSET;
  *unaff_FS_OFFSET = &uStack_14;
  if (DAT_0080ab2c == 3) {
    if (param_1 <= DAT_0080ab4c) {
      FUN_00577040(9);
      local_8 = 0;
      FUN_005792a0(param_1);
      local_8 = 0xffffffff;
      FUN_00578035();
      FUN_00578040();
      return;
    }
    FUN_005780e1();
    return;
  }
  if (DAT_0080ab2c == 2) {
    if (param_1 == 0) {
      param_1 = 0x10;
    }
    else {
      param_1 = param_1 + 0xf & 0xfffffff0;
    }
    if (param_1 <= DAT_0076415c) {
      FUN_00577040(9);
      local_8 = 1;
      FUN_0057ad20(param_1 >> 4);
      local_8 = 0xffffffff;
      FUN_005780b7();
      FUN_005780c2();
      return;
    }
    (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,param_1);
  }
  else {
    if (param_1 == 0) {
      param_1 = 1;
    }
    (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,0,param_1 + 0xf & 0xfffffff0);
  }
  *unaff_FS_OFFSET = uStack_14;
  return;
}

