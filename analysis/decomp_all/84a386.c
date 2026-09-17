
LONG FUN__text1__0084a386(undefined4 param_1,_EXCEPTION_POINTERS *param_2)

{
  code *pcVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  int *piVar4;
  LONG LVar5;
  int iVar6;
  undefined4 *puVar7;
  
  piVar4 = (int *)FUN__text1__0084a4c7(param_1);
  uVar3 = DAT_008756c4;
  if ((piVar4 == (int *)0x0) || (pcVar1 = (code *)piVar4[2], pcVar1 == (code *)0x0)) {
    LVar5 = UnhandledExceptionFilter(param_2);
  }
  else if (pcVar1 == (code *)0x5) {
    piVar4[2] = 0;
    LVar5 = 1;
  }
  else {
    if (pcVar1 != (code *)0x1) {
      DAT_008756c4 = param_2;
      if (piVar4[1] == 8) {
        if (DAT_008704f8 < DAT_008704fc + DAT_008704f8) {
          iVar6 = (DAT_008704fc + DAT_008704f8) - DAT_008704f8;
          puVar7 = (undefined4 *)(&UNK_00870488 + DAT_008704f8 * 0xc);
          do {
            *puVar7 = 0;
            puVar7 = puVar7 + 3;
            iVar6 = iVar6 + -1;
          } while (iVar6 != 0);
        }
        uVar2 = DAT_00870504;
        iVar6 = *piVar4;
        if (iVar6 == -0x3fffff72) {
          DAT_00870504 = 0x83;
        }
        else if (iVar6 == -0x3fffff70) {
          DAT_00870504 = 0x81;
        }
        else if (iVar6 == -0x3fffff6f) {
          DAT_00870504 = 0x84;
        }
        else if (iVar6 == -0x3fffff6d) {
          DAT_00870504 = 0x85;
        }
        else if (iVar6 == -0x3fffff73) {
          DAT_00870504 = 0x82;
        }
        else if (iVar6 == -0x3fffff71) {
          DAT_00870504 = 0x86;
        }
        else if (iVar6 == -0x3fffff6e) {
          DAT_00870504 = 0x8a;
        }
        (*pcVar1)(8,DAT_00870504);
        DAT_00870504 = uVar2;
      }
      else {
        piVar4[2] = 0;
        (*pcVar1)(piVar4[1]);
      }
    }
    LVar5 = -1;
    DAT_008756c4 = (_EXCEPTION_POINTERS *)uVar3;
  }
  return LVar5;
}

