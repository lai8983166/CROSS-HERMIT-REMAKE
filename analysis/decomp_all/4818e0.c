
void __thiscall FUN__text__004818e0(int param_1,undefined4 param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_18 = 0;
  if (param_3 != 0) {
    local_1c = param_3;
    if (param_3 == 1) {
      local_c = 0;
      local_10 = 10;
    }
    else if (param_3 == 2) {
      local_c = 10;
      local_10 = 0x14;
    }
    else if (param_3 == 3) {
      local_c = 0;
      local_10 = 0x14;
    }
    local_8 = param_1;
    for (local_14 = local_c; local_14 != local_10; local_14 = local_14 + 1) {
      if ((*(int *)(local_8 + 0xdb818 + local_14 * 4) != 0) &&
         (iVar2 = FUN__text__0046fac0(param_2,local_14), iVar2 != 0)) {
        if ((*(char *)(*(int *)(*(int *)(local_8 + 0xdb818 + local_14 * 4) + 600) + 0xa4) !=
             *(char *)(local_8 + 0x2ef44)) &&
           (iVar2 = FUN__text__00424f80("FaceUwTbl[i]->data->player==PlayerNo",
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAppear.cpp",
                                        DAT_00618ed0 + 0x11,0), iVar2 != 0)) {
          pcVar1 = (code *)swi(3);
          (*pcVar1)();
          return;
        }
        iVar2 = FUN__text__00468d10(*(undefined4 *)(local_8 + 0xdb818 + local_14 * 4));
        if (((iVar2 != 0) &&
            (iVar2 = FUN__text__0046a7a0(*(undefined4 *)(local_8 + 0xdb818 + local_14 * 4)),
            iVar2 != 0)) && (*(char *)(*(int *)(local_8 + 0xdb818 + local_14 * 4) + 0x28c) != '\0'))
        break;
      }
    }
  }
  local_8 = 0x481a57;
  FUN__text__0056ce80();
  return;
}

