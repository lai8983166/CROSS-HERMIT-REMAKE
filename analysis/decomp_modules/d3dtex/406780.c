
void FUN__text__00406780(int *param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_9c [16];
  undefined4 local_5c;
  int local_58;
  int local_54;
  undefined4 local_50;
  int local_4c;
  undefined4 local_48;
  undefined4 local_44;
  int local_40;
  int local_3c;
  undefined4 local_38 [8];
  int *local_18;
  int *local_14;
  int *local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_9c;
  for (iVar1 = 0x26; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_50 = 1;
  local_10 = (int *)0x0;
  local_14 = (int *)0x0;
  local_18 = (int *)0x0;
  (**(code **)(*param_1 + 0x40))(param_1,0,0,&local_10);
  local_4c = FUN__text__0056ce80();
  if (-1 < local_4c) {
    _memset(local_38,0,0x20);
    (**(code **)(*local_10 + 0x20))(local_10,local_38);
    local_4c = FUN__text__0056ce80();
    if (-1 < local_4c) {
      local_48 = 0;
      local_44 = 0;
      local_40 = (int)*(short *)(local_8 + 0x38);
      local_3c = (int)*(short *)(local_8 + 0x3a);
      local_c = 0;
      (**(code **)(*param_1 + 0x6c))
                (param_1,(int)*(short *)(local_8 + 0x38),(int)*(short *)(local_8 + 0x3a),local_38[0]
                 ,&local_18);
      local_4c = FUN__text__0056ce80();
      if (-1 < local_4c) {
        (**(code **)(*param_1 + 0x70))(param_1,local_10,&local_48,1,local_18,0);
        local_4c = FUN__text__0056ce80();
        if (-1 < local_4c) {
          FUN__text__00403730();
          *(undefined4 *)(local_8 + 0x34) = 0x19;
          local_4c = FUN__text__00403bd0(param_1,0);
          if (local_4c == 0) {
            (**(code **)(**(int **)(local_8 + 0x2c) + 0x3c))
                      (*(undefined4 *)(local_8 + 0x2c),0,&local_14);
            local_4c = FUN__text__0056ce80();
            if ((-1 < local_4c) &&
               (local_4c = FUN__text__00528b33(local_14,0,0,local_18,0,0,1,param_2), -1 < local_4c))
            {
              local_50 = 0;
            }
          }
        }
      }
    }
    if (local_10 != (int *)0x0) {
      (**(code **)(*local_10 + 8))(local_10);
      FUN__text__0056ce80();
    }
    if (local_14 != (int *)0x0) {
      (**(code **)(*local_14 + 8))(local_14);
      FUN__text__0056ce80();
    }
    if (local_18 != (int *)0x0) {
      (**(code **)(*local_18 + 8))(local_18);
      FUN__text__0056ce80();
    }
    if (local_c != 0) {
      local_58 = local_c;
      local_54 = local_c;
      if (local_c == 0) {
        local_5c = 0;
      }
      else {
        local_5c = FUN__text__00406370(1);
      }
    }
  }
  local_18 = (int *)0x406a01;
  FUN__text__0056ce80();
  return;
}

