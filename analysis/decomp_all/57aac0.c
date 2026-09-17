
void FUN_0057aac0(int param_1)

{
  undefined *puVar1;
  int iVar2;
  undefined *local_18;
  int local_14;
  int local_10;
  int *local_8;
  
  local_18 = PTR_LOOP_0076213c;
  do {
    puVar1 = local_18;
    if (*(int *)(local_18 + 0x10) != -1) {
      local_14 = 0;
      local_8 = (int *)(local_18 + 0x2010);
      for (local_10 = 0x3ff; -1 < local_10; local_10 = local_10 + -1) {
        if ((*local_8 == 0xf0) &&
           (iVar2 = (*API_KERNEL32_DLL_VirtualFree)
                              (*(int *)(local_18 + 0x10) + local_10 * 0x1000,0x1000,0x4000),
           iVar2 != 0)) {
          *local_8 = -1;
          DAT_0080a4f4 = DAT_0080a4f4 + -1;
          if ((*(int *)(local_18 + 0xc) == 0) || (local_8 < *(int **)(local_18 + 0xc))) {
            *(int **)(local_18 + 0xc) = local_8;
          }
          local_14 = local_14 + 1;
          param_1 = param_1 + -1;
          if (param_1 == 0) break;
        }
        local_8 = local_8 + -2;
      }
      puVar1 = *(undefined **)(local_18 + 4);
      if ((local_14 != 0) && (*(int *)(local_18 + 0x18) == -1)) {
        local_10 = 1;
        for (local_8 = (int *)(local_18 + 0x20); (local_10 < 0x400 && (*local_8 == -1));
            local_8 = local_8 + 2) {
          local_10 = local_10 + 1;
        }
        if (local_10 == 0x400) {
          FUN_0057aa40(local_18);
        }
      }
    }
    local_18 = puVar1;
    if ((local_18 == PTR_LOOP_0076213c) || (param_1 < 1)) {
      return;
    }
  } while( true );
}

