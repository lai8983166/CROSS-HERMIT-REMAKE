
undefined4 * __fastcall FUN_005797e0(undefined4 param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  
  if (DAT_0080ab44 == DAT_0080ab30) {
    iVar1 = (*API_NTDLL_DLL_RtlReAllocateHeap)
                      (DAT_0080ab28,0,DAT_0080ab48,(DAT_0080ab30 + 0x10) * 0x14,param_1);
    if (iVar1 == 0) {
      return (undefined4 *)0x0;
    }
    DAT_0080ab30 = DAT_0080ab30 + 0x10;
    DAT_0080ab48 = iVar1;
  }
  puVar3 = (undefined4 *)(DAT_0080ab48 + DAT_0080ab44 * 0x14);
  uVar2 = (*API_NTDLL_DLL_RtlAllocateHeap)(DAT_0080ab28,8,0x41c4);
  puVar3[4] = uVar2;
  if (puVar3[4] == 0) {
    puVar3 = (undefined4 *)0x0;
  }
  else {
    uVar2 = (*API_KERNEL32_DLL_VirtualAlloc)(0,0x100000,0x2000,4);
    puVar3[3] = uVar2;
    if (puVar3[3] == 0) {
      (*API_KERNEL32_DLL_HeapFree)(DAT_0080ab28,0,puVar3[4]);
      puVar3 = (undefined4 *)0x0;
    }
    else {
      *puVar3 = 0;
      puVar3[1] = 0;
      puVar3[2] = 0xffffffff;
      DAT_0080ab44 = DAT_0080ab44 + 1;
      *(undefined4 *)puVar3[4] = 0xffffffff;
    }
  }
  return puVar3;
}

