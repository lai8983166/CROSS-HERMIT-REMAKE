
void __thiscall FUN__text__00412650(int param_1,int *param_2,uint param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (((*(uint *)(param_1 + 0x8d0) & param_3) == 0) && ((*(uint *)(param_1 + 0x8d4) & param_3) != 0)
     ) {
    *param_2 = 1;
    param_2[1] = *(int *)(param_1 + 0x8b4);
    param_2[2] = *(int *)(param_1 + 0x8b8);
    param_2[3] = *(int *)(param_1 + 0x8bc);
  }
  else {
    if (((*(uint *)(param_1 + 0x8d0) & param_3) == 0) ||
       ((*(uint *)(param_1 + 0x8d4) & param_3) == 0)) {
      if ((((*(uint *)(param_1 + 0x8d0) & param_3) != 0) &&
          ((*(uint *)(param_1 + 0x8d4) & param_3) == 0)) && (*param_2 == 2)) {
        *param_2 = 3;
        local_8 = param_1;
        local_c = FUN__text__0056db00(*(int *)(param_1 + 0x8b4) - param_2[1]);
        local_10 = FUN__text__0056db00(*(int *)(local_8 + 0x8b8) - param_2[2]);
        if (*(int *)(local_8 + 0x9d8) < local_c) {
          param_2[4] = *(int *)(local_8 + 0x8b4);
        }
        else {
          param_2[4] = param_2[1];
        }
        if (*(int *)(local_8 + 0x9dc) < local_10) {
          param_2[5] = *(int *)(local_8 + 0x8b8);
        }
        else {
          param_2[5] = param_2[2];
        }
        param_2[6] = *(int *)(local_8 + 0x8bc);
        goto LAB__text__004127ef;
      }
    }
    else if ((*param_2 == 1) || (*param_2 == 2)) {
      *param_2 = 2;
      goto LAB__text__004127ef;
    }
    *param_2 = 0;
  }
LAB__text__004127ef:
  local_8 = 0x412804;
  FUN__text__0056ce80();
  return;
}

