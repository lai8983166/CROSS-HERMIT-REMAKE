
void FUN__text__004900e0(int param_1,uint param_2)

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
  if ((param_2 == 0) &&
     (iVar2 = FUN__text__00424f80("no!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCond.cpp",
                                  DAT_006191f0 + 2,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = 0;
  while ((local_c != 3 && (*(byte *)(param_1 + 0x14 + local_c * 0x10) != param_2))) {
    local_c = local_c + 1;
  }
  local_8 = 0x49016c;
  FUN__text__0056ce80();
  return;
}

