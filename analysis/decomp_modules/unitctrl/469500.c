
void FUN__text__00469500(int param_1)

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
  if ((param_1 == 0) &&
     (iVar2 = FUN__text__00424f80("wk!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618b7c + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(char *)(*(int *)(param_1 + 600) + 0xf) == '\x01') {
    local_c = *(char *)(param_1 + 0x290) + -1;
    switch(*(char *)(param_1 + 0x290)) {
    case '\x01':
    case '\f':
    case '\r':
    case '\x0e':
    case '\x19':
      break;
    default:
    }
  }
  local_8 = 0x4695a2;
  FUN__text__0056ce80();
  return;
}

