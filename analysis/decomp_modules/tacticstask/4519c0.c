
void __fastcall FUN__text__004519c0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_1 + 0x34);
  local_8 = param_1;
  if (local_c == 0) {
    FUN__text__00451f50();
  }
  else if (local_c == 1) {
    FUN__text__00452f90();
  }
  else if (local_c == 2) {
    FUN__text__00452fc0();
  }
  else {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp"
                                ,DAT_0060cd6c + 0xc,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x451a54;
  FUN__text__0056ce80();
  return;
}

