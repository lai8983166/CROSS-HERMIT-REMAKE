
void FUN__text__004048d0(undefined4 param_1,undefined4 param_2,int param_3,undefined4 param_4,
                        int param_5,undefined4 param_6,undefined4 *param_7)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  undefined4 *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_3;
  iVar2 = FUN__text__004209f0(param_3);
  if (iVar2 != 0) goto LAB__text__00404afa;
  FUN__text__00420a40(local_c);
  local_1c = *(ushort *)(local_c + 0x1c) - 4;
  switch(*(ushort *)(local_c + 0x1c)) {
  case 4:
  case 8:
    if (*(short *)(local_c + 0x1c) == 4) goto code_r0x00404aa8;
    if (param_5 == 1) {
      if (param_7 == (undefined4 *)0x0) {
        local_10 = (undefined4 *)(local_c + 0x36);
        for (local_14 = 0; local_14 != *(int *)(local_c + 0x2e); local_14 = local_14 + 1) {
          if (((*(char *)(local_c + 0x38 + local_14 * 4) == '\0') &&
              (*(char *)(local_c + 0x37 + local_14 * 4) == '\0')) &&
             ((*(char *)(local_10 + local_14) == '\0' && (local_14 != 0)))) {
            local_10[local_14] = *local_10;
          }
        }
      }
      else {
        local_10 = param_7;
        for (local_14 = 0; local_14 != 0x100; local_14 = local_14 + 1) {
          if ((((*(char *)((int)param_7 + local_14 * 4 + 2) == '\0') &&
               (*(char *)((int)param_7 + local_14 * 4 + 1) == '\0')) &&
              (*(char *)(param_7 + local_14) == '\0')) && (local_14 != 0)) {
            param_7[local_14] = *param_7;
          }
        }
      }
    }
    *(undefined2 *)(local_8 + 0x38) = *(undefined2 *)(local_c + 0x12);
    *(undefined2 *)(local_8 + 0x3a) = *(undefined2 *)(local_c + 0x16);
    iVar2 = FUN__text__00403bd0(param_1,param_2);
    if (iVar2 != 0) goto LAB__text__00404afa;
    iVar2 = FUN__text__00404150(param_3,param_4,param_6,param_7);
    break;
  default:
    goto switchD__text__00404943_caseD_5;
  case 0x10:
  case 0x18:
  case 0x20:
code_r0x00404aa8:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                "e:\\crosshermit\\game\\src\\system\\directx\\d3dtex.cpp",
                                DAT_005ff0a0 + 0x39,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    local_18 = FUN__text__00404ca0(param_1,param_3,param_4,param_5);
    iVar2 = local_18;
  }
  if (iVar2 == 0) {
switchD__text__00404943_caseD_5:
  }
LAB__text__00404afa:
  local_8 = 0x404b07;
  FUN__text__0056ce80();
  return;
}

