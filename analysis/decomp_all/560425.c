
int FUN__text__00560425(uint param_1,undefined4 param_2,int param_3,int *param_4,int *param_5,
                       undefined4 param_6,undefined4 param_7,undefined4 param_8,int param_9)

{
  int iVar1;
  int iVar2;
  undefined4 local_8;
  
  local_8 = 0;
  iVar1 = (**(code **)(param_9 + 0x20))(*(undefined4 *)(param_9 + 0x28),0x120,4);
  if (iVar1 == 0) {
    return -4;
  }
  iVar2 = FUN__text__00560021(param_3,param_1,0x101,&DAT_005d4458,&DAT_005d44d8,param_6,param_8,
                              &local_8,iVar1);
  if (iVar2 == 0) {
    if (*param_4 == 0) goto LAB__text__0056050a;
    iVar2 = FUN__text__00560021(param_3 + param_1 * 4,param_2,0,&DAT_005d4558,&DAT_005d45d0,param_7,
                                param_8,&local_8,iVar1);
    if (iVar2 == 0) {
      if ((*param_5 != 0) || (param_1 < 0x102)) {
        iVar2 = 0;
        goto LAB__text__00560516;
      }
LAB__text__005604ee:
      *(char **)(param_9 + 0x18) = "empty distance tree with lengths";
    }
    else {
      if (iVar2 == -3) {
        *(char **)(param_9 + 0x18) = "oversubscribed distance tree";
        goto LAB__text__00560516;
      }
      if (iVar2 != -5) {
        if (iVar2 == -4) goto LAB__text__00560516;
        goto LAB__text__005604ee;
      }
      *(char **)(param_9 + 0x18) = "incomplete distance tree";
    }
  }
  else {
    if (iVar2 == -3) {
      *(char **)(param_9 + 0x18) = "oversubscribed literal/length tree";
      goto LAB__text__00560516;
    }
    if (iVar2 == -4) goto LAB__text__00560516;
LAB__text__0056050a:
    *(char **)(param_9 + 0x18) = "incomplete literal/length tree";
  }
  iVar2 = -3;
LAB__text__00560516:
  (**(code **)(param_9 + 0x24))(*(undefined4 *)(param_9 + 0x28),iVar1);
  return iVar2;
}

