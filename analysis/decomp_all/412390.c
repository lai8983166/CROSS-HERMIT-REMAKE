
void __thiscall FUN__text__00412390(int param_1,int *param_2,uint param_3,uint param_4)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  int *local_c;
  int local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (int *)(param_1 + 0x9cc);
  param_2[4] = param_2[4] + 1;
  local_8 = param_1;
  if (*param_2 == 1) {
    if (param_2[4] <= *(int *)(param_1 + 0x9d4)) {
      local_10 = FUN__text__0056db00(param_2[1] - *(int *)(param_1 + 0x8c4));
      local_14 = FUN__text__0056db00(param_2[2] - *(int *)(local_8 + 0x8c8));
      if ((local_10 <= *local_c) && (local_14 <= local_c[1])) goto LAB__text__00412437;
    }
  }
  else {
LAB__text__00412437:
    if ((*(uint *)(local_8 + 0x8d8) & param_3) == 0) goto LAB__text__004124c4;
    if (*param_2 == 0) {
      *param_2 = 1;
      param_2[4] = 0;
      param_2[1] = *(int *)(local_8 + 0x8c4);
      param_2[2] = *(int *)(local_8 + 0x8c8);
      param_2[3] = *(int *)(local_8 + 0x8cc);
      goto LAB__text__004124c4;
    }
    *(uint *)(local_8 + 0x8d8) = *(uint *)(local_8 + 0x8d8) | param_4;
    *(uint *)(local_8 + 0x8dc) = *(uint *)(local_8 + 0x8dc) | param_3;
  }
  *param_2 = 0;
LAB__text__004124c4:
  local_8 = 0x4124db;
  FUN__text__0056ce80();
  return;
}

