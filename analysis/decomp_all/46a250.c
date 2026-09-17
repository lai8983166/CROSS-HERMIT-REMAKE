
void FUN__text__0046a250(int param_1)

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
  if (((param_1 < 0) || (0x3ff < param_1)) &&
     (iVar2 = FUN__text__00424f80("(0<=skill_no) && (skill_no<1024)",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618bc0 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = param_1;
  local_8 = 0x46a2ea;
  FUN__text__0056ce80();
  return;
}

