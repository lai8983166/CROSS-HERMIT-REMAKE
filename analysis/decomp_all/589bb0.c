
int FUN__text__00589bb0(byte *param_1,uint param_2,byte *param_3,undefined4 param_4,
                       undefined *param_5)

{
  byte *pbVar1;
  int iVar2;
  bool bVar3;
  undefined *local_14;
  uint local_10;
  uint local_c;
  undefined *local_8;
  
  local_10 = param_2;
  (*API_KERNEL32_DLL_InterlockedIncrement)(&DAT_0080bb6c);
  bVar3 = DAT_0080bb68 != 0;
  if (bVar3) {
    (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
    FUN__text__00577040(0x13);
  }
  local_c = (uint)bVar3;
  if (param_5 == (undefined *)0x0) {
    local_14 = PTR_PTR_00765160;
  }
  else {
    local_14 = param_5;
  }
  local_8 = local_14;
  for (; (local_10 != 0 && (*param_3 != 0)); param_3 = param_3 + 1) {
    if (*param_3 == 0x25) {
      bVar3 = param_3[1] == 0x23;
      pbVar1 = param_3 + 1;
      if (bVar3) {
        pbVar1 = param_3 + 2;
      }
      param_3 = pbVar1;
      DAT_0080a7f4 = (uint)bVar3;
      FUN__text__00589d40(CONCAT31((int3)((uint)&param_1 >> 8),*param_3),param_4,&param_1,&local_10,
                          local_8);
    }
    else {
      if (((*(ushort *)(PTR_DAT_00764164 + (uint)*param_3 * 2) & 0x8000) != 0) && (1 < local_10)) {
        *param_1 = *param_3;
        param_1 = param_1 + 1;
        param_3 = param_3 + 1;
        local_10 = local_10 - 1;
      }
      *param_1 = *param_3;
      param_1 = param_1 + 1;
      local_10 = local_10 - 1;
    }
  }
  if (local_c == 0) {
    (*API_KERNEL32_DLL_InterlockedDecrement)(&DAT_0080bb6c);
  }
  else {
    FUN__text__005770e0(0x13);
  }
  if (local_10 == 0) {
    iVar2 = 0;
  }
  else {
    *param_1 = 0;
    iVar2 = param_2 - local_10;
  }
  return iVar2;
}

