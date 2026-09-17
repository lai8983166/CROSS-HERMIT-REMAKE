
int FUN__text1__00847936
              (uint param_1,undefined4 param_2,int param_3,int *param_4,int *param_5,
              undefined4 param_6,undefined4 param_7,undefined4 param_8,int param_9)

{
  int iVar1;
  undefined4 local_c;
  int local_8;
  
  local_c = 0;
  iVar1 = (**(code **)(param_9 + 0x20))(*(undefined4 *)(param_9 + 0x28),0x120,4);
  if (iVar1 == 0) {
    local_8 = -4;
  }
  else {
    local_8 = FUN__text1__00847068
                        (param_3,param_1,0x101,&DAT_00873da0,&DAT_00873e1c,param_6,param_4,param_8,
                         &local_c,iVar1);
    if ((local_8 == 0) && (*param_4 != 0)) {
      local_8 = FUN__text1__00847068
                          (param_3 + param_1 * 4,param_2,0,&DAT_00873e98,&DAT_00873f10,param_7,
                           param_5,param_8,&local_c,iVar1);
      if ((local_8 == 0) && ((*param_5 != 0 || (param_1 < 0x102)))) {
        (**(code **)(param_9 + 0x24))(*(undefined4 *)(param_9 + 0x28),iVar1);
        local_8 = 0;
      }
      else {
        if (local_8 == -3) {
          *(char **)(param_9 + 0x18) = "oversubscribed distance tree";
        }
        else if (local_8 == -5) {
          *(char **)(param_9 + 0x18) = "incomplete distance tree";
          local_8 = -3;
        }
        else if (local_8 != -4) {
          *(char **)(param_9 + 0x18) = "empty distance tree with lengths";
          local_8 = -3;
        }
        (**(code **)(param_9 + 0x24))(*(undefined4 *)(param_9 + 0x28),iVar1);
      }
    }
    else {
      if (local_8 == -3) {
        *(char **)(param_9 + 0x18) = "oversubscribed literal/length tree";
      }
      else if (local_8 != -4) {
        *(char **)(param_9 + 0x18) = "incomplete literal/length tree";
        local_8 = -3;
      }
      (**(code **)(param_9 + 0x24))(*(undefined4 *)(param_9 + 0x28),iVar1);
    }
  }
  return local_8;
}

