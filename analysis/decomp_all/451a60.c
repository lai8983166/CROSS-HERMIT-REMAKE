
void __fastcall FUN__text__00451a60(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  undefined4 local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_10 = *(int *)(param_1 + 0x34);
  local_8 = param_1;
  if (local_10 == 0) {
    local_c = FUN__text__004538d0();
  }
  else if (local_10 == 1) {
    local_c = FUN__text__00453930();
  }
  else if (local_10 == 2) {
    local_c = FUN__text__004539b0();
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp"
                                ,DAT_0060cd70 + 0x11,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x451b0b;
  FUN__text__0056ce80();
  return;
}

