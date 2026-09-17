
void __thiscall FUN__text__00471f50(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_58;
  for (iVar1 = 0x15; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_14 = ((int)((*(int *)(param_2 + 0x2ec) >> 0x10) +
                   (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)) >> 5) + -0xf;
  local_18 = ((int)((*(int *)(param_2 + 0x2f0) >> 0x10) + (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)
                   ) >> 4) + -0xf;
  local_8 = param_1;
  for (local_10 = local_18; local_10 != local_18 + 0x1f; local_10 = local_10 + 1) {
    if (-1 < local_10) {
      if (*(short *)(*(int *)(local_8 + 0x2a304) + 6) <= local_10) break;
      for (local_c = local_14; local_c != local_14 + 0x1f; local_c = local_c + 1) {
        if (-1 < local_c) {
          if (*(short *)(*(int *)(local_8 + 0x2a304) + 4) <= local_c) break;
          iVar1 = FUN__text__0043be60(local_c,local_10,
                                      *(undefined1 *)(*(int *)(param_2 + 600) + 0x30));
          if (iVar1 == 0) {
            *(undefined1 *)
             ((local_c - local_14) + local_8 + 0x108f7c + (local_10 - local_18) * 0x1f) = 0xff;
          }
        }
      }
    }
  }
  local_8 = 0x472083;
  FUN__text__0056ce80();
  return;
}

