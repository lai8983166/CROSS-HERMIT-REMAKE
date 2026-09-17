
undefined4 __thiscall FUN__text__0041db30(int *param_1,undefined4 param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  int iStack_7c;
  undefined4 local_6c [16];
  undefined1 *local_2c;
  int local_28;
  int local_24;
  undefined1 *local_20;
  undefined4 local_1c;
  int *local_18;
  int *local_14;
  undefined4 local_10;
  int local_c;
  int *local_8;
  
  puVar4 = local_6c;
  for (iVar3 = 0x1a; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_14 = (int *)0x0;
  local_18 = (int *)0x0;
  local_1c = 0;
  local_20 = (undefined1 *)0x0;
  local_24 = 0;
  local_28 = 0;
  if (*param_1 == 0) {
    local_10 = 1;
  }
  else if (param_1[1] == 0) {
    local_10 = 1;
  }
  else if (param_1[2] == 0) {
    local_10 = 1;
  }
  else if (param_1[5] == 0) {
    local_10 = 1;
  }
  else {
    *(undefined1 *)(param_1 + 8) = 0;
    *(undefined1 *)((int)param_1 + 0x21) = 0;
    local_10 = 1;
    iStack_7c = param_1[1];
    local_8 = param_1;
    (**(code **)(*(int *)param_1[1] + 0x24))();
    local_c = FUN__text__0056ce80();
    if (local_c < 0) {
      FUN__text__0041d040(local_c);
    }
    else {
      *(undefined2 *)(local_8 + 0x10) = 0;
      (*API_KERNEL32_DLL_MultiByteToWideChar)(0,0,param_2,0xffffffff,local_8 + 0x10,0x104);
      FUN__text__0056ce80();
      (**(code **)(*(int *)*local_8 + 0x38))(*local_8,local_8 + 0x10,local_8 + 0x10,local_8 + 7);
      local_c = FUN__text__0056ce80();
      if (local_c < 0) {
        FUN__text__0041d040(local_c);
      }
      else {
        (**(code **)(*(int *)local_8[7] + 0x2c))(local_8[7],L"Output",&local_14);
        local_c = FUN__text__0056ce80();
        if (local_c < 0) {
          FUN__text__0041d040(local_c);
        }
        else {
          (**(code **)(*(int *)*local_8 + 0x14))(*local_8,&local_18);
          local_c = FUN__text__0056ce80();
          if (local_c < 0) {
            FUN__text__0041d040(local_c);
          }
          else {
            while( true ) {
              (**(code **)(*local_18 + 0x10))(local_18,1);
              iVar3 = FUN__text__0056ce80();
              if (iVar3 != 0) break;
              local_24 = local_24 + 1;
            }
            (**(code **)(*local_18 + 0x14))(local_18);
            local_c = FUN__text__0056ce80();
            if (local_c < 0) {
              FUN__text__0041d040(local_c);
            }
            else {
              FUN__text__0056e230();
              local_2c = (undefined1 *)&iStack_7c;
              local_20 = (undefined1 *)&iStack_7c;
              if ((&stack0x00000000 == (undefined1 *)0x7c) &&
                 (local_2c = (undefined1 *)&iStack_7c, local_20 = (undefined1 *)&iStack_7c,
                 iVar3 = FUN__text__00424f80("ppFilters!=0",
                                             "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxShow.cpp"
                                             ,DAT_005ff5b8 + 0x40,0), iVar3 != 0)) {
                pcVar1 = (code *)swi(3);
                uVar2 = (*pcVar1)();
                return uVar2;
              }
              if (local_20 != (undefined1 *)0x0) {
                while( true ) {
                  (**(code **)(*local_18 + 0xc))(local_18,1,local_20 + local_28 * 4,0);
                  local_c = FUN__text__0056ce80();
                  if (local_c != 0) break;
                  local_28 = local_28 + 1;
                  local_c = 0;
                }
                if ((local_18 != (int *)0x0) && (local_18 != (int *)0x0)) {
                  (**(code **)(*local_18 + 8))(local_18);
                  FUN__text__0056ce80();
                  local_18 = (int *)0x0;
                }
                for (local_28 = 0; local_28 < local_24; local_28 = local_28 + 1) {
                  if (*(int *)(local_20 + local_28 * 4) == local_8[6]) {
                    (**(code **)(*(int *)*local_8 + 0x10))
                              (*local_8,*(undefined4 *)(local_20 + local_28 * 4));
                    local_c = FUN__text__0056ce80();
                  }
                  if ((*(int *)(local_20 + local_28 * 4) != 0) &&
                     (*(int *)(local_20 + local_28 * 4) != 0)) {
                    (**(code **)(**(int **)(local_20 + local_28 * 4) + 8))
                              (*(undefined4 *)(local_20 + local_28 * 4));
                    FUN__text__0056ce80();
                    *(undefined4 *)(local_20 + local_28 * 4) = 0;
                  }
                }
                (**(code **)(*(int *)*local_8 + 0x30))(*local_8,local_14);
                local_c = FUN__text__0056ce80();
                if (-1 < local_c) {
                  local_8[6] = local_8[7];
                  *(undefined1 *)(local_8 + 8) = 1;
                  local_10 = 0;
                }
              }
            }
          }
        }
      }
    }
    if (local_14 != (int *)0x0) {
      (**(code **)(*local_14 + 8))(local_14);
      FUN__text__0056ce80();
      local_14 = (int *)0x0;
    }
    if (local_8[7] != 0) {
      (**(code **)(*(int *)local_8[7] + 8))(local_8[7]);
      FUN__text__0056ce80();
      local_8[7] = 0;
    }
  }
  return local_10;
}

