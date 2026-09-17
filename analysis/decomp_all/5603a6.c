
int FUN__text__005603a6(undefined4 param_1,int *param_2,undefined4 param_3,undefined4 param_4,
                       int param_5)

{
  int iVar1;
  int iVar2;
  undefined4 local_8;
  
  local_8 = 0;
  iVar1 = (**(code **)(param_5 + 0x20))(*(undefined4 *)(param_5 + 0x28),0x13,4);
  if (iVar1 == 0) {
    iVar2 = -4;
  }
  else {
    iVar2 = FUN__text__00560021(param_1,0x13,0x13,0,0,param_3,param_4,&local_8,iVar1);
    if (iVar2 == -3) {
      *(char **)(param_5 + 0x18) = "oversubscribed dynamic bit lengths tree";
    }
    else if ((iVar2 == -5) || (*param_2 == 0)) {
      *(char **)(param_5 + 0x18) = "incomplete dynamic bit lengths tree";
      iVar2 = -3;
    }
    (**(code **)(param_5 + 0x24))(*(undefined4 *)(param_5 + 0x28),iVar1);
  }
  return iVar2;
}

