
undefined4 FUN__text1__0083e932(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 local_8;
  
  local_8 = 0;
  if ((param_1 == 0) || (*(int *)(param_1 + 0x1c) == 0)) {
    local_8 = 0xfffffffe;
  }
  else {
    iVar1 = *(int *)(param_1 + 0x1c);
    if (param_2 == -1) {
      param_2 = 6;
    }
    if ((((param_2 < 0) || (9 < param_2)) || (param_3 < 0)) || (2 < param_3)) {
      local_8 = 0xfffffffe;
    }
    else {
      if (((&PTR_DAT_00872e80)[*(int *)(iVar1 + 0x7c) * 3] != (&PTR_DAT_00872e80)[param_2 * 3]) &&
         (*(int *)(param_1 + 8) != 0)) {
        local_8 = FUN__text1__0083ea4e(param_1,1);
      }
      if (*(int *)(iVar1 + 0x7c) != param_2) {
        *(int *)(iVar1 + 0x7c) = param_2;
        *(uint *)(iVar1 + 0x78) = (uint)*(ushort *)(&DAT_00872e7a + param_2 * 0xc);
        *(uint *)(iVar1 + 0x84) = (uint)*(ushort *)(&DAT_00872e78 + param_2 * 0xc);
        *(uint *)(iVar1 + 0x88) = (uint)*(ushort *)(&DAT_00872e7c + param_2 * 0xc);
        *(uint *)(iVar1 + 0x74) = (uint)*(ushort *)(&DAT_00872e7e + param_2 * 0xc);
      }
      *(int *)(iVar1 + 0x80) = param_3;
    }
  }
  return local_8;
}

