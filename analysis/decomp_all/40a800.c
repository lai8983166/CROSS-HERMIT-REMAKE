
void __thiscall FUN__text__0040a800(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_60 [16];
  uint local_20;
  byte *local_1c;
  byte *local_18;
  byte *local_14;
  byte *local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar2 = local_60;
  for (iVar1 = 0x17; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  *(undefined1 *)(param_2 + 1) = 1;
  local_8 = param_1;
  if (*(char *)(param_2 + 0xb) == '\0') {
    if (*(int *)(param_2 + 4) != 0) {
      if (*(int *)(param_2 + 0x2c) != 0) {
        if (0 < *(short *)(param_2 + 0x48)) {
          *(short *)(param_2 + 0x48) = *(short *)(param_2 + 0x48) + -1;
          if (*(short *)(param_2 + 0x48) == 0) {
            *(undefined2 *)(param_2 + 0x48) = 0xfffe;
          }
          goto switchD__text__0040a8ed_default;
        }
        if (*(short *)(param_2 + 0x48) == -2) {
          *(undefined2 *)(param_2 + 0x48) = 0xfffd;
          FUN__text__0040a520(param_2);
        }
      }
LAB__text__0040a8c4:
      local_c = CONCAT31(local_c._1_3_,**(byte **)(param_2 + 4)) & 0xffffff03;
      local_20 = **(byte **)(param_2 + 4) & 3;
      switch(local_20) {
      case 0:
        goto switchD__text__0040a8ed_caseD_0;
      case 1:
        local_14 = *(byte **)(param_2 + 4);
        if ((*(byte *)(param_2 + 8) < 8) && (*(short *)(local_14 + 2) != -1)) {
          FUN__text__0040ada0(param_2,local_14);
        }
        if ((*local_14 & 0x80) != 0) {
          *(undefined1 *)(param_2 + 0xb) = 1;
          break;
        }
        *(int *)(param_2 + 4) = *(int *)(param_2 + 4) + 10;
        FUN__text__0040a520(param_2);
        goto LAB__text__0040a8c4;
      case 2:
        local_18 = *(byte **)(param_2 + 4);
        if (*(short *)(local_18 + 8) != -1) {
          FUN__text__0040b990(*(undefined2 *)(local_18 + 8),0);
        }
        if ((*local_18 & 0x80) != 0) {
          *(undefined1 *)(param_2 + 0xb) = 1;
          break;
        }
        *(int *)(param_2 + 4) = *(int *)(param_2 + 4) + 10;
        FUN__text__0040a520(param_2);
        goto LAB__text__0040a8c4;
      case 3:
        local_1c = *(byte **)(param_2 + 4);
        if (*(short *)(param_2 + 0x10) != 0x7f) {
          if ((*(short *)(param_2 + 0x10) == 0) || (*(short *)(param_2 + 0x10) == 1)) {
            if ((*local_1c & 0x80) != 0) {
              *(undefined1 *)(param_2 + 0xb) = 1;
              break;
            }
            *(undefined2 *)(param_2 + 0x10) = 0;
            *(int *)(param_2 + 4) = *(int *)(param_2 + 4) + 10;
            FUN__text__0040a520(param_2);
            goto LAB__text__0040a8c4;
          }
          *(short *)(param_2 + 0x10) = *(short *)(param_2 + 0x10) + -1;
        }
        if ((*local_1c & 0x40) == 0) {
          *(int *)(param_2 + 4) = *(int *)(param_2 + 4) + *(short *)(local_1c + 2) * -10;
        }
        else {
          *(int *)(param_2 + 4) = *(int *)(param_2 + 4) + *(short *)(local_1c + 2) * 10;
        }
        FUN__text__0040a520(param_2);
        goto LAB__text__0040a8c4;
      default:
        break;
      }
    }
  }
  else {
    *(undefined4 *)(param_2 + 4) = 0;
    FUN__text__0040ab80(param_2);
  }
switchD__text__0040a8ed_default:
  local_8 = 0x40ab63;
  FUN__text__0056ce80();
  return;
switchD__text__0040a8ed_caseD_0:
  *(undefined4 *)(param_2 + 0x28) = *(undefined4 *)(param_2 + 4);
  local_10 = *(byte **)(param_2 + 0x28);
  *(short *)(param_2 + 0xe) = *(short *)(param_2 + 0xe) + -1;
  if (0 < *(short *)(param_2 + 0xe)) goto switchD__text__0040a8ed_default;
  if ((*local_10 & 0x80) != 0) {
    *(undefined1 *)(param_2 + 0xb) = 1;
    goto switchD__text__0040a8ed_default;
  }
  *(int *)(param_2 + 4) = *(int *)(param_2 + 4) + 10;
  FUN__text__0040a520(param_2);
  local_c = CONCAT31(local_c._1_3_,**(byte **)(param_2 + 4)) & 0xffffff03;
  if ((**(byte **)(param_2 + 4) & 3) == 0) goto switchD__text__0040a8ed_default;
  goto LAB__text__0040a8c4;
}

