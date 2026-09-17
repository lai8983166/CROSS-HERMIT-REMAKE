
void FUN__text__0046a950(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__0046a430(param_1);
  if (iVar2 == 0) {
    local_c = (int)*(char *)(local_8 + 0x115aac + (uint)*(byte *)(local_8 + 0x2ef44) * 0x10 +
                            (uint)*(byte *)(*(int *)(param_1 + 600) + 0xa4));
    switch(local_c) {
    case 0:
      break;
    case 1:
      break;
    case 2:
      break;
    case 3:
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618be0 + 0xb,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
  }
  local_8 = 0x46aa1c;
  FUN__text__0056ce80();
  return;
}

