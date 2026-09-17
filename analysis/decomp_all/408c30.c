
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN__text__00408c30(float *param_1,float param_2,float param_3,short param_4)

{
  int iVar1;
  undefined4 *puVar2;
  float10 fVar3;
  undefined4 local_88 [16];
  double local_48;
  double local_40;
  double local_38;
  double local_30;
  double local_28;
  double local_20;
  int local_18;
  float local_14;
  float local_10;
  float local_c;
  undefined4 local_8;
  
  puVar2 = local_88;
  for (iVar1 = 0x21; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = *param_1 - param_2;
  local_10 = param_1[1] - param_3;
  local_18 = (int)param_4;
  local_14 = (float)local_18 * _DAT_00592778;
  local_20 = (double)local_c;
  fVar3 = (float10)FUN__text__0056d9d4((double)local_14);
  local_28 = (double)(fVar3 * (float10)local_20);
  local_30 = (double)local_10;
  fVar3 = (float10)FUN__text__0056d924((double)local_14);
  *param_1 = (float)((float10)local_28 - fVar3 * (float10)local_30);
  local_38 = (double)local_c;
  fVar3 = (float10)FUN__text__0056d924((double)local_14);
  local_40 = (double)(fVar3 * (float10)local_38);
  local_48 = (double)local_10;
  fVar3 = (float10)FUN__text__0056d9d4((double)local_14);
  param_1[1] = (float)(fVar3 * (float10)local_48 + (float10)local_40);
  *param_1 = param_2 + *param_1;
  param_1[1] = param_3 + param_1[1];
  local_8 = 0x408d2a;
  FUN__text__0056ce80();
  return;
}

