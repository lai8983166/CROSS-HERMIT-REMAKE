
void FUN__text__00468f40(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  byte local_18;
  int local_14;
  short local_10;
  short local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00468d10(param_1);
  if ((iVar2 == 0) &&
     (iVar2 = FUN__text__00424f80("IsUwUsed(wk)!=0",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b60 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (param_1 != 0) {
    local_14 = *(char *)(param_1 + 0x290) + -1;
    switch(*(char *)(param_1 + 0x290)) {
    case '\x01':
    case '\f':
    case '\r':
    case '\x0e':
    case '\x19':
      break;
    default:
      if ((((*(char *)(local_8 + 0x108b48) == '\0') ||
           (local_18 = *(byte *)(*(int *)(param_1 + 600) + 0xf), local_18 < 3)) || (5 < local_18))
         && (iVar2 = FUN__text__0046a430(param_1), iVar2 == 0)) {
        local_c = (short)((int)((*(int *)(param_1 + 0x2ec) >> 0x10) +
                               (*(int *)(param_1 + 0x2ec) >> 0x1f & 0x1fU)) >> 5);
        local_10 = (short)((int)((*(int *)(param_1 + 0x2f0) >> 0x10) +
                                (*(int *)(param_1 + 0x2f0) >> 0x1f & 0xfU)) >> 4);
        FUN__text__0043c160((int)local_c,(int)local_10);
      }
    }
  }
  local_8 = 0x469076;
  FUN__text__0056ce80();
  return;
}

