
void FUN__text__00574f20(int param_1,int param_2,uint *param_3,uint *param_4)

{
  int *piVar1;
  int iVar2;
  undefined4 uVar3;
  void *local_14;
  undefined1 *puStack_10;
  undefined *puStack_c;
  undefined4 local_8;
  
  puStack_c = &DAT_005fa060;
  puStack_10 = &LAB__text__00576b9c;
  local_14 = ExceptionList;
  if (((param_3[1] != 0) && (*(char *)(param_3[1] + 8) != '\0')) && (param_3[2] != 0)) {
    piVar1 = (int *)(param_2 + 0xc + param_3[2]);
    local_8 = 0;
    if ((*param_3 & 8) == 0) {
      if ((*param_4 & 1) == 0) {
        if (param_4[6] == 0) {
          ExceptionList = &local_14;
          iVar2 = FUN__text__00585990(*(undefined4 *)(param_1 + 0x18),1);
          if ((iVar2 == 0) || (iVar2 = FUN__text__005859c0(piVar1,1), iVar2 == 0)) {
            FUN__text__00575630();
          }
          else {
            uVar3 = FID_conflict____AdjustPointer
                              (*(undefined4 *)(param_1 + 0x18),param_4 + 2,param_4[5]);
            FUN__text__005855a0(piVar1,uVar3);
          }
        }
        else {
          ExceptionList = &local_14;
          iVar2 = FUN__text__00585990(*(undefined4 *)(param_1 + 0x18),1);
          if (((iVar2 == 0) || (iVar2 = FUN__text__005859c0(piVar1,1), iVar2 == 0)) ||
             (iVar2 = _ValidateExecute((_func_int *)param_4[6]), iVar2 == 0)) {
            FUN__text__00575630();
          }
          else if ((*param_4 & 4) == 0) {
            uVar3 = FID_conflict____AdjustPointer(*(undefined4 *)(param_1 + 0x18),param_4 + 2);
            FUN__text__0056d050(piVar1,param_4[6],uVar3);
          }
          else {
            uVar3 = FID_conflict____AdjustPointer(*(undefined4 *)(param_1 + 0x18),param_4 + 2,1);
            FUN__text__0056d060(piVar1,param_4[6],uVar3);
          }
        }
      }
      else {
        ExceptionList = &local_14;
        iVar2 = FUN__text__00585990(*(undefined4 *)(param_1 + 0x18),1);
        if ((iVar2 == 0) || (iVar2 = FUN__text__005859c0(piVar1,1), iVar2 == 0)) {
          FUN__text__00575630();
        }
        else {
          FUN__text__005855a0(piVar1,*(undefined4 *)(param_1 + 0x18),param_4[5]);
          if ((param_4[5] == 4) && (*piVar1 != 0)) {
            iVar2 = FID_conflict____AdjustPointer(*piVar1,param_4 + 2);
            *piVar1 = iVar2;
          }
        }
      }
    }
    else {
      ExceptionList = &local_14;
      iVar2 = FUN__text__00585990(*(undefined4 *)(param_1 + 0x18),1);
      if ((iVar2 == 0) || (iVar2 = FUN__text__005859c0(piVar1,1), iVar2 == 0)) {
        FUN__text__00575630();
      }
      else {
        *piVar1 = *(int *)(param_1 + 0x18);
        iVar2 = FID_conflict____AdjustPointer(*piVar1,param_4 + 2);
        *piVar1 = iVar2;
      }
    }
  }
  ExceptionList = local_14;
  return;
}

