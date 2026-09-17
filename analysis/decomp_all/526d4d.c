
int FUN__text__00526d4d(int *param_1,undefined4 param_2,undefined4 param_3,int *param_4)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  int *piVar4;
  int *piVar5;
  int *piVar6;
  undefined4 local_ec;
  undefined4 local_e8;
  undefined1 local_18 [12];
  undefined4 local_c;
  int *local_8;
  
  local_8 = (int *)0x0;
  FUN__text__0052b019(1);
  if (param_1 != (int *)0x0) {
    (**(code **)(*param_1 + 0x18))(param_1,&local_8);
    (**(code **)(*param_1 + 0x1c))(param_1,&local_ec);
    (**(code **)(*param_1 + 0x20))(param_1,local_18);
  }
  uVar3 = 0xffffffff;
  piVar4 = &DAT_005d03c8;
  piVar6 = &DAT_005d03a0;
  piVar5 = &DAT_005d03a0;
  if (&DAT_005d03c8 < PTR_DAT_0075dda4) {
    do {
      piVar6 = piVar5;
      if ((*piVar4 != 0) &&
         ((param_1 == (int *)0x0 ||
          (iVar1 = (**(code **)(*local_8 + 0x28))
                             (local_8,local_e8,local_ec,local_c,param_2,param_3,*piVar4), -1 < iVar1
          )))) {
        piVar6 = piVar4;
        if (*param_4 == *piVar4) break;
        piVar6 = piVar5;
        if ((((piVar4[8] != 0) && (uVar2 = FUN__text__00526c6a(), uVar2 != 0xffffffff)) &&
            (uVar2 <= uVar3)) && ((uVar2 != uVar3 || ((uint)piVar4[2] < (uint)piVar5[2])))) {
          uVar3 = uVar2;
          piVar6 = piVar4;
        }
      }
      piVar4 = piVar4 + 9;
      piVar5 = piVar6;
    } while (piVar4 < PTR_DAT_0075dda4);
  }
  if (local_8 != (int *)0x0) {
    (**(code **)(*local_8 + 8))(local_8);
    local_8 = (int *)0x0;
  }
  FUN__text__0052b019(0);
  return *piVar6;
}

