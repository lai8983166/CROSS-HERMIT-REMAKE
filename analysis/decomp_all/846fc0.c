
int FUN__text1__00846fc0
              (undefined4 param_1,int *param_2,undefined4 param_3,undefined4 param_4,int param_5)

{
  int iVar1;
  undefined4 local_c;
  int local_8;
  
  local_c = 0;
  iVar1 = (**(code **)(param_5 + 0x20))(*(undefined4 *)(param_5 + 0x28),0x13,4);
  if (iVar1 == 0) {
    local_8 = -4;
  }
  else {
    local_8 = FUN__text1__00847068(param_1,0x13,0x13,0,0,param_3,param_2,param_4,&local_c,iVar1);
    if (local_8 == -3) {
      *(char **)(param_5 + 0x18) = "oversubscribed dynamic bit lengths tree";
    }
    else if ((local_8 == -5) || (*param_2 == 0)) {
      *(char **)(param_5 + 0x18) = "incomplete dynamic bit lengths tree";
      local_8 = -3;
    }
    (**(code **)(param_5 + 0x24))(*(undefined4 *)(param_5 + 0x28),iVar1);
  }
  return local_8;
}

