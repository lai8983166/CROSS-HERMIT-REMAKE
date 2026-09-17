
void FUN__text__0046ae20(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00468d10(param_1);
  if ((iVar2 == 0) &&
     (iVar2 = FUN__text__00424f80("IsUwUsed(wkf)",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618bf8 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  iVar2 = FUN__text__00468d10(param_2);
  if ((iVar2 == 0) &&
     (iVar2 = FUN__text__00424f80("IsUwUsed(wkt)",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618bf8 + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = *(char *)(param_2 + 0x290) + -1;
  switch(*(char *)(param_2 + 0x290)) {
  case '\x01':
  case '\f':
  case '\r':
  case '\x19':
    break;
  default:
    iVar2 = FUN__text__0046a050(param_2);
    if (iVar2 == 0) {
      local_10 = FUN__text__0046af50(param_1,param_2);
    }
  }
  local_8 = 0x46af22;
  FUN__text__0056ce80();
  return;
}

