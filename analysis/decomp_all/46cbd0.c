
void FUN__text__0046cbd0(int param_1)

{
  code *pcVar1;
  undefined1 uVar2;
  int iVar3;
  undefined4 uVar4;
  undefined2 extraout_var;
  int iVar5;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  int extraout_ECX_04;
  undefined2 uVar6;
  undefined2 extraout_var_00;
  undefined4 *puVar7;
  undefined4 local_80 [16];
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  int local_34;
  uint local_30;
  int local_2c;
  undefined2 local_28;
  short local_24;
  short local_20;
  undefined2 local_1c;
  undefined2 local_18;
  short local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar7 = local_80;
  for (iVar5 = 0x1f; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar7 = 0xcccccccc;
    puVar7 = puVar7 + 1;
  }
  local_28 = 0;
  local_34 = FUN__text__0046a950(param_1);
  if ((0 < local_34) && (local_34 < 4)) {
    iVar5 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
    local_20 = (short)((int)(iVar5 + (iVar5 >> 0x1f & 0x1fU)) >> 5);
    iVar5 = (int)(short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
    local_24 = (short)((int)(iVar5 + (iVar5 >> 0x1f & 0xfU)) >> 4);
    iVar5 = FUN__text__0043c160((int)local_20,(int)local_24);
    if (iVar5 == 0) goto LAB__text__0046d1bb;
  }
  local_20 = (short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10) - *(short *)(local_8 + 0x2a30e)
  ;
  iVar5 = ((int)(short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10) -
          (int)*(short *)(local_8 + 0x2a310)) + 0x1e;
  local_24 = (short)iVar5;
  iVar5 = FUN__text__0046b130(local_20,iVar5);
  if (iVar5 != 0) {
    *(byte *)(param_1 + 8) = *(byte *)(param_1 + 8) | 0x80;
    local_28 = 1;
    local_14 = 0x6e8 - local_24;
    local_18 = 900;
    local_1c = 0x74c;
    FUN__text__0046d6a0(param_1,CONCAT22(local_24 >> 0xf,local_20),local_24);
    local_10 = 0;
    *(byte *)(param_1 + 0x4b) = *(byte *)(param_1 + 0x4b) & 0xf7;
    if ((*(short *)(local_8 + 0x30992) == -1) ||
       (*(short *)(local_8 + 0x30992) != *(short *)(param_1 + 2))) {
      iVar3 = FUN__text__00456b20();
      iVar5 = extraout_ECX_01;
      if ((iVar3 != 0) &&
         (iVar3 = FUN__text__00468d80(param_1), iVar5 = extraout_ECX_02, iVar3 != 0)) {
        local_38 = FUN__text__0046a950(param_1);
        iVar5 = param_1;
        switch(local_38) {
        case 0:
          iVar5 = extraout_ECX_03;
          break;
        case 1:
          *(byte *)(param_1 + 0x4b) = *(byte *)(param_1 + 0x4b) | 8;
          *(undefined1 *)(param_1 + 0x9c) = 0x96;
          *(undefined1 *)(param_1 + 0x9d) = 100;
          *(undefined1 *)(param_1 + 0x9e) = 0x50;
          break;
        case 2:
          *(byte *)(param_1 + 0x4b) = *(byte *)(param_1 + 0x4b) | 8;
          *(undefined1 *)(param_1 + 0x9c) = 0x8c;
          *(undefined1 *)(param_1 + 0x9d) = 0x82;
          *(undefined1 *)(param_1 + 0x9e) = 0x28;
          break;
        case 3:
          *(byte *)(param_1 + 0x4b) = *(byte *)(param_1 + 0x4b) | 8;
          *(undefined1 *)(param_1 + 0x9c) = 0x5a;
          *(undefined1 *)(param_1 + 0x9d) = 0x5a;
          *(undefined1 *)(param_1 + 0x9e) = 0x5a;
          break;
        case 4:
          *(byte *)(param_1 + 0x4b) = *(byte *)(param_1 + 0x4b) | 8;
          *(undefined1 *)(param_1 + 0x9c) = 100;
          *(undefined1 *)(param_1 + 0x9d) = 0x8c;
          *(undefined1 *)(param_1 + 0x9e) = 0x5a;
          break;
        default:
          iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                      DAT_00618c18 + 0x4c,0);
          iVar5 = extraout_ECX_04;
          if (iVar3 != 0) {
            pcVar1 = (code *)swi(3);
            (*pcVar1)();
            return;
          }
        }
      }
    }
    else {
      *(byte *)(param_1 + 0x4b) = *(byte *)(param_1 + 0x4b) | 8;
      local_2c = FUN__text__0046a950(param_1);
      if (((local_2c < 0) || (uVar4 = extraout_ECX, 4 < local_2c)) &&
         (iVar5 = FUN__text__00424f80("(0<=off) && (off<=4)",
                                      "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                      DAT_00618c18 + 0x3c,0), uVar4 = extraout_ECX_00, iVar5 != 0))
      {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      *(undefined *)(param_1 + 0x9c) = (&DAT_0061877c)[local_2c * 3];
      *(undefined *)(param_1 + 0x9d) = (&DAT_0061877d)[local_2c * 3];
      uVar2 = (&DAT_0061877e)[local_2c * 3];
      *(undefined1 *)(param_1 + 0x9e) = uVar2;
      local_10 = 1;
      iVar5 = CONCAT31((int3)((uint)uVar4 >> 8),uVar2);
    }
    uVar6 = (undefined2)((uint)iVar5 >> 0x10);
    if (local_10 == 0) {
      local_3c = FUN__text__0046a950(param_1);
      uVar6 = extraout_var_00;
      switch(local_3c) {
      case 0:
      case 4:
        goto switchD__text__0046cf4f_caseD_0;
      case 1:
      case 2:
      case 3:
        if (*(char *)(param_1 + 0x28c) != '\0') goto switchD__text__0046cf4f_caseD_0;
        break;
      default:
        iVar5 = FUN__text__00424f80(&DAT_005924d4,
                                    "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                    DAT_00618c18 + 0x6d,0);
        if (iVar5 != 0) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
      }
    }
    else {
switchD__text__0046cf4f_caseD_0:
      FUN__text__0046d340(param_1,(int)local_20,(int)local_24,CONCAT22(uVar6,local_14));
    }
    FUN__text__0040a1e0();
    FUN__text__0040a220(param_1 + 0x48);
    for (local_c = 0; local_c != 5; local_c = local_c + 1) {
      FUN__text__0040a220(param_1 + 0xa0 + local_c * 0x58);
    }
    FUN__text__0040a290(local_8 + 0xde4b0,(int)local_20,(int)local_24,local_14,local_1c,local_18);
    iVar5 = FUN__text__00469500(param_1);
    if (iVar5 != 0) {
      FUN__text__0046d210(param_1,0x756);
    }
  }
  iVar5 = FUN__text__00469480(param_1);
  if (((iVar5 != 0) && (*(int *)(local_8 + 0x108b50) == 1)) && (*(char *)(param_1 + 0x28c) != '\0'))
  {
    uVar4 = FUN__text__0046ca60(param_1);
    uVar2 = FUN__text__004ddc60(param_1,uVar4);
    FUN__text__0043c530((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                             (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5,
                        (int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                             (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4,uVar2);
  }
  iVar5 = FUN__text__0046a430(param_1);
  if (iVar5 != 0) {
    FUN__text__0046db20(param_1,0);
    FUN__text__0046e0f0(param_1);
    if (*(char *)(param_1 + 0x28c) != '\0') {
      FUN__text__00472860(local_20,CONCAT22(extraout_var,local_24),0x352);
    }
  }
  local_20 = (short)((uint)*(undefined4 *)(param_1 + 0x2ec) >> 0x10);
  local_24 = (short)((uint)*(undefined4 *)(param_1 + 0x2f0) >> 0x10);
  local_40 = FUN__text__0046a950(param_1);
  switch(local_40) {
  case 0:
    local_30 = (uint)(*(char *)(param_1 + 0x28c) == '\0');
    break;
  case 1:
    local_30 = 3;
    break;
  case 2:
  case 3:
  case 4:
    local_30 = 2;
  }
  FUN__text__00440fe0(local_20,local_24,local_30);
LAB__text__0046d1bb:
  local_8 = 0x46d1c8;
  FUN__text__0056ce80();
  return;
}

