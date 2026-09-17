
void __thiscall FUN__text__0046eda0(int param_1,int param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_5c;
  for (iVar1 = 0x16; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_18 = 0;
  if (param_3 != 0) {
    local_1c = param_3;
    if (param_3 == 1) {
      local_c = 0;
      local_10 = 10;
    }
    else if (param_3 == 2) {
      local_c = 10;
      local_10 = 0x14;
    }
    else if (param_3 == 3) {
      local_c = 0;
      local_10 = 0x14;
    }
    local_8 = param_1;
    for (local_14 = local_c; local_14 != local_10; local_14 = local_14 + 1) {
      if ((((*(int *)(local_8 + 0xdb818 + local_14 * 4) != 0) &&
           (iVar1 = FUN__text__0046fac0(param_2,local_14), iVar1 != 0)) &&
          (iVar1 = FUN__text__00468f40(*(undefined4 *)(local_8 + 0xdb818 + local_14 * 4)),
          iVar1 != 0)) &&
         (iVar1 = FUN__text__0046a430(*(undefined4 *)(local_8 + 0xdb818 + local_14 * 4)), iVar1 != 0
         )) {
        if ((*(uint *)(DAT_007a49fc + 0x194c) & 0x40000) == 0) {
          *(undefined1 *)(*(int *)(local_8 + 0xdb818 + local_14 * 4) + 0x28c) = 1;
        }
        else {
          *(byte *)(*(int *)(local_8 + 0xdb818 + local_14 * 4) + 0x28c) =
               *(byte *)(*(int *)(local_8 + 0xdb818 + local_14 * 4) + 0x28c) ^ 1;
        }
        *(int *)(local_8 + 0x108f74) = *(int *)(local_8 + 0x108f74) + 1;
        local_18 = local_18 + 1;
        if (((param_2 == 0) &&
            (iVar1 = FUN__text__00469480(*(undefined4 *)(local_8 + 0xdb818 + local_14 * 4)),
            iVar1 != 0)) && ((*(uint *)(DAT_007a49fc + 0x1990) & 8) != 0)) {
          FUN__text__0043b400(*(int *)(*(int *)(local_8 + 0xdb818 + local_14 * 4) + 0x2ec) >> 0x10,
                              *(int *)(*(int *)(local_8 + 0xdb818 + local_14 * 4) + 0x2f0) >> 0x10);
        }
      }
    }
  }
  local_8 = 0x46ef9a;
  FUN__text__0056ce80();
  return;
}

