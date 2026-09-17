
void FUN__text__00589d40(undefined1 param_1,undefined4 *param_2,int *param_3,int *param_4,
                        int param_5)

{
  int local_c;
  int local_8;
  
  switch(param_1) {
  case 0x25:
    *(undefined1 *)*param_3 = 0x25;
    *param_3 = *param_3 + 1;
    *param_4 = *param_4 + -1;
    break;
  case 0x41:
    FID_conflict__store_str(*(undefined4 *)(param_5 + 0x1c + param_2[6] * 4),param_3,param_4);
    break;
  case 0x42:
    FID_conflict__store_str(*(undefined4 *)(param_5 + 0x68 + param_2[4] * 4),param_3,param_4);
    break;
  case 0x48:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(param_2[2],2,param_3,param_4);
    break;
  case 0x49:
    DAT_0080a7f8 = DAT_0080a7f4;
    local_8 = (int)param_2[2] % 0xc;
    if (local_8 == 0) {
      local_8 = 0xc;
    }
    FUN__text__0058a3b0(local_8,2,param_3,param_4);
    break;
  case 0x4d:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(param_2[1],2,param_3,param_4);
    break;
  case 0x53:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(*param_2,2,param_3,param_4);
    break;
  case 0x55:
    local_c = param_2[6];
    goto LAB__text__0058a0ed;
  case 0x57:
    if (param_2[6] == 0) {
      local_c = 6;
    }
    else {
      local_c = param_2[6] + -1;
    }
LAB__text__0058a0ed:
    DAT_0080a7f8 = DAT_0080a7f4;
    if ((int)param_2[7] < local_c) {
      local_8 = 0;
    }
    else {
      local_8 = (int)param_2[7] / 7;
      if (local_c <= (int)param_2[7] % 7) {
        local_8 = local_8 + 1;
      }
    }
    FUN__text__0058a3b0(local_8,2,param_3,param_4);
    break;
  case 0x58:
    DAT_0080a7f4 = 0;
    FUN__text__0058a510(*(undefined4 *)(param_5 + 0xa8),param_2,param_3,param_4,param_5);
    break;
  case 0x59:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(((int)param_2[5] / 100 + 0x13) * 100 + (int)param_2[5] % 100,4,param_3,
                        param_4);
    break;
  case 0x5a:
  case 0x7a:
    FUN__text__00587750();
    FID_conflict__store_str((&PTR_DAT_00764f5c)[param_2[8] != 0],param_3,param_4);
    break;
  case 0x61:
    FID_conflict__store_str(*(undefined4 *)(param_5 + param_2[6] * 4),param_3,param_4);
    break;
  case 0x62:
    FID_conflict__store_str(*(undefined4 *)(param_5 + 0x38 + param_2[4] * 4),param_3,param_4);
    break;
  case 99:
    if (DAT_0080a7f4 == 0) {
      FUN__text__0058a510(*(undefined4 *)(param_5 + 0xa0),param_2,param_3,param_4,param_5);
      if (*param_4 != 0) {
        *(undefined1 *)*param_3 = 0x20;
        *param_3 = *param_3 + 1;
        *param_4 = *param_4 + -1;
        FUN__text__0058a510(*(undefined4 *)(param_5 + 0xa8),param_2,param_3,param_4,param_5);
      }
    }
    else {
      DAT_0080a7f4 = 0;
      FUN__text__0058a510(*(undefined4 *)(param_5 + 0xa4),param_2,param_3,param_4,param_5);
      if (*param_4 != 0) {
        *(undefined1 *)*param_3 = 0x20;
        *param_3 = *param_3 + 1;
        *param_4 = *param_4 + -1;
        FUN__text__0058a510(*(undefined4 *)(param_5 + 0xa8),param_2,param_3,param_4,param_5);
      }
    }
    break;
  case 100:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(param_2[3],2,param_3,param_4);
    break;
  case 0x6a:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(param_2[7] + 1,3,param_3,param_4);
    break;
  case 0x6d:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(param_2[4] + 1,2,param_3,param_4);
    break;
  case 0x70:
    if ((int)param_2[2] < 0xc) {
      FID_conflict__store_str(*(undefined4 *)(param_5 + 0x98),param_3,param_4);
    }
    else {
      FID_conflict__store_str(*(undefined4 *)(param_5 + 0x9c),param_3,param_4);
    }
    break;
  case 0x77:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0(param_2[6],1,param_3,param_4);
    break;
  case 0x78:
    if (DAT_0080a7f4 == 0) {
      FUN__text__0058a510(*(undefined4 *)(param_5 + 0xa0),param_2,param_3,param_4,param_5);
    }
    else {
      DAT_0080a7f4 = 0;
      FUN__text__0058a510(*(undefined4 *)(param_5 + 0xa4),param_2,param_3,param_4,param_5);
    }
    break;
  case 0x79:
    DAT_0080a7f8 = DAT_0080a7f4;
    FUN__text__0058a3b0((int)param_2[5] % 100,2,param_3,param_4);
  }
  return;
}

