
void __thiscall
FUN__text__004064a0(undefined4 param_1,int *param_2,int param_3,int param_4,undefined4 param_5)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_c4 [16];
  undefined4 local_84;
  int local_80;
  int local_7c;
  int local_78;
  int local_74;
  int local_70;
  undefined4 local_6c;
  int local_68;
  int local_64;
  undefined1 local_60 [32];
  undefined1 local_40 [32];
  int *local_20;
  int *local_1c;
  undefined4 local_18;
  undefined4 local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058eb2b;
  local_10 = ExceptionList;
  puVar2 = local_c4;
  for (iVar1 = 0x2d; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_6c = 1;
  ExceptionList = &local_10;
  local_14 = param_1;
  if (*(int *)(param_3 + 0x30) != 0) {
    local_18 = 0;
    local_1c = (int *)0x0;
    local_20 = (int *)0x0;
    ExceptionList = &local_10;
    local_74 = FUN__text__00428a40(0x48);
    local_8 = 0;
    if (local_74 == 0) {
      local_80 = 0;
    }
    else {
      local_80 = FUN__text__00403620();
    }
    local_70 = local_80;
    local_8 = 0xffffffff;
    local_68 = local_80;
    if (local_80 != 0) {
      *(undefined2 *)(local_80 + 0x38) = *(undefined2 *)(param_3 + 0x38);
      *(undefined2 *)(local_80 + 0x3a) = *(undefined2 *)(param_3 + 0x3a);
      *(undefined4 *)(local_80 + 0x34) = *(undefined4 *)(param_3 + 0x34);
      iVar1 = FUN__text__00403bd0(param_2,0);
      if (iVar1 == 0) {
        FUN__text__00403730();
        *(undefined2 *)(param_4 + 0x38) = *(undefined2 *)(param_3 + 0x38);
        *(undefined2 *)(param_4 + 0x3a) = *(undefined2 *)(param_3 + 0x3a);
        *(undefined4 *)(param_4 + 0x34) = 0x19;
        iVar1 = FUN__text__00403bd0(param_2,0);
        if (iVar1 == 0) {
          (**(code **)(**(int **)(param_4 + 0x2c) + 0x38))
                    (*(undefined4 *)(param_4 + 0x2c),0,local_40);
          local_64 = FUN__text__0056ce80();
          if (-1 < local_64) {
            (**(code **)(**(int **)(local_68 + 0x2c) + 0x38))
                      (*(undefined4 *)(local_68 + 0x2c),0,local_60);
            local_64 = FUN__text__0056ce80();
            if (-1 < local_64) {
              local_18 = *(undefined4 *)(param_3 + 0x30);
              (**(code **)(**(int **)(param_4 + 0x2c) + 0x3c))
                        (*(undefined4 *)(param_4 + 0x2c),0,&local_1c);
              local_64 = FUN__text__0056ce80();
              if (-1 < local_64) {
                (**(code **)(**(int **)(local_68 + 0x2c) + 0x3c))
                          (*(undefined4 *)(local_68 + 0x2c),0,&local_20);
                local_64 = FUN__text__0056ce80();
                if (-1 < local_64) {
                  (**(code **)(*param_2 + 0x70))(param_2,local_18,0,0,local_20,0);
                  local_64 = FUN__text__0056ce80();
                  if ((-1 < local_64) &&
                     (local_64 = FUN__text__00528b33(local_1c,0,0,local_20,0,0,1,param_5),
                     -1 < local_64)) {
                    local_6c = 0;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  if (local_1c != (int *)0x0) {
    (**(code **)(*local_1c + 8))(local_1c);
    FUN__text__0056ce80();
  }
  if (local_20 != (int *)0x0) {
    (**(code **)(*local_20 + 8))(local_20);
    FUN__text__0056ce80();
  }
  if (local_68 != 0) {
    local_7c = local_68;
    local_78 = local_68;
    if (local_68 == 0) {
      local_84 = 0;
    }
    else {
      local_84 = FUN__text__00406370(1);
    }
  }
  ExceptionList = local_10;
  local_8 = 0x406775;
  FUN__text__0056ce80();
  return;
}

