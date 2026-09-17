
void FUN__text__0046bd30(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  char *local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = (char *)(param_1 + 0x290);
  local_10 = *local_c + -1;
  switch(*local_c) {
  case '\x01':
  case '\x19':
    FUN__text__0046bcc0(param_1,0x12);
    break;
  case '\x02':
    FUN__text__0046bcc0(param_1,1);
    break;
  case '\x03':
    FUN__text__0046bcc0(param_1,0x18);
    break;
  case '\x04':
    FUN__text__0046bcc0(param_1,3);
    break;
  case '\x05':
    FUN__text__0046bcc0(param_1,2);
    break;
  case '\x06':
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618c00 + 9,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x46be10;
  FUN__text__0056ce80();
  return;
}

