
void FUN__text__00471ab0(undefined4 param_1,undefined4 param_2,int param_3,int param_4,
                        undefined4 *param_5,undefined4 *param_6)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_54 [16];
  int local_14;
  int local_10;
  char local_c;
  undefined4 local_8;
  
  puVar2 = local_54;
  for (iVar1 = 0x14; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = (&DAT_00618801)[param_3 + (param_4 + 1) * 3];
  local_14 = local_c + -1;
  switch(local_14) {
  case 0:
    local_10 = FUN__text__00471ca0(0xfffffff1,0,0x10,0x10,param_5,param_6);
    goto joined_r0x00471c33;
  case 1:
    local_10 = FUN__text__00471ca0(0xfffffff1,0,0x1f,0x10,param_5,param_6);
joined_r0x00471c33:
    if (local_10 != 0) goto switchD__text__00471b00_default;
    goto switchD__text__00471b00_caseD_4;
  case 2:
    local_10 = FUN__text__00471ca0(0,0,0x10,0x10,param_5,param_6);
    break;
  case 3:
    local_10 = FUN__text__00471ca0(0xfffffff1,0xfffffff1,0x10,0x1f,param_5,param_6);
    break;
  case 4:
    goto switchD__text__00471b00_caseD_4;
  case 5:
    local_10 = FUN__text__00471ca0(0,0xfffffff1,0x10,0x1f,param_5,param_6);
    break;
  case 6:
    local_10 = FUN__text__00471ca0(0xfffffff1,0xfffffff1,0x10,0x10,param_5,param_6);
    break;
  case 7:
    local_10 = FUN__text__00471ca0(0xfffffff1,0xfffffff1,0x1f,0x10,param_5,param_6);
    break;
  case 8:
    local_10 = FUN__text__00471ca0(0,0xfffffff1,0x10,0x10,param_5,param_6);
    break;
  default:
    goto switchD__text__00471b00_default;
  }
  if (local_10 == 0) {
switchD__text__00471b00_caseD_4:
    *param_6 = 0;
    *param_5 = 0;
  }
switchD__text__00471b00_default:
  local_8 = 0x471c71;
  FUN__text__0056ce80();
  return;
}

