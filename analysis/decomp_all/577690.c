
int FUN__text__00577690(int param_1)

{
  int iVar1;
  int local_10;
  int local_c;
  int local_8;
  
  local_8 = 0;
  local_c = 0;
  FUN__text__00577040(2);
  for (local_10 = 0; local_10 < DAT_0080bb60; local_10 = local_10 + 1) {
    if ((*(int *)(DAT_0080ab50 + local_10 * 4) != 0) &&
       ((*(uint *)(*(int *)(DAT_0080ab50 + local_10 * 4) + 0xc) & 0x83) != 0)) {
      FUN__text__005772b0(local_10,*(undefined4 *)(DAT_0080ab50 + local_10 * 4));
      if ((*(uint *)(*(int *)(DAT_0080ab50 + local_10 * 4) + 0xc) & 0x83) != 0) {
        if (param_1 == 1) {
          iVar1 = FUN__text__00577570(*(undefined4 *)(DAT_0080ab50 + local_10 * 4));
          if (iVar1 != -1) {
            local_8 = local_8 + 1;
          }
        }
        else if (((param_1 == 0) &&
                 ((*(uint *)(*(int *)(DAT_0080ab50 + local_10 * 4) + 0xc) & 2) != 0)) &&
                (iVar1 = FUN__text__00577570(*(undefined4 *)(DAT_0080ab50 + local_10 * 4)),
                iVar1 == -1)) {
          local_c = -1;
        }
      }
      FUN__text__00577320(local_10,*(undefined4 *)(DAT_0080ab50 + local_10 * 4));
    }
  }
  FUN__text__005770e0(2);
  if (param_1 == 1) {
    local_c = local_8;
  }
  return local_c;
}

