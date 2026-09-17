
void __thiscall
FUN__text__00405ff0(undefined4 param_1,int *param_2,int param_3,int param_4,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_e4 [16];
  undefined4 local_a4;
  int local_a0;
  int local_9c;
  int local_98;
  int local_94;
  int local_90;
  undefined4 local_8c;
  int local_88;
  int local_84;
  undefined1 local_80 [32];
  undefined1 local_60 [32];
  undefined1 local_40 [32];
  int *local_20;
  int *local_1c;
  int *local_18;
  undefined4 local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058eb0e;
  local_10 = ExceptionList;
  puVar2 = local_e4;
  for (iVar1 = 0x35; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8c = 1;
  ExceptionList = &local_10;
  local_14 = param_1;
  if (*(int *)(param_3 + 0x2c) != 0) {
    local_18 = (int *)0x0;
    local_1c = (int *)0x0;
    local_20 = (int *)0x0;
    ExceptionList = &local_10;
    local_94 = FUN__text__00428a40(0x48);
    local_8 = 0;
    if (local_94 == 0) {
      local_a0 = 0;
    }
    else {
      local_a0 = FUN__text__00403620();
    }
    local_90 = local_a0;
    local_8 = 0xffffffff;
    local_88 = local_a0;
    if ((local_a0 != 0) && (iVar1 = FUN__text__00403e70(param_2,param_3), iVar1 == 0)) {
      FUN__text__00403730();
      *(undefined2 *)(param_4 + 0x38) = *(undefined2 *)(param_3 + 0x38);
      *(undefined2 *)(param_4 + 0x3a) = *(undefined2 *)(param_3 + 0x3a);
      *(undefined4 *)(param_4 + 0x34) = 0x19;
      iVar1 = FUN__text__00403bd0(param_2,0);
      if (iVar1 == 0) {
        (**(code **)(**(int **)(param_3 + 0x2c) + 0x38))(*(undefined4 *)(param_3 + 0x2c),0,local_40)
        ;
        local_84 = FUN__text__0056ce80();
        if (-1 < local_84) {
          (**(code **)(**(int **)(param_4 + 0x2c) + 0x38))
                    (*(undefined4 *)(param_4 + 0x2c),0,local_60);
          local_84 = FUN__text__0056ce80();
          if (-1 < local_84) {
            (**(code **)(**(int **)(local_88 + 0x2c) + 0x38))
                      (*(undefined4 *)(local_88 + 0x2c),0,local_80);
            local_84 = FUN__text__0056ce80();
            if (-1 < local_84) {
              (**(code **)(**(int **)(param_3 + 0x2c) + 0x3c))
                        (*(undefined4 *)(param_3 + 0x2c),0,&local_18);
              local_84 = FUN__text__0056ce80();
              if (-1 < local_84) {
                (**(code **)(**(int **)(param_4 + 0x2c) + 0x3c))
                          (*(undefined4 *)(param_4 + 0x2c),0,&local_1c);
                local_84 = FUN__text__0056ce80();
                if (-1 < local_84) {
                  (**(code **)(**(int **)(local_88 + 0x2c) + 0x3c))
                            (*(undefined4 *)(local_88 + 0x2c),0,&local_20);
                  local_84 = FUN__text__0056ce80();
                  if (-1 < local_84) {
                    (**(code **)(*param_2 + 0x70))(param_2,local_18,0,0,local_20,0);
                    local_84 = FUN__text__0056ce80();
                    if ((-1 < local_84) &&
                       (local_84 = FUN__text__00528b33(local_1c,0,0,local_20,0,0,1,param_5),
                       -1 < local_84)) {
                      local_8c = 0;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  if (local_18 != (int *)0x0) {
    (**(code **)(*local_18 + 8))(local_18);
    FUN__text__0056ce80();
  }
  if (local_1c != (int *)0x0) {
    (**(code **)(*local_1c + 8))(local_1c);
    FUN__text__0056ce80();
  }
  if (local_20 != (int *)0x0) {
    (**(code **)(*local_20 + 8))(local_20);
    FUN__text__0056ce80();
  }
  if (local_88 != 0) {
    local_9c = local_88;
    local_98 = local_88;
    if (local_88 == 0) {
      local_a4 = 0;
    }
    else {
      local_a4 = FUN__text__00406370(1);
    }
  }
  ExceptionList = local_10;
  local_8 = 0x406360;
  FUN__text__0056ce80();
  return;
}

