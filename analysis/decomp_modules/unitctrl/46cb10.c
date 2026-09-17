
void FUN__text__0046cb10(int param_1,uint param_2)

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
  if ((((int)param_2 < 1) || (100 < (int)param_2)) &&
     (iVar2 = FUN__text__00424f80("(1<=skillno) && (skillno<=(100))",
                                  "E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                  DAT_00618c14 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = 0;
  while ((local_c != 8 &&
         (((*(ushort *)(*(int *)(param_1 + 600) + 0x84 + local_c * 2) & 0x8000) != 0 ||
          (*(ushort *)(*(int *)(param_1 + 600) + 0x84 + local_c * 2) != param_2))))) {
    local_c = local_c + 1;
  }
  local_8 = 0x46cbc8;
  FUN__text__0056ce80();
  return;
}

