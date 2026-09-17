
void __thiscall FUN__text__004721d0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = ((int)((*(int *)(param_2 + 0x2ec) >> 0x10) + (*(int *)(param_2 + 0x2ec) >> 0x1f & 0x1fU)
                  ) >> 5) + -0xf;
  local_18 = ((int)((*(int *)(param_2 + 0x2f0) >> 0x10) + (*(int *)(param_2 + 0x2f0) >> 0x1f & 0xfU)
                   ) >> 4) + -0xf;
  local_10 = local_18;
  local_8 = param_1;
  for (; local_18 != local_10 + 0x1f; local_18 = local_18 + 1) {
    if (-1 < local_18) {
      if (*(short *)(*(int *)(local_8 + 0x2a304) + 6) <= local_18) break;
      for (local_14 = local_c; local_14 != local_c + 0x1f; local_14 = local_14 + 1) {
        if (-1 < local_14) {
          if (*(short *)(*(int *)(local_8 + 0x2a304) + 4) <= local_14) break;
          if ((*(char *)((local_14 - local_c) + local_8 + 0x108f7c + (local_18 - local_10) * 0x1f)
               != -1) &&
             (*(char *)((local_14 - local_c) + local_8 + 0x108f7c + (local_18 - local_10) * 0x1f) !=
              '\0')) {
            local_1c = local_14 * 0x20 - (int)*(short *)(local_8 + 0x2a30e);
            local_20 = (local_18 * 0x10 - (int)*(short *)(local_8 + 0x2a310)) + 0x1e;
            FUN__text__00410310(local_1c,local_20,0x20,0x10,0xeff,0x80ff0000,1);
          }
        }
      }
    }
  }
  local_8 = 0x47235f;
  FUN__text__0056ce80();
  return;
}

