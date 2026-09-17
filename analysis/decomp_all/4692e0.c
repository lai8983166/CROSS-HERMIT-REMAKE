
void FUN__text__004692e0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00468d10(param_1);
  if ((iVar2 == 0) &&
     (iVar2 = FUN__text__00424f80("IsUwUsed(wk)!=0",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b70 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(char *)(param_1 + 6) == '\0') {
    local_c = *(char *)(param_1 + 0x290) + -1;
    switch(*(char *)(param_1 + 0x290)) {
    case '\x01':
    case '\f':
    case '\r':
    case '\x19':
      break;
    default:
    }
  }
  local_8 = 0x469387;
  FUN__text__0056ce80();
  return;
}

