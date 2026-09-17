
void __thiscall FUN__text__00465f90(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_2 == 0) {
    iVar2 = FUN__text__00424f80("task!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618b14 + 1,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *(int *)(local_8 + 0x117c38) = param_2;
  local_8 = 0x465ff2;
  FUN__text__0056ce80();
  return;
}

